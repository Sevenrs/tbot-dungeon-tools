import sys, json
from datetime import datetime


def run():

    # Read input file
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    # Print some useful information
    print('generate_map_bin by Icseon. Input file is > {0} <'.format(input_file))

    try:

        # Load JSON file
        data = json.load(open(input_file))

        # Output some useful information
        print("Got {0} map(s). Generating binary file and saving to {1} ...\n".format(len(data), output_file))
        for instance in data:
            print("{0}\t{1}\t{2}\t{3}".format(instance['name'], instance['map'], instance['bgm'], instance['ui_picture'])
                  .expandtabs(35))

        # Construct map data block
        map_data = bytearray()

        for index, instance in enumerate(data):

            # Construct value array
            values = [
                str(index)
            ]
            for key in instance.keys():
                values.append(str(instance[key]))

            # Add value, followed by the 0x09 seperator
            for val_idx, value in enumerate(values):
                map_data.extend(value.encode('windows-1252', errors='replace'))

                # Add 0x09 to separate the values. Use 0x0D, 0x0A, 0x09 to signify the end of the value
                map_data.extend([0x09] if (val_idx + 1) < len(values) else [0x0D, 0x0A, 0x09])

        # After we've added all the map data, we'll want to remove the last three bytes and replace them
        map_data = map_data[:-3]
        map_data.extend([0x0D, 0x3B, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x0D, 0x0A, 0x0D, 0x0A])

        # Construct file header
        file_header = bytearray()
        file_header.extend([0xFE, 0xFF, 0xFF, 0xFF])
        file_header.extend((65535 - len(map_data)).to_bytes(length=2, byteorder='little'))
        file_header.extend([0xFF, 0xFF])

        # Combine the file header and map data
        result = bytearray()
        result.extend(file_header)
        result.extend(map_data)
        result.extend([0xFF, 0xFF, 0xFF, 0xFF])

        # We'll have to xor the file now
        for i in range(len(result)):
            result[i] = result[i] ^ 0xFF

        open(output_file, 'wb').write(result)


    except Exception as e:
        print('An error occurred: ', e)