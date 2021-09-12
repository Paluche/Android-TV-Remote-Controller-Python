#!/usr/bin/env python3

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pynput import keyboard
from pairing import PairingSocket
from sending_keys import SendingKeySocket
from key_codes import *


# Set your server name, server ip and client name here
sending_key_socket = None

def print_guide():
    print('''
    You can controll you device with this keys:
                w = up                      u = volume up

    a = left    o = ok      d = right       j = volume down

                s = down

    b = back    h = home    n = netflix     q = exit
    ''')

def on_release(key):
    global sending_key_socket
    print_guide()
    if key.char == 'q' or key == keyboard.Key.esc:
        # Stop listener
        sending_key_socket.disconnect()
        return False
    elif key.char == 'h' :
        sending_key_socket.send_key_command(KEYCODE_HOME)
    elif key.char == 'b' :
        sending_key_socket.send_key_command(KEYCODE_BACK)
    elif key.char == 'w' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_UP)
    elif key.char == 's' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_DOWN)
    elif key.char == 'a' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_LEFT)
    elif key.char == 'd' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_RIGHT)
    elif key.char == 'o' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_CENTER)
    elif key.char == 'u' :
        sending_key_socket.send_key_command(KEYCODE_VOLUME_UP)
    elif key.char == 'j' :
        sending_key_socket.send_key_command(KEYCODE_VOLUME_DOWN)
    elif key.char == 'n' :
        sending_key_socket.send_launch_app_command("netflix")

def __main():
    global sending_key_socket

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)

    parser.add_argument(
        dest='host',
        help='IP address or host name of the TV.'
    )

    parser.add_argument(
        dest='name',
        help='Friendly name of the TV'
    )

    parser.add_argument(
        '--pairing',
        metavar='[Client name]',
        dest='pairing',
        help='Perform the pairing with the TV, specify the name of the client.'
    )

    parsed = parser.parse_args()

    # if argument for pairing exist, start to pair
    if parsed.pairing is not None:
        print('Performing pairing')
        pairing_sock = PairingSocket(parsed.pairing, parsed.host)
        pairing_sock.connect()
        pairing_sock.start_pairing()
        assert (pairing_sock.connected), "Connection unsuccessful!"
        print('Pairing OK')

    print('Connecting to the TV')
    sending_key_socket = SendingKeySocket(parsed.name, parsed.host)
    sending_key_socket.connect()
    print_guide()
    # Receive input keys
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    __main()
