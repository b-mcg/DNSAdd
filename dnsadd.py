#!/usr/bin/env python2

#imports
import subprocess
import argparse


def build_opts():
    """
    Build and return a
    parser object containing
    valid command line arguments

    """
    # Build parser object
    parser      =       argparse.ArgumentParser(description='dnsadd commandline options')

    # Add dns domain name positional argument
    parser.add_argument('domain', type=str, help='domain name of dns server(Required).',
                        metavar=''
                        )
    # Add ipv4 nameserver positional argument
    parser.add_argument('nameserver1', type=str, help='ipv4 address of dns server(Required).',
                        metavar=''
                        )

    # Add optional backup ipv4 nameserver argument
    parser.add_argument('-ns2', '--nameserver2', type=str, required=False,
                        help='ipv4 address of backup dns server(Optional).', metavar=''
                        )

    # return parser object
    return parser


def arg_parser(parser):
    """
    Parse and return a dictionary
    of command line arguments

    """
    # Parse arguments
    args        =       parser.parse_args()

    # Build and return a dictionary of command line arguments
    return {'d'     : args.domain,
            'n'     : args.nameserver1,
            'n2'    : args.nameserver2 if '-ns2' or '--nameserver2' in args else None
            }


class DNSArgumentError(Exception):
    """
    Error to be raised 
    when domain name is invalid.
    Mainly used for checking if 
    domain name is first argument given

    """
    pass

class NameserverArgumentError(Exception):
    """
    Error to be raised 
    when IPv4 nameserver
    is in invalid form.
    Mainly used for checking if
    nameserver is second argument
    given

    """
    pass


def dnsadd(args):
    """
    Switches to root user
    and echoes comcast dns
    servers, then exits
    to normal user

    """
    # Check for ipv4 errors if backup nameserver is given.
    if args['n2'] is not None and not check_for_ipv4_errors(args['n2']) or not check_for_ipv4_errors(args['n']):
        raise NameserverArgumentError("\nIPv4 Error: Check that IP address given is valid.\n")

    # Check for ipv4 errors if only required nameserver is given.
    elif args['n2'] is None and not check_for_ipv4_errors(args['n']):
        raise NameserverArgumentError("\nIPv4 Error: Check that IP address given is valid.\n")

    # Check for DNS Domain errors.
    elif not check_for_dns_errors(args['d']):
        raise DNSArgumentError("\nTop-Level Domain not found: Check that the DNS Domain name was first argument given.\n")

    # Call subprocess with su root -c echo to add DNS info to /etc/resolv.conf.
    else:
        p       =       subprocess.call(['su', 'root', 
                                        '-c', r"echo -e 'domain {0}.\nnameserver {1}{2}' >> /etc/resolv.conf".format(args['d'], args['n'],
                                        ''.join((r'\nnameserver ', args['n2'])) if args['n2'] is not None else '')])


def check_for_ipv4_errors(ip_args):
    """
    Check for valid IPv4 address.
    Return True if valid, False
    otherwise.

    """
    # Split ip arg into list, omitting dot notation.
    ip_1        =       ip_args.split('.')

    # Check if four item list.  Return False if not.
    if len(ip_1) != 4:
        return False

    # If four item list, traverse the list and convert each item to an int.
    # Return False if ValueError is raised.
    elif len(ip_1) == 4:
        for i in ip_1:
            try:
                int(i)
            except ValueError:
                return False

    # Otherwise return True.
    return True


def check_for_dns_errors(dns_domain):
    """
    Check that domain name is valid.
    Return True if valid.
    Otherwise return False.

    """
    # Build list containing most common top-level domains to test against.
    top_levels      =       ['.com', '.net', '.org', '.gov', '.edu']

    # Traverse top-level domains list.
    for i in top_levels:

    # Check if the last portion of domain arg is in top-level domain list.
        if i in dns_domain[dns_domain.rfind('.'):]:

    # Return True if match is found.
            return True 

    # Otherwise return False.
    return False
    

def main():
    """
    main()

    """
    # Build args
    args        =       arg_parser(build_opts())

    # Call dnsadd function
    dnsadd(args)


if __name__ ==  '__main__':
    main()
