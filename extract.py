#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getpass
from pykeepass import PyKeePass

def _get_group(keepass, group_path):
    """
    Get or create a group based on a group object
    """
    if keepass.find_groups(path=group_path):
        return keepass.find_groups(path=group_path)
    elif '/' not in group_path.rstrip('/'):
        return keepass.root_group
    else:
        parent_name, name = group_path.rstrip('/').rsplit('/', 1)
        parent_group = _get_group(keepass, parent_name)
        return keepass.add_group(parent_group, name)

def _add_entry(keepass, entry):
    """
    Add an entry to a keepass
    """
    group = _get_group(keepass, entry.get_custom_property(search_attribute) or '')
    new_entry = keepass.add_entry(destination_group=group,
                                  title=entry.title or '',
                                  username=entry.username or '',
                                  password=entry.password or '',
                                  url=entry.url or '',
                                  notes=entry.notes or '',
                                  tags=entry.tags or [],
                                  icon=entry.icon or '')
    # some attributes need to be set after creation
    new_entry.autotype_enabled = entry.autotype_enabled
    new_entry.autotype_sequence = entry.autotype_sequence
    return new_entry

# setting arguments and get them
parser = ArgumentParser(description='A small tool to export a subset of entries from one keepass to another one.')
parser.add_argument('input_keepass', type=str, help='input keepass path')
parser.add_argument('output_keepass', type=str, help='output keepass path')
parser.add_argument('-i', '--input-password', type=str, help='input keepass password', metavar='password')
parser.add_argument('-o', '--output-password', type=str, help='output keepass password', metavar='password')
parser.add_argument('-a', '--attribute', type=str, default='extract_to', help='attribute for getting entries', metavar='attribute')
args = parser.parse_args()
search_attribute = args.attribute
input_path = args.input_keepass
output_path = args.output_keepass
# ask for passwort if not passed by command line
input_password = args.input_password if args.input_password else getpass(prompt='Input KeePass password:')
output_password = args.output_password if args.output_password else getpass(prompt='Output KeePass password:')

# open keepass files 
input_keepass = PyKeePass(input_path, input_password)
output_keepass = PyKeePass(output_path, output_password)

# empty destination KeePass
for entry in output_keepass.entries:
    entry.delete()
for group in output_keepass.groups:
    if not group == output_keepass.root_group:
        group.delete()

# find all entries which should be exctracted and add them to output keepass
searchstring = {}
searchstring[search_attribute] = '.*'
for entry in input_keepass.find_entries(string=searchstring, regex=True):
    _add_entry(output_keepass, entry)

# finally, save the output keepass
output_keepass.save()
