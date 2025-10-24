#!/usr/bin/env python3
"""
BLE Characteristic Writer
Source: https://techoverflow.net/2025/08/04/python-script-to-write-ble-characteristics-using-bleak/

This script connects to a BLE device by MAC address and writes a specified value to a given characteristic UUID.

Requirements:
    - bleak library: pip install bleak

Usage:
    python write_ble_characteristic.py [MAC_ADDRESS] [CHARACTERISTIC_UUID] [VALUE] [--hex]

Example:
    python write_ble_characteristic.py 24:EC:4A:76:00:32 00002a37-0000-1000-8000-00805f9b34fb "Hello"
    python write_ble_characteristic.py 24:EC:4A:76:00:32 00002a37-0000-1000-8000-00805f9b34fb "48656c6c6f" --hex
"""

import asyncio
import sys
import argparse
from bleak import BleakClient
from bleak.exc import BleakError
from datetime import datetime

def parse_value(value_str, hex_mode):
    if hex_mode:
        # Convert hex string to bytes
        try:
            return bytes.fromhex(value_str)
        except ValueError:
            print(f"Invalid hex string: {value_str}")
            sys.exit(1)
    else:
        return value_str.encode("utf-8")

async def write_characteristic(mac_address, char_uuid, value_bytes):
    print(f"\nAttempting to connect to {mac_address} ...")
    try:
        async with BleakClient(mac_address) as client:
            if client.is_connected:
                print(f"Successfully connected to {mac_address}")
                print(f"Connected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Writing to characteristic {char_uuid} ...")
                try:
                    await client.write_gatt_char(char_uuid, value_bytes)
                    print(f"Successfully wrote value to characteristic {char_uuid}.")
                except Exception as e:
                    print(f"Failed to write value: {e}")
                    return False
                print(f"\nDisconnected from {mac_address}")
                return True
            else:
                print(f"Failed to connect to {mac_address}")
                return False
    except BleakError as e:
        print(f"Bluetooth error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

async def main():
    parser = argparse.ArgumentParser(description="Write a value to a BLE device characteristic.")
    parser.add_argument("mac_address", help="MAC address of the BLE device")
    parser.add_argument("char_uuid", help="Characteristic UUID to write to")
    parser.add_argument("value", help="Value to write (string or hex)")
    parser.add_argument("--hex", action="store_true", help="Interpret value as hex string")
    args = parser.parse_args()

    mac_address = args.mac_address
    char_uuid = args.char_uuid
    value_str = args.value
    hex_mode = args.hex

    print(f"Using MAC address: {mac_address}")
    print(f"Characteristic UUID: {char_uuid}")
    print(f"Value: {value_str} ({'hex' if hex_mode else 'utf-8'})")

    # Validate MAC address format (basic check)
    if len(mac_address.replace(":", "").replace("-", "")) != 12:
        print(f"Invalid MAC address format: {mac_address}")
        print("Expected format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX")
        return

    value_bytes = parse_value(value_str, hex_mode)
    success = await write_characteristic(mac_address, char_uuid, value_bytes)

    if success:
        print("\nWrite operation completed successfully.")
    else:
        print("\nWrite operation failed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
