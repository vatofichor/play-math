import http.server
import socketserver
import webbrowser
import threading
import sys
import os
import json

PORT = 8090
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

MANIFEST_PATH = os.path.join(DIRECTORY, "manifest.json")

def load_manifest():
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading manifest: {e}")
        return {"domains": {}, "subtopic_names": {}}

MANIFEST = load_manifest()

def format_subtopic_name(name):
    subtopic_names = MANIFEST.get("subtopic_names", {})
    if name.lower() in subtopic_names:
        return subtopic_names[name.lower()]
        
    words = name.replace('_', ' ').split()
    formatted = []
    for w in words:
        if w.lower() in ('and', 'of', 'by', 'with', 'to', 'for'):
            formatted.append(w.lower())
        else:
            formatted.append(w.capitalize())
    if formatted:
        formatted[0] = formatted[0].capitalize()
    return ' '.join(formatted)

def get_roadmap_data():
    data = {}
    content_dir = os.path.join(DIRECTORY, "content")
    if not os.path.exists(content_dir):
        return data
    
    entries = sorted(os.listdir(content_dir))
    for entry in entries:
        entry_path = os.path.join(content_dir, entry)
        if os.path.isdir(entry_path) and entry[0:2].isdigit() and '_' in entry:
            subtopics = []
            sub_entries = sorted(os.listdir(entry_path))
            for sub in sub_entries:
                sub_path = os.path.join(entry_path, sub)
                if os.path.isdir(sub_path):
                    is_live = os.path.exists(os.path.join(sub_path, 'index.html'))
                    subtopics.append({
                        "id": sub,
                        "name": format_subtopic_name(sub),
                        "live": is_live,
                        "path": f"/{entry}/{sub}/index.html" if is_live else None
                    })
            data[entry] = subtopics
    return data

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        path_map = {
            '/arithmetic': '/content/01_arithmetic_number_sense/index.html',
            '/algebra': '/content/02_algebra/index.html',
            '/geometry': '/content/03_geometry_measurement/index.html',
            '/trig': '/content/04_trigonometry/index.html',
            '/calculus': '/content/05_calculus/index.html',
            '/data': '/content/06_data_science_statistics/index.html',
            '/compmath': '/content/07_computational_math/index.html',
            '/tags': '/content/tags/index.html'
        }

        path_part = self.path.split('?')[0].split('#')[0].rstrip('/')

        if self.path == '/api/roadmap':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            data = get_roadmap_data()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif path_part in path_map:
            suffix = ''
            if '?' in self.path:
                suffix = '?' + self.path.split('?', 1)[1]
            elif '#' in self.path:
                suffix = '#' + self.path.split('#', 1)[1]
            self.path = path_map[path_part] + suffix
            super().do_GET()
        elif self.path.startswith('/0') and '_' in self.path:
            path_part_0 = self.path.split('?')[0].split('#')[0]
            local_path = os.path.join(DIRECTORY, "content", path_part_0.lstrip('/'))
            
            if os.path.isdir(local_path) and not self.path.endswith('/'):
                self.send_response(301)
                new_path = self.path + '/'
                self.send_header('Location', new_path)
                self.end_headers()
                return
                
            self.path = '/content' + self.path
            super().do_GET()
        else:
            super().do_GET()

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n========================================================")
        print(f" [Roadmap] Mathematics Mastery Roadmap Server Started!")
        print(f" Serving Roadmap from: {DIRECTORY}")
        print(f" Local Address:        http://localhost:{PORT}")
        print(f" Press Ctrl+C to shut down the server.")
        print(f"========================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Test syntax check passed.")
        sys.exit(0)
        
    threading.Timer(0.8, open_browser).start()
    run_server()
