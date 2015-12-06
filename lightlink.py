import socket
import time


class Client(object):
    """
    Communicate with the lightlink
    """
    def __init__(self, link_ip, link_port=9760, response_port=9761):
        self.read_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.write_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.read_sock.bind(('0.0.0.0', response_port))
        self.message_count = 1
        self.link_ip = link_ip
        self.link_port = link_port

    def send(self, command):
        """
        Send a command
        """
        seq_no = '{:03d},!'.format(self.message_count)
        self.write_sock.sendto(seq_no + command,
                               (self.link_ip, self.link_port))
        self.message_count += 1

    def recv(self, buffsize=1024):
        """
        Receive a response
        """
        response = self.read_sock.recvfrom(buffsize)
        return response

    def on(self, room, device):
        """
        Turn on a light
        """
        ident = 'R{}D{}'.format(room, device)
        command = ident + 'F0|1337|Off'
        self.send(command)
        return self.recv()

    def off(self, room, device):
        """
        Turn off a light
        """
        ident = 'R{}D{}'.format(room, device)
        command = '001,!' + ident + 'F1|1337|On'
        self.send(command)
        return self.recv()

    def flicker(self, room, device, delay=1):
        """
        Turn it off and on again
        """
        self.on(room, device)
        time.sleep(delay)
        self.off(room, device)

    def register(self):
        """
        Send a register message to the LightLink
        You need to press a button when it starts flashing
        """
        self.send('F*p')
        return self.recv()


def all_devices():
    """
    Iterate over all devices
    Lightwave numbers all rooms and devices - we don't have access to their
    names.
    """
    for room in range(1, 2):
        for device in range(1, 6):
            yield room, device


if __name__ == '__main__':
    client = Client('192.168.1.51')

    for room, device in all_devices():
        client.flicker(room, device)
