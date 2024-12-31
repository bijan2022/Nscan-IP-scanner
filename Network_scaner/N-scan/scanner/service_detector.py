import socket

def detect_service(host, port):
    """
    Detect the service running on a specific port.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            banner = s.recv(1024).decode().strip()
            return banner if banner else "Unknown service"
    except Exception:
        return "Unknown service"