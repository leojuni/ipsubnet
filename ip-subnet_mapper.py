import ipaddress
import csv

# Ask for input IP address .csv file path
# format example 10.0.0.33
ip_file_path = input("Enter IP address file path in .csv format: ")

# Ask for input subnet .csv file path with subnet ID in first column & subnet mask in sider notation.
#format example: 10.0.0.0 24
subnet_file_path = input("Enter subnet file path in .csv format: ")

# Ask for output .csv file path to save results
output_file_path = input("Enter output file path in .csv format to save results: ")

# Open the CSV files for reading
with open(ip_file_path, 'r') as ip_file, open(subnet_file_path, 'r') as subnet_file:

    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:

        ip_reader = csv.reader(ip_file)
        subnet_reader = csv.reader(subnet_file)
        output_writer = csv.writer(output_file)

        # Loop over each IP address in the IP address file
        for ip_row in ip_reader:
            ip_address = ip_row[0]

            # Convert the IP address string to an ipaddress.IPv4Address object
            try:
                ip_address_obj = ipaddress.IPv4Address(ip_address)
            except ValueError:
                print(f'Error: Invalid IP address format: {ip_address}')
                continue

            # Loop over each subnet in the subnet file
            for subnet_row in subnet_reader:
                subnet_id = subnet_row[0]
                subnet_mask = subnet_row[1]

                # Create a network object using the subnet ID and subnet mask
                try:
                    network = ipaddress.IPv4Network(subnet_id+'/'+subnet_mask)
                except ValueError:
                    print(f'Error: Invalid subnet format: {subnet_id}/{subnet_mask}')
                    continue

                # Check if the IP address is within the network
                if ip_address_obj in network:
                    result_row = [ip_address, f'{subnet_id}/{subnet_mask}']
                    output_writer.writerow(result_row)

            # Reset the subnet file pointer to the beginning of the file
            subnet_file.seek(0)