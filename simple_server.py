"""Ultra-simple HTTP server - no dependencies."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/" or self.path == "/form/new-client":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = b"""<!DOCTYPE html>
<html>
<head>
    <title>Coaching Portal</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        input, select { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 12px; border: none; cursor: pointer; border-radius: 4px; width: 100%; font-size: 16px; }
        button:hover { background: #0056b3; }
        .success { color: green; margin-top: 20px; }
        .error { color: red; margin-top: 20px; }
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
                    '<p class="success">SUCCESS: ' + result.message + '</p>';
            } catch (err) {
                document.getElementById('result').innerHTML = 
                    '<p class="error">ERROR: ' + err.message + '</p>';
            }
        });
    </script>
</body>
</html>"""
            self.wfile.write(html)
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/api/clients/new":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "success", "message": "Client registered successfully!"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"[{self.address_string()}] {format % args}")

if __name__ == "__main__":
    PORT = 3000
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print("\n" + "="*60)
    print("COACHING PORTAL - SIMPLE HTTP SERVER")
    print("="*60)
    print(f"\nServer running on port {PORT}")
    print(f"\nOpen in your browser:")
    print(f"  http://127.0.0.1:{PORT}/")
    print(f"  http://192.168.3.144:{PORT}/")
    print(f"\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()
