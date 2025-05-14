#
# import ipaddress
# import subprocess
# import platform
# import concurrent.futures
#
#
#
#
#
#
#
# class SearchIpAddressView:
#     def __init__(self):
#
#
#
#
#     # Kompyuter OS'ga qarab ping buyruq tanlash
#     def ping(ip):
#         param = "-n" if platform.system().lower() == "windows" else "-c"
#         command = ["ping", param, "1", str(ip)]
#         try:
#             result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
#             if result.returncode == 0:
#                 return str(ip)
#         except:
#             return None
#         return None
#     # Subnet ichidagi IP'larni topish
#     def scan_subnet(subnet_str):
#         print(f"{subnet_str} tarmog'i ichidagi faol IP'lar:")
#         active_ips = []
#         subnet = ipaddress.ip_network(subnet_str, strict=False)
#
#         with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#             futures = {executor.submit(ping, ip): ip for ip in subnet.hosts()}
#
#             for future in concurrent.futures.as_completed(futures):
#                 ip = future.result()
#                 if ip:
#                     print(f"Faol: {ip}")
#                     active_ips.append(ip)
#
#         return active_ips


import ipaddress
import subprocess
import platform
import concurrent.futures


# Kompyuter OS'ga qarab ping buyruq tanlash
def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", str(ip)]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        if result.returncode == 0:
            return str(ip)
    except:
        return None
    return None


# Subnet ichidagi IP'larni topish
def scan_subnet(subnet_str):
    print(f"{subnet_str} tarmog'i ichidagi faol IP'lar:")
    active_ips = []
    subnet = ipaddress.ip_network(subnet_str, strict=False)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(ping, ip): ip for ip in subnet.hosts()}

        for future in concurrent.futures.as_completed(futures):
            ip = future.result()
            if ip:
                print(f"Faol: {ip}")
                active_ips.append(ip)

    return active_ips


if __name__ == "__main__":
    subnet_input = "192.168.100.0/24"  # Siz kiritmoqchi bo'lgan subnet
    scan_subnet(subnet_input)
