#!/usr/bin/env python
import sys
import csv


def create_alias(alias):
    """Create a new zone alias"""

    name = alias['alias_name']
    wwpn = alias['wwpn']
    message = 'alicreate "{}", "{}"'.format(name, wwpn)

    print(message)


def create_zoning(aliases_t, aliases_i):
    """Create a new zone alias"""

    message = 'zonecreate "{0}_to_{1}_zone", "{0}; {1}"'
    zones = []
    for target in aliases_t:
        target_name = target['alias_name']
        target_wwpn = target['wwpn']
        for initiator in aliases_i:
            initiator_name = initiator['alias_name']
            initiator_wwpn = initiator['wwpn']
            zones.append(message.format(
                target_name, initiator_name
            ))
    for zone in zones:
        print(zone)        

    return zones
            

def zone_add(san_name, zones):
    """Add one or more members to an existing zone"""

    create = True
    for zone in zones:
        zone_name = zone.split()[1].replace(',', '')

        if create:
            message = 'cfgcreate "{}", {}'.format(san_name, zone_name)
            create = False
            print(message)

        message = 'cfgadd "{}", {}'.format(san_name, zone_name)
        print(message)


def zoning_config(csv_file, zone_name):
    """Parse the csv file and initiate zoning creation"""

    csv_file = csv.DictReader(open(csv_file))
    aliases_i = []
    aliases_t = []

    for line in csv_file:
        create_alias(line)

        mode = line['mode']
        if mode == "initiator":
            aliases_i.append(line)
        elif mode == "target":
            aliases_t.append(line)

    zones = create_zoning(aliases_t, aliases_i)
    zone_add(zone_name, zones)


if __name__ == '__main__':
    file_name = sys.argv[1]
    zone_name = sys.argv[2]
    zoning_config(file_name, zone_name)
    print('cfgsave')
    print('cfgenable {}'.format(zone_name))

