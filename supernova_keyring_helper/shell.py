import sys
import getpass
import argparse
from supernova import supernova
from supernova import executable


def write(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def input_value():
    try:
        value = sys.stdin.readline().rstrip('\n')
    except KeyboardInterrupt:
        value = ''
    if len(value) < 1:
        msg = '\n[{}] No data was altered in your keyring.\n'.format(
            executable.rwrap('Canceled'))
        write(msg)
        sys.exit()
    return value


def input_all_values():
    ''' Prompts for values. '''
    values = {}

    write('DDI : '.rjust(15))
    ddi = input_value()
    values['OS_TENANT_NAME'] = ddi
    values['OS_PROJECT_ID'] = ddi

    write('USERNAME : '.rjust(15))
    username = input_value()
    values['OS_USERNAME'] = username

    write('REGION : '.rjust(15))
    region = input_value().upper()
    values['OS_REGION_NAME'] = region

    write('APIKEY : '.rjust(15))
    apikey = input_value()
    values['OS_PASSWORD'] = apikey

    return values


def store_values(s, args, values):
    for each in values.keys():
        parameter = '{}:{}'.format(args.env, each)
        value = values.get(each)
        if args.verbose:
            write('{}={}\n'.format(each, value))
        try:
            s.password_set(parameter, value)
        except:
            if args.verbose:
                write('failed to store {}\n'.format(parameter))
            return False
    return True


def set_values(s, args):
    msg = '[{}] Storing data for the {} environment.\n'.format(
        executable.gwrap('Keyring operation'),
        args.env)
    write(msg)

    values = input_all_values()
    result = store_values(s, args, values)

    if result:
        msg = '[{}] Stored all values in keyring.\n'.format(
            executable.gwrap('Success'))
        write(msg)
    else:
        msg = '[{}] Could not store values in keyring.\n'.format(
            executable.rwrap('Failure'))
        write(msg)


def get_values(s, args):
    msg = '[{}] Retrieving data for the {} environment.\n'.format(
        executable.gwrap('Keyring operation'),
        args.env)
    write(msg)


def handle_args(s):
    ''' Handle arguements and validate input. '''
    # get a list of possible environments
    possible = s.get_nova_creds().sections()

    # program info
    the_name = 'supernova-keyring-helper'
    the_description = ('Store all required information for a Rackspace '
                       'Cloud environment in supernova-keyring.')
    the_version = '%(prog)s 0.2'

    # start parsing the args
    parser = argparse.ArgumentParser(prog=the_name,
                                     description=the_description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--get', action='store_true',
                       dest='get_values',
                       help='retrieves all credentials for env from keychain')
    group.add_argument('-s', '--set', action='store_true',
                       dest='set_values',
                       help='stores all credentials for env in keychain')    
    parser.add_argument('env',
                        help='environment to work against')
    parser.add_argument('-l',
                        '--list',
                        action=executable._ListAction,
                        help=argparse.SUPPRESS)
    #                    help='list all configured environments')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=the_version)
    parser.add_argument('-V',
                        '--verbose',
                        action='store_true',
                        help=argparse.SUPPRESS)
    #                    help='enable verbose output')
    args = parser.parse_args()

    # check for config file
    executable.check_supernova_conf(s)

    # check if env is valid
    executable.setup_supernova_env(s, args.env)

    return args


def main():
    s = supernova.SuperNova()
    args = handle_args(s)
    if args.set_values:
        set_values(s, args)
    if args.get_values:
        get_values(s, args)


if __name__ == '__main__':
    main()

# vim: set syntax=python sw=4 ts=4 expandtab :
