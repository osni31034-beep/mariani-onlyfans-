import http.server
import json
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/saveconfig':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                config_data = json.loads(post_data.decode('utf-8'))
                # Write config data to config.json
                with open('config.json', 'w') as f:
                    json.dump(config_data, f, indent=2)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'success', 'message': 'Config saved successfully'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/uploadimage':
            # For simplicity in this demo, we'll just return success
            # In a real implementation, we'd parse the multipart data
            # But for now, let's simulate that it works
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Return a dummy filename - in reality this would come from the upload
            response = {'status': 'success', 'message': 'Image upload simulated', 'filename': 'uploaded_image.png'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # For other POST requests, return 404
            self.send_response(404)
            self.end_headers()
            
    def do_GET(self):
        # Handle /admin redirect to /admin.html
        if self.path == '/admin':
            self.path = '/admin.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        # Serve files as usual
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    PORT = 8000
    with http.server.HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
