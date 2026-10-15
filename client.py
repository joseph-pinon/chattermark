import sys
import socket
import ssl
import threading
from queue import Queue

SERVER = "irc.libera.chat"
PORT = 6697
NICK = "testing"
USERNAME = "my_testing"
REALNAME = "real_testing"


def send(sock, message):
    print(f">> {message}")
    sock.sendall((message + "\r\n").encode("utf-8"))


def recieve(irc):
    buffer = b""
    while True:
        data = irc.recv(4096)
        if not data:
            print("SERVER DISCONNECTED")
            break
        buffer += data
        while b"\r\n" in buffer:
            line, buffer = buffer.split(b"\r\n", 1)
            message = line.decode("utf-8", errors="replace")
            print(f"<< {message}")

            # Respond to keepalive requests.
            if message.startswith("PING "):
                send(irc, "PONG " + message[5:])


def main():

    print("****JGP IRC CLIENT****\n")

    context = ssl.create_default_context()
    with socket.create_connection((SERVER, PORT)) as s:
        with context.wrap_socket(s, server_hostname=SERVER) as irc:
            send(irc, f"NICK {NICK}")
            send(irc, f"USER {USERNAME} 0 * :{REALNAME}")
            conn = threading.Thread(target=recieve, args=[irc], daemon=True)
            conn.start()

            while True:
                command = input()
                if (command.lower() == "quit"):
                    break
                else:
                    send(irc, command)

main()
