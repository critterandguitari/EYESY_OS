import subprocess
import os

def get_usb_device():
    devices = subprocess.getoutput("lsblk -o KNAME,TYPE | grep 'disk' | awk '{print $1}'").splitlines()
    for dev in devices:
        if "sd" in dev:  # Typical USB storage devices start with "sd"
            return f"/dev/{dev}1"  # Assuming first partition
    return None

def mount_usb():
    usb_device = get_usb_device()
    if not usb_device:
        print("No USB device found.")
        return False

    if not os.path.exists("/usbdrive"):
        os.makedirs("/usbdrive")

    if "/usbdrive" in subprocess.getoutput("mount"):
        print("USB already mounted.")
        return True

    result = subprocess.run(["sudo", "mount", "-o", "uid=1000,gid=1000", usb_device, "/usbdrive"],
                            capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Mounted {usb_device} at /usbdrive.")
        return True
    else:
        print(f"Mount failed: {result.stderr}")
        return False


