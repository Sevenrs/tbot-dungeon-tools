import sys
from tools import generate_map_bin, generate_dungeon_bin

# Available tools
tools = [
    {
        'name':             'Generate map binary file',
        'internal_name':    'generate_map_bin',
        'description':      'This tool will convert a JSON input file to a binary file',
        'example_use':      'generate_map_bin maps.json',
        'method':           generate_map_bin.run
    },

    {
        'name':             'Generate dungeon file',
        'internal_name':    'generate_dungeon_bin',
        'description':      'This tool will generate a dungeon.bin file from a dungeon JSON file',
        'example_use':      'generate_dungeon_bin files/dungeon.json files/dungeon.bin',
        'method':           generate_dungeon_bin.run
    }
]

# Script entry point
def main():

    # Print out some useful information
    print('T-Bot Tools by Icseon. Command line arguments:', sys.argv, '\n')

    if len(sys.argv) < 2:

        print('Available tools\n')

        print('Tool name\tDescription'.expandtabs(35), '\n')

        for tool in tools:
            print("{0}\t{1}\t{2}".format(
                tool['name'], tool['description'], tool['example_use']
            ).expandtabs(35))
    else:
        for tool in tools:
            if tool['internal_name'] == sys.argv[1]:
                tool['method']()

if __name__ == '__main__':
    main()