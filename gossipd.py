#TODO: DRY refactor for sending messages, sending errors
#TODO: Parcel size tuning
import multiprocessing
import socket
import random

LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 5555
SOCKET_BACKLOG = 10
PARCEL_SIZE = 2048

random.seed()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.listen(SOCKET_BACKLOG)

peers = {'sina': {'key': 'aaa', 'hosts': ['127.0.0.1:5555']}}
messages = [{'timestamp': 'x', 'from': 'sina', 'source': 'alice', 'text': "best msg is best"}]

def encrypt(name, challenge):
    return challenge

def client():
    while True:
        action = random.randint(1, 10)
        if action == 1:
            print("generate RSA key")
        elif action == 2:
            print("send bogus challenges")
        elif action == 3:
            print("get messages from peers")
            #for peer in peers:
            #    for host in peer['hosts']:
            #       #connect to peer
            #       #send hello
            #       #recv otp
            #       #send response
            #       #recv #!messages N
            #       #recv #!message 1, 2, ..., N
            #       #send #!messages N
            #       #send #!message 1, 2, ..., N
            #       #update last connected
        else:
            print("do nothing")

p = multiprocessing.Process(target=client)
p.start()

while True:

    conn, peer_ip = sock.accept()

    while True:
        data = conn.recv(PARCEL_SIZE)
        
        if data.startswith("hello "):
            hello = data.split(" ")

            if len(hello) == 1:
                conn.send("bad_hello\n")
                conn.shutdown(1)
                conn.close()
                break

            name = hello[1].strip()

            if name not in peers.keys():
                conn.send("unknown_peer\n")
                conn.shutdown(1)
                conn.close()
                break

            challenge = "areyoureal" #TODO: Generate OTP
            conn.send("challenge %s\n" % encrypt(name, challenge))
            
            response = conn.recv(PARCEL_SIZE).strip()
            if response == "response %s" % challenge:
                conn.send("messages %d\n" % len(messages))
                for message in messages:
                    conn.send("message %s,%s,%s,%s\n" % (message['time'], message['from'], message['source'], message['text']))

                #TODO:
                #recv #!messages N 
                #loop N times recv message and append

                conn.shutdown(1)
                conn.close()
                break
            else:
                conn.send("bad_otp\n")
                conn.shutdown(1)
                conn.close()
                break
