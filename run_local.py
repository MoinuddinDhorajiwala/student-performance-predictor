from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys
import json
import os

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from predictor import predict_student


class AppHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/api":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(
                self.rfile.read(length).decode("utf-8")
            )

            result = predict_student(data)

            body = json.dumps(result).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        except Exception as exc:
            body = json.dumps({
                "error": str(exc)
            }).encode("utf-8")

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api":
            body = json.dumps({
                "status": "ok",
                "message": "Student Performance Prediction API is running"
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)
            return

        super().do_GET()


# Serve files from the project folder
os.chdir(ROOT)

# Use port 8080 instead of 8000
PORT = 8080

server = ThreadingHTTPServer(
    ("127.0.0.1", PORT),
    AppHandler
)

print(f"Open http://127.0.0.1:{PORT}")
print("Press Ctrl+C to stop the server.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
finally:
    server.server_close()