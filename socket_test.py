import socket
import threading


HOST = socket.gethostbyname("localhost")
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_message():
    while True:
        message = input()
        client.send(message)


def receive_message():
    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)


if __name__ == '__main__':


    thread_send = threading.Thread(target=send_message)
    thread_send.start()

    receive_message()