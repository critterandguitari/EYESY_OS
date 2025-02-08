import subprocess
import re

CMDLINE_PATH = "/boot/firmware/cmdline.txt"
TV_NORM_PREFIX = "vc4.tv_norm="

def get_tv_norm():
    # Extract the current tv_norm value from cmdline.txt.
    try:
        with open(CMDLINE_PATH, "r") as f:
            match = re.search(rf"{TV_NORM_PREFIX}(\S+)", f.read())
            if match:
                return match.group(1)  # Return value after vc4.tv_norm=
    except FileNotFoundError:
        pass
    return "NTSC"  # Default if not found (though we assume it's always there)

def set_tv_norm(mode):
    # Replace the existing vc4.tv_norm= value with a new mode in cmdline.txt.
    try:
        subprocess.run(
            f"sudo sed -i 's/{TV_NORM_PREFIX}\\S\\+/{TV_NORM_PREFIX}{mode}/' {CMDLINE_PATH}",
            shell=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error modifying {CMDLINE_PATH}: {e}")

