import socket
import time

message_count = 1
port = 9760
response_port = 9761
ip = '192.168.1.51'

read_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
write_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_sock.bind(('0.0.0.0', response_port))


def send(command):
    """
    Send a command
    """
    global message_count
    seq_no = '{:03d},!'.format(message_count)
    write_sock.sendto(seq_no + command, (ip, port))
    message_count += 1


def recv(buffsize=1024):
    """
    Receive a response
    """
    response = read_sock.recvfrom(buffsize)
    return response


def on(room, device):
    """
    Turn on a light
    """
    ident = 'R{}D{}'.format(room, device)
    command = ident + 'F0|1337|Off'
    send(command)
    print recv()


def off(room, device):
    """
    Turn off a light
    """
    ident = 'R{}D{}'.format(room, device)
    command = '001,!' + ident + 'F1|1337|On'
    send(command)
    print recv()


def flicker(room, device, delay=1):
    """
    Turn it off and on again
    """
    on(room, device)
    time.sleep(delay)
    off(room, device)


def all_devices():
    """
    Iterate over all devices
    Lightwave numbers all rooms and devices - we don't have access to their
    names.
    """
    for room in range(1, 2):
        for device in range(1, 6):
            yield room, device


def register():
    """
    Send a register message to the LightLink
    You need to press a button when it starts flashing
    """
    send('F*p')
    print recv()


if __name__ == '__main__':
    #register()
    for room, device in all_devices():
        flicker(room, device)
