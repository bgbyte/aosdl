#!/usr/bin/env python3

import paramiko
from getpass import getpass
import time

def wait_for_shell(shell, timeout=120):
    """Read output from shell until timeout or prompt returns."""
    shell.settimeout(2)
    output = ""
    start = time.time()
    while time.time() - start < timeout:
        try:
            chunk = shell.recv(4096).decode("utf-8")
            output += chunk
            # Break if we detect shell prompt (e.g., ending in # or $)
            if any(p in chunk for p in ["# ", "#->", "$ ", ">", "login: "]):
                break
        except Exception:
            time.sleep(1)
    return output

# Step 1: Get AOS version info
aos_major = input("Enter AOS Major Version (e.g., 8.9) [8.9]: ") or "8.9"
aos_build = input("Enter AOS Build Number (e.g., 221) [221]: ") or "221"
aos_release = input("Enter AOS Release (e.g., R03) [R03]: ") or "R03"

# Step 2: Get list of IPs with optional usernames and passwords
hosts = []
print("\nEnter device details. Press Enter without an IP to finish.")
while True:
    ip = input("Enter device IP: ").strip()
    if not ip:
        break
    username = input(f"Enter username for {ip} [admin]: ") or "admin"
    password = getpass(f"Enter password for {ip} [switch]: ") or "switch"
    hosts.append({"ip": ip, "username": username, "password": password})

# Image mapping
image_map = {
    "nandi_sim": ["Nossim.img"],
    "everest": ["Uos.img"],
    "medora_sim64": ["Mossim.img", "Menisim.img"],
    "tor": ["Tos.img"],
    "vindhya": ["Nos.img"],
    "medora": ["Mos.img", "Meni.img", "Mhost.img"],
    "yukon": ["Yos.img"],
    "shasta": ["Uos.img"],
    "aravalli": ["Nosa.img"],
    "shasta_n": ["Uosn.img"],
    "whitney": ["Wos.img"],
    "nandi": ["Nos.img"],
    "whitney_sim": ["Wossim.img"]
}

# Constants
base_ip = "http://10.46.4.37"
base_dir = "/bop/images"
aos_major_fmt = aos_major.replace('.', '_')

# Step 3: Iterate over each host
for host in hosts:
    ip = host["ip"]
    print(f"\nConnecting to {ip}...")

    try:
        # Connect via SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=host["username"], password=host["password"], timeout=10)

        shell = client.invoke_shell()
        shell.send("su\n")
        time.sleep(1)
        shell.recv(1024)  # No password needed
        shell.send("echo $PS1\n")
        time.sleep(1)
        output = shell.recv(2048).decode("utf-8")
        

        lines = output.strip().splitlines()
        ps1 = lines[-1] if lines else ""
        family = ps1.split()[0].lower() if ps1 else None

        if not family or family not in image_map:
            print(f"[{ip}] Unknown or missing platform family: '{family}'")
            client.close()
            continue

        print(f"[{ip}] Platform family: {family}")
        images = image_map[family]
        image_path = f"{base_dir}/OS_{aos_major_fmt}_{aos_build}_{aos_release}/{family}/Release/"

        for img in images:
            url = f"{base_ip}{image_path}{img}"
            cmd = f"curl -kL \"{url}\" --output /flash/{img}"
            shell.send(cmd + "\n")
            print(f"[{ip}] Downloading {img}...")
            download_output = wait_for_shell(shell)
            print(f"[{ip}] Downloaded {img} to /flash/")

        client.close()

    except Exception as e:
        print(f"[{ip}] ERROR: {e}")
