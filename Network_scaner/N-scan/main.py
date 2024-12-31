from scanner.host_discovery import discover_hosts
from scanner.port_scanner import scan_ports
from scanner.service_detector import detect_service
import argparse

def main():
    parser = argparse.ArgumentParser(description="Network Scanner Tool")
    parser.add_argument('-t', '--target', type=str, required=True, help="Target IP or subnet (e.g., 192.168.1.0/24)")
    parser.add_argument('-p', '--ports', type=str, default="1-1024", help="Port range to scan (e.g., 1-65535)")
    args = parser.parse_args()

    target = args.target
    port_range = args.ports

    print(f"Scanning target: {target} on ports: {port_range}")
    active_hosts = discover_hosts(target)
    print(f"Discovered active hosts: {active_hosts}")

    for host in active_hosts:
        print(f"\nScanning host: {host}")
        open_ports = scan_ports(host, port_range)
        print(f"Open ports on {host}: {open_ports}")

        for port in open_ports:
            service = detect_service(host, port)
            print(f"Port {port}: {service}")

if __name__ == "__main__":
    main()