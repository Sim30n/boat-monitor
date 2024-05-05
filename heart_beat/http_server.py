from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import threading
import time

# Global variable to track the last request time
last_request_time = None


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global last_request_time
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Update the last request time
        last_request_time = time.time()

        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Print timestamp to console
        print(f"Request received at: {timestamp}")

        # Respond with the timestamp
        self.wfile.write(f"Request received at: {timestamp}".encode('utf-8'))


def check_request_interval(interval):
    global last_request_time
    while True:
        if last_request_time is not None and time.time() - last_request_time > interval:
            print("No requests received within the specified interval")
        time.sleep(interval)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")

    # Start the thread to check request interval
    interval_check_thread = threading.Thread(target=check_request_interval, args=(60,)) # Check every 60 seconds
    interval_check_thread.daemon = True
    interval_check_thread.start()

    httpd.serve_forever()


if __name__ == '__main__':
    run()
