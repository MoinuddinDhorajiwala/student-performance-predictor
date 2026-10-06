import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from predictor import predict_student

REQUIRED = [
    "Age", "Gender", "Class", "Study_Hours_Per_Day",
    "Attendance_Percentage", "Parental_Education",
    "Internet_Access", "Extracurricular_Activities",
    "Math_Score", "Science_Score", "English_Score",
    "Previous_Year_Score"
]

def response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        response(self, 204, {})

    def do_GET(self):
        response(self, 200, {
            "status": "ok",
            "message": "Student Performance Prediction API is running"
        })

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            missing = [c for c in REQUIRED if c not in data]
            if missing:
                response(self, 400, {"error": "Missing fields: " + ", ".join(missing)})
                return
            result = predict_student(data)
            response(self, 200, result)
        except Exception as exc:
            response(self, 400, {"error": str(exc)})

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    from http.server import HTTPServer
    HTTPServer(("127.0.0.1", 8000), handler).serve_forever()
