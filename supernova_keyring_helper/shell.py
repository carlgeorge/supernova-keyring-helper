import sys
import getpass
import argparse
from supernova import supernova
from supernova import executable


def write(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def get_value():
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


def get_all_values():
    ''' Prompts for values. '''
    values = {}

    write('DDI : '.rjust(15))
    ddi = get_value()
    values['OS_TENANT_NAME'] = ddi
    values['OS_PROJECT_ID'] = ddi

    write('USERNAME : '.rjust(15))
    username = get_value()
    values['OS_USERNAME'] = username

    write('REGION : '.rjust(15))
    region = get_value().upper()
    values['OS_REGION_NAME'] = region

    write('APIKEY : '.rjust(15))
    apikey = get_value()
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


def handle_args(s):
    ''' Handle arguements and validate input. '''
    # get a list of possible environments
    possible = s.get_nova_creds().sections()

    # program info
    the_name = 'supernova-setenv'
    the_description = ('Store all required information for a Rackspace '
                       'Cloud environment in supernova-keyring.')
    the_version = '%(prog)s 0.2'

    # start parsing the args
    parser = argparse.ArgumentParser(prog=the_name,
                                     description=the_description)
    parser.add_argument('env',
                        help='environment to store values for')
    parser.add_argument('-l',
                        '--list',
                        action=executable._ListAction,
                        help='list all configured environments')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=the_version)
    parser.add_argument('-V',
                        '--verbose',
                        action='store_true',
                        help='enable verbose output')
    args = parser.parse_args()

    # check for config file
    executable.check_supernova_conf(s)

    # check if env is valid
    executable.setup_supernova_env(s, args.env)

    return args


def main():
    s = supernova.SuperNova()
    args = handle_args(s)

    msg = '[{}] Storing data for the {} environment.\n'.format(
        executable.gwrap('Keyring operation'),
        args.env)
    write(msg)

    values = get_all_values()
    result = store_values(s, args, values)

    if result:
        msg = '[{}] Stored all values in keyring.\n'.format(
            executable.gwrap('Success'))
        write(msg)
    else:
        msg = '[{}] Could not store values in keyring.\n'.format(
            executable.rwrap('Failure'))
        write(msg)


if __name__ == '__main__':
    main()

# vim: set syntax=python sw=4 ts=4 expandtab :
