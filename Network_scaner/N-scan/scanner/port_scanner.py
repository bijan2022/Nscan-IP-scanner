import socket

def scan_ports(host, port_range):
    """
    Scan ports in the given range on a target host.
    """
    start_port, end_port = map(int, port_range.split('-'))
    open_ports = []

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((host, port)) == 0:
                    open_ports.append(port)
        except Exception as e:
            print(f"Error scanning port {port} on {host}: {e}")
    return open_ports