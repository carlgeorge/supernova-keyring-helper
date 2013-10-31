import sys
import argparse
import supernova.supernova
import supernova.executable


def write(msg):
    ''' My print function. '''
    sys.stdout.write(msg)
    sys.stdout.flush()


def input_value():
    ''' Get single value from user input. '''
    try:
        value = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        value = ''
    if len(value) < 1:
        msg = '[{}]\n'.format(supernova.executable.rwrap('Canceled'))
        write(msg)
        return None
    return value


def input_all_values():
    ''' Prompts for values from user input. '''
    payload = {}
    count = 0
    write('DDI : '.rjust(15))
    ddi = input_value()
    if ddi:
        payload['OS_TENANT_NAME'] = ddi
        payload['OS_PROJECT_ID'] = ddi
        count += 1
    write('USERNAME : '.rjust(15))
    username = input_value()
    if username:
        payload['OS_USERNAME'] = username
        count += 1
    write('APIKEY : '.rjust(15))
    apikey = input_value()
    if apikey:
        payload['OS_PASSWORD'] = apikey
        count += 1
    write('REGION : '.rjust(15))
    region = input_value()
    if region:
        payload['OS_REGION_NAME'] = region
        count += 1
    return payload, count


def store_values(s, args, payload):
    ''' Store the values in the keyring. '''
    for each in payload.keys():
        parameter = '{}:{}'.format(args.env, each)
        value = payload.get(each)
        try:
            s.password_set(parameter, value)
        except:
            return False
    return True


def set_values(s, args):
    ''' Primary function for the --set flag. '''
    msg = '[{}] Storing data for the {} environment.\n'.format(
        supernova.executable.gwrap('Keyring operation'),
        args.env)
    write(msg)
    payload, count = input_all_values()
    result = store_values(s, args, payload)
    if result:
        if count > 1:
            msg = '[{}] Stored {} values in your keyring.\n'.format(
                supernova.executable.gwrap('Success'), count)
        elif count == 1:
            msg = '[{}] Stored 1 value in your keyring.\n'.format(
                supernova.executable.gwrap('Success'))
        else:
            msg = '[{}] No data was altered in your keyring.\n'.format(
                supernova.executable.gwrap('Success'))
    else:
        msg = '[{}] Could not store values in keyring.\n'.format(
            supernova.executable.rwrap('Failure'))
    write(msg)


def print_values(payload):
    ''' Print the values that were retrieved from the keyring. '''
    # populate friendly variables from the payload
    ddi = payload.get('OS_TENANT_NAME')
    username = payload.get('OS_USERNAME')
    apikey = payload.get('OS_PASSWORD')
    region = payload.get('OS_REGION_NAME')

    # print each friendly variable, if it exists
    count = 0
    if ddi:
        write('DDI : '.rjust(15))
        write('{}\n'.format(ddi))
        count += 1
    if username:
        write('USERNAME : '.rjust(15))
        write('{}\n'.format(username))
        count += 1
    if apikey:
        write('APIKEY : '.rjust(15))
        write('{}\n'.format(apikey))
        count += 1
    if region:
        write('REGION : '.rjust(15))
        write('{}\n'.format(region))
        count += 1

    # print the total count of friendly variables
    if count > 1:
        msg = '[{}] Retrieved {} values from your keyring.\n'.format(
            supernova.executable.gwrap('Success'), count)
    elif count == 1:
        msg = '[{}] Retrieved 1 value from your keyring.\n'.format(
            supernova.executable.gwrap('Success'))
    else:
        msg = '[{}] No data was retrieved from your keyring.\n'.format(
            supernova.executable.gwrap('Success'))
    write(msg)


def retrieve_all_values(s, args):
    ''' Retrieve the values in the keyring. '''
    payload = {}
    os_list = ['OS_TENANT_NAME',
               'OS_PROJECT_ID',
               'OS_USERNAME',
               'OS_PASSWORD',
               'OS_REGION_NAME']
    for each in os_list:
        parameter = '{}:{}'.format(args.env, each)
        try:
            value = s.password_get(parameter)
        except:
            value = ''
        if value:
            payload[each] = value
    return payload


def get_values(s, args):
    ''' Primary function for the --get flag. '''
    msg = '[{}] Retrieving data for the {} environment.\n'.format(
        supernova.executable.gwrap('Keyring operation'),
        args.env)
    write(msg)

    # build the payload from the keyring
    payload = retrieve_all_values(s, args)

    # warn the user if the DDI is stored incorrectly
    if payload.get('OS_TENANT_NAME') != payload.get('OS_PROJECT_ID'):
        msg = ('[{}] OS_TENANT_NAME does not match OS_PROJECT_ID\n'.format(
            supernova.executable.rwrap('Warning')))
        write(msg)

    # print what we want
    print_values(payload)


def handle_args(s):
    ''' Handle arguements and validate input. '''
    # check for config file
    supernova.executable.check_supernova_conf(s)

    # get a list of possible environments
    possible = s.get_nova_creds().sections()

    # program info
    the_name = 'supernova-keyring-helper'
    the_description = ('Store all required information for a Rackspace '
                       'Cloud environment in supernova-keyring.')
    the_version = '%(prog)s 0.3'

    # start parsing the args
    parser = argparse.ArgumentParser(prog=the_name,
                                     description=the_description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g',
                       '--get',
                       action='store_true',
                       dest='get_values',
                       help='retrieves all credentials for env from keychain')
    group.add_argument('-s',
                       '--set',
                       action='store_true',
                       dest='set_values',
                       help='stores all credentials for env in keychain')
    parser.add_argument('env',
                        help=('environment to work against. '
                              'valid options: {}'.format(possible)))
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=the_version)
    args = parser.parse_args()

    # check if env is valid
    supernova.executable.setup_supernova_env(s, args.env)

    return args


def main():
    s = supernova.supernova.SuperNova()
    args = handle_args(s)
    if args.set_values:
        set_values(s, args)
    if args.get_values:
        get_values(s, args)


if __name__ == '__main__':
    main()

# vim: set syntax=python sw=4 ts=4 expandtab :
