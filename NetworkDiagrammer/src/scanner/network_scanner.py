
import nmap
import scapy.all as scapy
from dataclasses import dataclass
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import socket

@dataclass
class DeviceInfo:
    ip_address: str
    mac_address: str
    hostname: str
    os_type: str
    open_ports: List[int]
    services: Dict[int, str]

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        
    def scan_network(self, ip_range: str) -> List[DeviceInfo]:
        devices = []
        try:
            # ARP scan for live hosts
            arp_request = scapy.ARP(pdst=ip_range)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            
            # Use ThreadPoolExecutor for parallel scanning
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for element in answered_list:
                    futures.append(executor.submit(self.get_device_details, element[1].psrc))
                
                for future in futures:
                    if future.result():
                        devices.append(future.result())
                        
            return devices
            
        except Exception as e:
            print(f"Scan error: {e}")
            return devices

    def get_device_details(self, ip: str) -> DeviceInfo:
        try:
            # Perform detailed scan
            self.nm.scan(ip, arguments='-sS -sV -O --version-intensity 5')
            
            # Get device information
            hostname = socket.gethostbyaddr(ip)[0] if socket.gethostbyaddr(ip) else 'Unknown'
            os_match = self.nm[ip].get('osmatch', [{'name': 'Unknown'}])[0]['name']
            open_ports = list(self.nm[ip]['tcp'].keys()) if 'tcp' in self.nm[ip] else []
            services = {
                port: self.nm[ip]['tcp'][port]['name'] 
                for port in open_ports
            }
            
            return DeviceInfo(
                ip_address=ip,
                mac_address=self.get_mac(ip),
                hostname=hostname,
                os_type=os_match,
                open_ports=open_ports,
                services=services
            )
            
        except Exception as e:
            print(f"Error scanning {ip}: {e}")
            return None

    def get_mac(self, ip: str) -> str:
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            return answered_list[0][1].hwsrc if answered_list else "Unknown"
        except:
            return "Unknown"
