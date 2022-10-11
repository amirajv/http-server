#!/usr/bin/env python3

import os
import argparse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


class RequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # redirect requests to static files to the right place
        path = super().translate_path(path)
        if "/static/" in path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current_dir, "static", path.split("/static/")[1])
        return path

    def end_headers(self):
        # disable browser cache
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def run(addr="localhost", port=8000):
    server = ThreadingHTTPServer((addr, port), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a HTTP server.')
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()

    HOST = args.listen
    PORT = args.port
    DIRECTORY = os.getcwd()

    print(f"Serving HTTP traffic from {DIRECTORY} on {HOST}:{PORT}")
    run(addr=HOST, port=PORT)
