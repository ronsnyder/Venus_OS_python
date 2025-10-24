#!/usr/bin/env python3
"""
BLE Device Scanner
Source : https://techoverflow.net/2025/08/04/basic-script-to-list-ble-devices-in-python-using-bleak/

This script scans for and lists all available Bluetooth Low Energy (BLE) devices
in the vicinity. It displays device information including name, address, and RSSI.

Requirements:
    - bleak library: pip install bleak

Usage:
    python list_ble_devices.py
"""

import asyncio
import sys
from bleak import BleakScanner
from datetime import datetime


async def scan_ble_devices(scan_time=10):
    """
    Scan for BLE devices and return a list of discovered devices.

    Args:
        scan_time (int): Duration to scan in seconds (default: 10)

    Returns:
        list: List of BleakDevice objects
    """
    print(f"Scanning for BLE devices for {scan_time} seconds...")
    print("=" * 50)

    try:
        devices = await BleakScanner.discover(timeout=scan_time)
        return devices
    except Exception as e:
        print(f"Error during scanning: {e}")
        return []


def display_devices(devices):
    """
    Display the discovered BLE devices in a formatted table.

    Args:
        devices (list): List of BleakDevice objects
    """
    if not devices:
        print("No BLE devices found.")
        return

    print(f"Found {len(devices)} BLE device(s):")
    print("-" * 80)
    print(f"{'Name':<25} {'Address':<20} {'RSSI':<6} {'Services'}")
    print("-" * 80)

    for device in devices:
        name = device.name if device.name else "<Unknown>"
        address = device.address
        rssi = "N/A"
        if hasattr(device, 'metadata') and 'rssi' in device.metadata:
            rssi_val = device.metadata['rssi']
            rssi = f"{rssi_val} dBm" if rssi_val is not None else "N/A"

        # Get service UUIDs if available
        services = ""
        if hasattr(device, 'metadata') and 'uuids' in device.metadata:
            services = ', '.join(device.metadata['uuids'][:2])  # Show first 2 UUIDs
            if len(device.metadata['uuids']) > 2:
                services += "..."

        print(f"{name:<25} {address:<20} {rssi:<6} {services}")


async def main():
    """
    Main function to run the BLE device scanner.
    """
    print("BLE Device Scanner")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check if scan time is provided as command line argument
    scan_time = 10
    if len(sys.argv) > 1:
        try:
            scan_time = int(sys.argv[1])
            if scan_time <= 0:
                raise ValueError("Scan time must be positive")
        except ValueError as e:
            print(f"Invalid scan time: {e}")
            print("Using default scan time of 10 seconds")
            scan_time = 10

    # Perform the scan
    devices = await scan_ble_devices(scan_time)

    # Display results
    print()
    display_devices(devices)

    # Additional device details
    if devices:
        print()
        print("Additional device information:")
        print("-" * 50)
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device.name or '<Unknown>'} ({device.address})")
            metadata = getattr(device, 'metadata', None)
            if metadata:
                for key, value in metadata.items():
                    if key != 'uuids':  # uuids already shown above
                        print(f"   {key}: {value}")
            print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
