"""Main Flask application for Coaching Portal."""

import logging
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from functools import wraps

from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'coaching123')

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


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
    
    # Set secret key for sessions
    app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-change-me')
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    
    # Lazy initialize services
    sheets_service = None
    email_service = None
    ai_service = None
    client_service = None
    
    try:
        from services.google_sheets_service import GoogleSheetsService
        from services.email_service import EmailService
        from services.ai_service import AIService
        from services.client_service import ClientService
        
        sheets_service = GoogleSheetsService()
        email_service = EmailService()
        ai_service = AIService()
        client_service = ClientService(sheets_service, email_service, ai_service)
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.warning(f"Services not available: {e}")
    
    # ===== ROUTES =====
    
    @app.route("/", methods=["GET"])
    def home():
        """Redirect to login or dashboard."""
        if 'user_logged_in' in session:
            return redirect(url_for('new_client_form'))
        return redirect(url_for('login_page'))
    
    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        """Login page."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['user_logged_in'] = True
                session['username'] = username
                return redirect(url_for('new_client_form'))
            else:
                return render_template('login.html', error="Invalid credentials")
        
        return render_template('login.html')
    
    @app.route("/logout")
    def logout():
        """Logout."""
        session.clear()
        return redirect(url_for('login_page'))
    
    @app.route("/form/new-client", methods=["GET"])
    @login_required
    def new_client_form():
        """Display form for new client registration."""
        try:
            return render_template("new_client_form.html")
        except Exception as e:
            logger.error(f"Error rendering new client form: {e}")
            return f"Error: {str(e)}", 500
    
    @app.route("/form/existing-client", methods=["GET"])
    @login_required
    def existing_client_form():
        """Display form for existing client session."""
        try:
            return render_template("existing_client_form.html")
        except Exception as e:
            logger.error(f"Error rendering existing client form: {e}")
            return f"Error: {str(e)}", 500
    
    @app.route("/success", methods=["GET"])
    @login_required
    def success_page():
        """Display success page after form submission."""
        form_type = request.args.get('type', 'default')
        return render_template("success.html", form_type=form_type)
    
    @app.route("/api/clients", methods=["GET"])
    @login_required
    def get_all_clients():
        """Get all clients."""
        if not sheets_service:
            return jsonify({"error": "Service not available"}), 503
        try:
            clients = sheets_service.get_all_clients()
            return jsonify({"status": "success", "clients": clients}), 200
        except Exception as e:
            logger.error(f"Error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/clients/new", methods=["POST"])
    @login_required
    def submit_new_client():
        """Process new client registration."""
        try:
            from models import NewClientFormData
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            form_data = NewClientFormData(**data)
            
            if not client_service:
                return jsonify({"error": "Service not available"}), 503
            
            result = client_service.process_new_client_registration(form_data)
            return jsonify(result), 201
        except Exception as e:
            logger.error(f"Error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/clients/existing-session", methods=["POST"])
    @login_required
    def submit_existing_client_session():
        """Process existing client session."""
        try:
            from models import ExistingClientFormData
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            form_data = ExistingClientFormData(**data)
            
            if not client_service:
                return jsonify({"error": "Service not available"}), 503
            
            result = client_service.process_existing_client_session(form_data)
            return jsonify(result), 201
        except Exception as e:
            logger.error(f"Error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/clients/<string:client_name>/balance", methods=["GET"])
    @login_required
    def get_client_balance(client_name):
        """Get client balance information."""
        if not client_service or not sheets_service:
            return jsonify({"error": "Service not available"}), 503
        try:
            client = sheets_service.get_client_by_name(client_name)
            if not client:
                return jsonify({"error": "Client not found"}), 404
            
            sessions = sheets_service.get_client_history(client_name)
            total_collected = sum(float(s.get('amount_collected', 0)) for s in sessions)
            total_package = float(client.get('amount_paid', 0))
            remaining = total_package - total_collected
            
            return jsonify({
                "status": "success",
                "total_package": total_package,
                "total_collected": total_collected,
                "remaining_balance": remaining
            }), 200
        except Exception as e:
            logger.error(f"Error getting client balance: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Server error"}), 500
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
