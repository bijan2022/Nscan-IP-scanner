from scapy.all import ARP, Ether, srp

def discover_hosts(target):
    """
    Discover active hosts in the given subnet using ARP requests.
    """
    try:
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target)
        result = srp(packet, timeout=2, verbose=False)[0]

        hosts = []
        for sent, received in result:
            hosts.append(received.psrc)

        #if not hosts:
            #print("not found hosts") #i will try found error . / Matius
        
        return hosts
    except Exception as e:
        print(f"Error discovering hosts: {e}")
        return []
    