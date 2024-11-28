import ipaddress
import os
import sys

def read_ip_list_from_file(filename):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the full path to the file
    file_path = os.path.join(script_dir, filename)
    
    with open(file_path, 'r') as file:
        # Read lines and remove whitespace/empty lines
        return [line.strip() for line in file if line.strip()]

def convert_cidr_list_to_subnet(ip_cidr_list):
    results = []
    for ip_cidr in ip_cidr_list:
        # Check if the IP contains a subnet mask (/)
        if '/' not in ip_cidr:
            # If no subnet mask, only return the host IP format
            results.append((f"host {ip_cidr}",))
            continue
            
        network = ipaddress.ip_network(ip_cidr, strict=False)
        ip_address = str(network.network_address)
        subnet_mask = str(network.netmask)
        results.append((ip_address, subnet_mask))
    return results

def export_results(results, output_filename="converted_ips.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)
    
    with open(output_path, 'w') as file:
        for result in results:
            if isinstance(result, tuple) and len(result) == 1:
                file.write(f"{result[0]}\n")
            else:
                file.write(f"{result[0]} {result[1]}\n")
    return output_path

if __name__ == "__main__":
    try:
        ip_list = read_ip_list_from_file("ip_addresses.txt")
        results = convert_cidr_list_to_subnet(ip_list)
        
        # Print results
        print("\nConverted IP addresses:")
        print("-" * 40)
        for result in results:
            if isinstance(result, tuple) and len(result) == 1:
                print(result[0])
            else:
                print(f"{result[0]} {result[1]}")
        
        # Export results
        output_file = export_results(results)
        print(f"\nResults have been exported to: {output_file}")
        
        # Hold terminal
        print("\nPress Enter to exit...", end='')
        input()
        
    except FileNotFoundError:
        print("Error: ip_addresses.txt file not found")
        input("\nPress Enter to exit...")
    except ValueError as e:
        print(f"Error: Invalid IP address format - {e}")
        input("\nPress Enter to exit...")