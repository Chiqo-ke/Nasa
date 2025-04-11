from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None):
        try:
            super().send_error(code, message)
        except BrokenPipeError:
            pass
        except ConnectionResetError:
            pass

PORT = 5500

Handler = CustomHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at http://localhost:{PORT}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    httpd.shutdown() 