"""Main Flask application for Coaching Portal."""

import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from datetime import datetime

from config import get_config
from models import (
    NewClientFormData,
    ExistingClientFormData,
    ClientListItem
)
from services.google_sheets_service import GoogleSheetsService
from services.email_service import EmailService
from services.ai_service import AIService
from services.client_service import ClientService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory function."""
    
    # Initialize Flask app
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    
    # Initialize services
    try:
        sheets_service = GoogleSheetsService()
        email_service = EmailService()
        ai_service = AIService()
        client_service = ClientService(sheets_service, email_service, ai_service)
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        # Services will be initialized lazily on first use
        sheets_service = None
        email_service = None
        ai_service = None
        client_service = None
    
    # Health check endpoint
    @app.route("/", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }), 200
    
    # Display new client form
    @app.route("/form/new-client", methods=["GET"])
    def new_client_form():
        """Display form for new client registration."""
        try:
            return render_template("new_client_form.html")
        except Exception as e:
            logger.error(f"Error rendering new client form: {e}")
            return redirect(url_for("error_page", msg="Failed to load form"))
    
    # Display existing client form
    @app.route("/form/existing-client", methods=["GET"])
    def existing_client_form():
        """Display form for existing client session."""
        try:
            return render_template("existing_client_form.html")
        except Exception as e:
            logger.error(f"Error rendering existing client form: {e}")
            return redirect(url_for("error_page", msg="Failed to load form"))
    
    # API: Submit new client form
    @app.route("/api/clients/new", methods=["POST"])
    def submit_new_client():
        """Process new client registration."""
        try:
            # Validate request data
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Parse and validate form data
            form_data = NewClientFormData(**data)
            
            # Process the registration
            if not client_service:
                raise RuntimeError("Client service not initialized")
            
            result = client_service.process_new_client_registration(form_data)
            
            logger.info(f"New client registered: {form_data.name}")
            return jsonify({
                "status": "success",
                "message": "Client registered successfully",
                "data": result
            }), 201
        
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error submitting new client: {e}")
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    
    # API: Submit existing client session
    @app.route("/api/clients/existing-session", methods=["POST"])
    def submit_existing_client_session():
        """Process existing client coaching session."""
        try:
            # Validate request data
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Parse and validate form data
            form_data = ExistingClientFormData(**data)
            
            # Process the session
            if not client_service:
                raise RuntimeError("Client service not initialized")
            
            result = client_service.process_existing_client_session(form_data)
            
            logger.info(f"Session recorded for client: {form_data.client_name}")
            return jsonify({
                "status": "success",
                "message": "Session recorded successfully",
                "data": result
            }), 201
        
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error submitting session: {e}")
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    
    # API: Get all clients (for dropdown)
    @app.route("/api/clients", methods=["GET"])
    def get_all_clients():
        """Get list of all clients for dropdown."""
        try:
            if not sheets_service:
                raise RuntimeError("Sheets service not initialized")
            
            clients = sheets_service.get_all_clients()
            
            # Convert to simplified client list format
            client_list = [
                ClientListItem(
                    name=client.get("name"),
                    email=client.get("email"),
                    package_type=client.get("package_type", ""),
                    active=True
                ).dict()
                for client in clients
            ]
            
            return jsonify({
                "status": "success",
                "clients": client_list
            }), 200
        
        except Exception as e:
            logger.error(f"Error fetching clients: {e}")
            return jsonify({"error": f"Failed to fetch clients: {str(e)}"}), 500
    
    # Success page
    @app.route("/success", methods=["GET"])
    def success_page():
        """Display success message."""
        form_type = request.args.get("type", "unknown")
        try:
            return render_template("success.html", form_type=form_type)
        except Exception as e:
            logger.error(f"Error rendering success page: {e}")
            return redirect(url_for("error_page", msg="Success page not available"))
    
    # Error page
    @app.route("/error", methods=["GET"])
    def error_page():
        """Display error message."""
        msg = request.args.get("msg", "An unexpected error occurred")
        try:
            return render_template("error.html", error_message=msg)
        except Exception as e:
            logger.error(f"Error rendering error page: {e}")
            return f"<h1>Error</h1><p>{msg}</p>", 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        logger.warning(f"404 error: {request.path}")
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"500 error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors."""
        logger.warning(f"400 error: {error}")
        return jsonify({"error": "Bad request"}), 400
    
    return app


if __name__ == "__main__":
    app = create_app()
    # Note: In production, use gunicorn instead of Flask development server
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=app.config.get("DEBUG", False)
    )
