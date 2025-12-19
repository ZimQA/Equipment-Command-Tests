from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockAPI(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Body запроса
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        request = json.loads(body)
        
        # Негативный тест: пустой device_id -> 400
        if not request.get('device_id') or request['device_id'].strip() == '':
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "device_id cannot be empty"}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Позитивный тест
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"id": "cmd-test-123", "status": "NEW"}
        self.wfile.write(json.dumps(response).encode())
    
    def do_GET(self):
        # Всегда SUCCESS для polling
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"id": "cmd-test-123", "status": "SUCCESS", "result": "OK"}
        self.wfile.write(json.dumps(response).encode())

# Запуск сервера
server = HTTPServer(('localhost', 8080), MockAPI)
print("Mock running: http://localhost:8080")
print("POST /api/commands - создание команды")
print("GET  /api/commands/{id} - статус команды")
server.serve_forever()