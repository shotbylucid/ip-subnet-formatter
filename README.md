# IP Subnet Converter

A Python utility for converting IP addresses and CIDR notations to subnet mask format.

## Overview

This tool reads IP addresses from a text file and converts them into appropriate subnet mask notation. It handles both individual IP addresses (host format) and CIDR notation, making it useful for network configuration and firewall rule management.

## Features

- Converts CIDR notation to IP address and subnet mask pairs
- Handles individual IP addresses in host format
- Reads input from a text file
- Robust error handling for invalid IP formats
- Supports both IPv4 and IPv6 addresses

## Prerequisites

- Python 3.x
- `ipaddress` module (included in Python standard library)

## Usage

1. Create a text file named `ip_addresses.txt` in the same directory as the script
2. Add IP addresses or CIDR notations, one per line:
   ```
   192.168.1.1
   10.0.0.0/24
   172.16.0.0/16
   ```
3. Run the script:
   ```bash
   python ip_subnet_converter.py
   ```
4. The script will:
   - Display the converted IP addresses in the terminal
   - Export results to `converted_ips.txt` in the same directory
   - Wait for user input before closing

### Output Format

- For CIDR notation (e.g., "10.0.0.0/24"):
  ```
  10.0.0.0 255.255.255.0
  ```
- For single IP addresses:
  ```
  host 192.168.1.1
  ```

## Error Handling

The script includes error handling for:
- Missing input file
- Invalid IP address formats
- Malformed CIDR notation

## License

[Add appropriate license information here]