DNSAdd
---
---

Simple Python script allowing for the addition of a DNS domain, an IPv4 nameserver, and an optional backup IPv4 nameserver to /etc/resolv.conf.
Useful if using statically assigned IP addresses and running a script through OpenVPN which edits resolv.conf and removes all DNS entries upon exit.

Options:

domain (Positional argument)

nameserver1 (Positional argument)

-ns2/--nameserver2 (Optional backup IPv4 nameserver)

Example Usage:

dnsadd.py domain.server.com 68.23.45.76

Additional Notes:

Can either run the script as: python2 dnsadd.py [domain] [nameserver1]
or to make use easier, run: sudo cp dnsadd.py /usr/bin/ ; sudo chmod 755 /usr/bin/dnsadd.py
and just call the program as: dnsadd.py [domain] [nameserver1]
