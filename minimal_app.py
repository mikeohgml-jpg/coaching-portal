"""Minimal stable Flask app - Pure HTML strings, no templates."""

import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-key'

# Demo data
demo_clients = [
    {"name": "John Doe", "email": "john@example.com", "package_type": "Standard"},
    {"name": "Jane Smith", "email": "jane@example.com", "package_type": "Premium"},
]

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Coaching Portal - Demo</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        input, select { width: 100%; padding: 8px; margin: 5px 0 15px; border: 1px solid #ccc; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Register New Client</h2>
        <form id="form">
            <label>Full Name *</label>
            <input type="text" name="name" required>
            
            <label>Email *</label>
            <input type="email" name="email" required>
            
            <label>Package Type *</label>
            <select name="package_type" required>
                <option>Select...</option>
                <option>Starter</option>
                <option>Standard</option>
                <option>Premium</option>
            </select>
            
            <label>Start Date *</label>
            <input type="date" name="start_date" required>
            
            <label>End Date *</label>
            <input type="date" name="end_date" required>
            
            <label>Amount Paid ($) *</label>
            <input type="number" name="amount_paid" step="0.01" required>
            
            <button type="submit">Register Client</button>
        </form>
        <div id="result"></div>
    </div>
    
    <script>
        document.getElementById('form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const res = await fetch('/api/clients/new', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                document.getElementById('result').innerHTML = 
                    '<p style="color: green; margin-top: 20px;">SUCCESS: ' + result.message + '</p>';
            } catch (err) {
                document.getElementById('result').innerHTML = 
                    '<p style="color: red; margin-top: 20px;">ERROR: ' + err.message + '</p>';
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    """Home page."""
    return HTML_FORM, 200

@app.route("/form/new-client", methods=["GET"])
def new_client():
    """New client form."""
    return HTML_FORM, 200

@app.route("/api/clients/new", methods=["POST"])
def register_client():
    """Register new client."""
    try:
        data = request.get_json()
        demo_clients.append(data)
        logger.info(f"Client registered: {data.get('name')}")
        return jsonify({"status": "success", "message": "Client registered!"}), 201
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/clients", methods=["GET"])
def get_clients():
    """Get clients."""
    return jsonify({"clients": demo_clients}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    PORT = 3000
    print("\n" + "="*50)
    print("COACHING PORTAL - STABLE DEMO")
    print("="*50)
    print(f"\nServer running on ALL interfaces on port {PORT}")
    print("Open in your browser:")
    print(f"  - Local:   http://127.0.0.1:{PORT}/")
    print(f"  - Network: http://192.168.3.144:{PORT}/")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False, threaded=True)
