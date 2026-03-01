import http.server
import socketserver
import json
import webbrowser
import os

PORT = 8000
# This is the "Database" that lives while the server is running
market_data = []

class SyncedGridHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/market':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(market_data).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/market':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse the new energy listing
            new_entry = json.loads(post_data)
            market_data.insert(0, new_entry) # Put new items at the top
            
            self.send_response(201)
            self.end_headers()

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Allow port reuse so restarting is fast
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), SyncedGridHandler) as httpd:
        print("\n" + "="*50)
        print(f"🌿 NATURE-GRID SYNC SERVER ACTIVE")
        print(f"📡 API Hub: http://localhost:{PORT}")
        print(f"📊 Ready for multi-device P2P simulation.")
        print("="*50 + "\n")
        
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()