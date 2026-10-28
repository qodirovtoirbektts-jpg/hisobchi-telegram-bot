"""Root runner for Hisobchi Telegram Bot."""
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from bot.main import main


def start_health_server() -> None:
    """Optional health check server for hosting platforms like Render Web Service."""
    port_str = os.environ.get("PORT")
    if not port_str:
        return

    try:
        port = int(port_str)
    except ValueError:
        return

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Hisobchi Bot is running OK.")

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_health_server()
    asyncio.run(main())
