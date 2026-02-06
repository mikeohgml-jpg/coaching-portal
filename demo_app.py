"""Demo Flask app - Stable version without external dependencies."""

import logging
from flask import Flask, render_template, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

app.config['SECRET_KEY'] = 'demo-secret-key'

# In-memory demo data
demo_clients = [
    {"name": "John Doe", "email": "john@example.com", "package_type": "Standard"},
    {"name": "Jane Smith", "email": "jane@example.com", "package_type": "Premium"},
]

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Coaching Portal Demo - Ready to Use"
    }), 200

@app.route("/form/new-client", methods=["GET"])
def new_client_form():
    """Display new client registration form."""
    try:
        return render_template("new_client_form.html")
    except Exception as e:
        logger.error(f"Error rendering new client form: {e}")
        return f"Error: {str(e)}", 500

@app.route("/form/existing-client", methods=["GET"])
def existing_client_form():
    """Display existing client form."""
    try:
        return render_template("existing_client_form.html")
    except Exception as e:
        logger.error(f"Error rendering existing client form: {e}")
        return f"Error: {str(e)}", 500

@app.route("/api/clients", methods=["GET"])
def get_all_clients():
    """Get all clients - demo version."""
    try:
        return jsonify({
            "status": "success",
            "clients": demo_clients
        }), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/clients/new", methods=["POST"])
def submit_new_client():
    """Register new client - demo version."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add to demo data
        demo_clients.append({
            "name": data.get("name"),
            "email": data.get("email"),
            "package_type": data.get("package_type")
        })
        
        logger.info(f"New client registered: {data.get('name')}")
        return jsonify({
            "status": "success",
            "message": "Client registered successfully (DEMO MODE)",
            "data": data
        }), 201
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/clients/existing-session", methods=["POST"])
def submit_existing_client_session():
    """Record session - demo version."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        logger.info(f"Session recorded for: {data.get('client_name')}")
        return jsonify({
            "status": "success",
            "message": "Session recorded successfully (DEMO MODE)",
            "data": data
        }), 201
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/success", methods=["GET"])
def success_page():
    """Success page."""
    return render_template("success.html", form_type="demo"), 200

@app.route("/error", methods=["GET"])
def error_page():
    """Error page."""
    return render_template("error.html", error_message="Demo error"), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("\n" + "="*60)
    print("COACHING PORTAL - DEMO MODE")
    print("="*60)
    print("\nServer starting on http://127.0.0.1:5000")
    print("\nEndpoints:")
    print("  GET  http://127.0.0.1:5000/                - Health check")
    print("  GET  http://127.0.0.1:5000/form/new-client - Registration form")
    print("  GET  http://127.0.0.1:5000/form/existing-client - Session form")
    print("\n" + "="*60 + "\n")
    
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
