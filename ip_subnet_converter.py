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

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("IP/Subnet Converter - Main Menu")
    print("="*50)
    print("1. Convert IPs directly in CLI")
    print("2. Convert IPs from file (ip_addresses.txt)")
    print("3. Toggle 'Converted:' prefix (Currently: {})".format("ON" if show_prefix[0] else "OFF"))
    print("4. Toggle real-time output to file (Currently: {})".format("ON" if rt_output[0] else "OFF"))
    print("5. Exit")
    print("="*50)

def process_single_ip(ip_cidr):
    """Process a single IP/CIDR input and return the formatted result"""
    results = convert_cidr_list_to_subnet([ip_cidr])
    result = results[0]
    if isinstance(result, tuple) and len(result) == 1:
        return result[0]
    return f"{result[0]} {result[1]}"

# Add these at the top of the file with other global variables
show_prefix = [True]  # Using list to make it mutable in all scopes
rt_output = [False]   # Using list to make it mutable in all scopes

def write_realtime_output(result):
    """Write result to real-time output file"""
    if rt_output[0]:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rt_output_path = os.path.join(script_dir, "rt_output.txt")
        with open(rt_output_path, 'a') as file:
            file.write(f"{result}\n")

def interactive_mode():
    """Handle interactive IP conversion mode"""
    print("\nEnter IP addresses (one per line). Type 'done' to finish or 'exit' to quit completely.")
    print("For batch input, use square brackets and comma separation:")
    print("Example: [192.168.1.0/24, 10.0.0.1, 172.16.0.0/16]")
    
    # Clear rt_output.txt if real-time output is enabled
    if rt_output[0]:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rt_output_path = os.path.join(script_dir, "rt_output.txt")
        with open(rt_output_path, 'w') as file:
            file.write("")  # Clear the file
    
    results = []
    while True:
        try:
            ip_input = input("\nEnter IP address or CIDR: ").strip()
            
            if ip_input.lower() == 'exit':
                sys.exit(0)
            if ip_input.lower() == 'done':
                break
            if not ip_input:
                continue
            
            # Check for batch input
            if ip_input.startswith('[') and ip_input.endswith(']'):
                batch_ips = [ip.strip() for ip in ip_input[1:-1].split(',')]
                for ip in batch_ips:
                    try:
                        result = process_single_ip(ip)
                        if show_prefix[0]:
                            print(f"Converted: {result}")
                        else:
                            print(result)
                        results.append(result)
                        write_realtime_output(result)
                    except ValueError as e:
                        print(f"Error with IP {ip}: {e}")
            else:
                result = process_single_ip(ip_input)
                if show_prefix[0]:
                    print(f"Converted: {result}")
                else:
                    print(result)
                results.append(result)
                write_realtime_output(result)
            
        except ValueError as e:
            print(f"Error: Invalid IP format - {e}")
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            break
    
    return results

def main_menu():
    """Handle the main menu logic"""
    while True:
        display_menu()
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                results = interactive_mode()
                if results:
                    print("\nConverted IP addresses:")
                    print("-" * 40)
                    for result in results:
                        if isinstance(result, tuple) and len(result) == 1:
                            print(result[0])
                        else:
                            print(f"{result[0]} {result[1]}")
                    
                    save = input("\nWould you like to save the results? (y/n): ").lower()
                    if save == 'y':
                        output_file = export_results(results)
                        print(f"\nResults have been exported to: {output_file}")
            
            elif choice == '2':
                try:
                    ip_list = read_ip_list_from_file("ip_addresses.txt")
                    results = convert_cidr_list_to_subnet(ip_list)
                    
                    print("\nConverted IP addresses:")
                    print("-" * 40)
                    for result in rbesults:
                        if isinstance(result, tuple) and len(result) == 1:
                            print(result[0])
                        else:
                            print(f"{result[0]} {result[1]}")
                    
                    output_file = export_results(results)
                    print(f"\nResults have been exported to: {output_file}")
                
                except FileNotFoundError:
                    print("\nError: ip_addresses.txt file not found")
                except ValueError as e:
                    print(f"\nError: Invalid IP address format - {e}")
            
            elif choice == '3':
                show_prefix[0] = not show_prefix[0]
                print(f"\n'Converted:' prefix is now {'ON' if show_prefix[0] else 'OFF'}")
            
            elif choice == '4':
                rt_output[0] = not rt_output[0]
                print(f"\nReal-time output to file is now {'ON' if rt_output[0] else 'OFF'}")
                if rt_output[0]:
                    print("Results will be written to rt_output.txt in real-time")
            
            elif choice == '5':
                print("\nGoodbye!")
                break
            
            else:
                print("\nInvalid choice. Please enter 1-5.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        input("\nPress Enter to exit...")

# -------------------------------------------------------------------------------------------------
# To Do:
# - Add a function to clear the rt_output.txt file when the program starts and move to archive folder
# - Add a function to clear terminal output when new input is entered and after user confirms use of output, ie. clear the screen after 'Enter IP address or CIDR: and outputted results'
# - Add a local file to store settings such as 'show_prefix' and 'rt_output' and potentially other preferences, such as 'last_run_date' and 'rt_output_path and ip_addresses_path and output_path'
# - Add a function to load settings from the local file and apply them when the program starts
# ------------------------------------------------------------------------------------------------- 

