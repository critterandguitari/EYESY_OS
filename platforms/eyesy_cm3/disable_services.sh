#!/bin/bash
# disable-unwanted-services.sh
# This script disables and masks services that are not needed for the EYESY device.
# Masking prevents any accidental or dependency-based activation.

# List of unwanted services:
SERVICES=(
    "apparmor.service"
    "rpi-eeprom-update.service"
    "ModemManager.service"
    "console-setup.service"
    "keyboard-setup.service"
    "rpi-display-backlight.service"
    "glamor-test.service"
    "cron.service"
    "dphys-swapfile.service"
    "rp1-test.service"
    "NetworkManager-wait-online.service"
    "e2scrub_reap.service"
    "raspi-config.service"
    "apt-daily-upgrade.service"
    "systemd-random-seed.service"
    "systemd-journal-flush"
    "getty@tty1.service"
    "avahi-daemon"
)

# Loop through each service to disable and mask it.
for SERVICE in "${SERVICES[@]}"; do
    echo "Disabling ${SERVICE}..."
    sudo systemctl disable "${SERVICE}" || echo "Failed to disable ${SERVICE}"
    
    echo "Stopping ${SERVICE} if running..."
    sudo systemctl stop "${SERVICE}" || echo "${SERVICE} was not running"
    
    echo "Masking ${SERVICE}..."
    sudo systemctl mask "${SERVICE}" || echo "Failed to mask ${SERVICE}"
    
    echo "--------------------------------------"
done

echo "All unwanted services have been disabled and masked."
