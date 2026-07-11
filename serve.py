import http.server
import socketserver
import webbrowser
import threading
import sys
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving TrackMyRun at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()

if __name__ == "__main__":
    print(f"Starting server in directory: {DIRECTORY}")
    
    # Start server in a background thread so we can handle browser open smoothly
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open default browser after a short delay
    threading.Event().wait(1.0)
    webbrowser.open(f"http://localhost:{PORT}")
    
    try:
        # Keep main thread alive
        while True:
            threading.Event().wait(1.0)
    except KeyboardInterrupt:
        print("\nShutting down TrackMyRun server. Goodbye!")
        sys.exit(0)
