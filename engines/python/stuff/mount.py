import os
import subprocess

MOUNT_POINT = "/usbdrive"

def get_usb_device():
    """Find the first USB storage device."""
    devices = subprocess.getoutput("lsblk -o KNAME,TYPE | grep 'disk' | awk '{print $1}'").splitlines()
    for dev in devices:
        if "sd" in dev:  # Typical USB storage devices start with "sd"
            return f"/dev/{dev}1"  # Assuming first partition
    return None

def is_mounted(mount_point):
    """Check if the USB drive is already mounted."""
    return mount_point in subprocess.getoutput("mount")

def mount_usb():
    """Mount the USB drive with proper permissions."""
    if not os.path.exists(MOUNT_POINT):
        os.makedirs(MOUNT_POINT)

    usb_device = get_usb_device()
    if usb_device and not is_mounted(MOUNT_POINT):
        result = subprocess.run(
            ["sudo", "mount", "-o", "uid=1000,gid=1000", usb_device, MOUNT_POINT],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Mounted {usb_device} at {MOUNT_POINT}")
        else:
            print(f"Mount failed: {result.stderr}")
    else:
        print("No USB drive found or already mounted.")


if __name__ == "__main__":
    mount_usb()

