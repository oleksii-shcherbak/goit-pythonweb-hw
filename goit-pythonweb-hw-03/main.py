import json
import mimetypes
import pathlib
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, FileSystemLoader

BASE_DIR = pathlib.Path(__file__).parent
STORAGE_FILE = BASE_DIR / "storage" / "data.json"
TEMPLATES_DIR = BASE_DIR / "templates"

jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def read_storage() -> dict:
    if not STORAGE_FILE.exists():
        return {}
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_storage(data: dict) -> None:
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.send_read_page()
        elif pathlib.Path().joinpath(pr_url.path[1:]).exists():
            self.send_static()
        else:
            self.send_html_file("error.html", 404)

    def do_POST(self):
        if self.path == "/message":
            data = self.rfile.read(int(self.headers["Content-Length"]))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {
                key: value
                for key, value in [el.split("=") for el in data_parse.split("&")]
            }

            timestamp = str(datetime.now())
            storage = read_storage()
            storage[timestamp] = {
                "username": data_dict.get("username", ""),
                "message": data_dict.get("message", ""),
            }
            write_storage(storage)

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_html_file("error.html", 404)

    def send_html_file(self, filename: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(BASE_DIR / filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self) -> None:
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def send_read_page(self) -> None:
        messages = read_storage()
        template = jinja_env.get_template("read.html")
        rendered = template.render(messages=messages)
        encoded = rendered.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    print("Server started at http://localhost:3000")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
