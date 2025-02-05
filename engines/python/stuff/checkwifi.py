import subprocess

def check_wifi_adapter():
    try:
        output = subprocess.check_output(["nmcli", "device"], text=True)
        return any("wifi" in line for line in output.splitlines())
    except subprocess.CalledProcessError:
        return False  # nmcli failed, assume no adapter

if __name__ == "__main__":
    if check_wifi_adapter():
        print("Wi-Fi adapter found.")
    else:
        print("No Wi-Fi adapter detected!")

