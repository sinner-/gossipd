#TODO: DRY refactor for sending messages, sending errors
import multiprocessing
import socket
import random
import hashlib
import re

LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 5555
SOCKET_BACKLOG = 10
MAX_NAME_LEN = 50
OTP_RANGE_START = 2**128
OTP_RANGE_END = 2**129

random.seed()

hello_pattern = re.compile("(hello [a-zA-Z0-9]+)$")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.listen(SOCKET_BACKLOG)

keys = [{'sina': ('privatekey', 'publickey')}, {'bogus': ('privatekey', 'publickey')}]
peers = {'sina': {'peer_key': 'aaa', 'my_key': 'bbb', 'hosts': ['127.0.0.1:5555']}}
messages = [{'timestamp': 'x', 'from': 'sina', 'source': 'alice', 'text': "best msg is best"}]

#TODO: implement
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
            print("get/send messages from/to peers")
            #for peer in peers:
            #    for host in peer['hosts']:
            #       #connect to peer
            #       #send hello using unique peer key
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

    data = conn.recv(len("hello ") + MAX_NAME_LEN + 1).strip()

    if hello_pattern.match(data)
        hello = data.split(" ")

        name = hello[1].strip()

        if name not in peers.keys():
            conn.send("unknown_peer\n")
            conn.shutdown(1)
            conn.close()
            continue

        challenge = hashlib.sha256(str(random.randint(OTP_RANGE_START, OTP_RANGE_END))).hexdigest()
        conn.send("challenge %s\n" % encrypt(name, challenge))

        response = conn.recv(len("response ") + len(challenge) + 1).strip()
        if response == "response %s" % challenge:
            conn.send("messages %d\n" % len(messages))
            for message in messages:
                #TODO: should probably transmit message length
                conn.send("message %s,%s,%s,%s\n" % (message['time'], message['from'], message['source'], message['text']))

            #TODO:
            #recv #!messages N
            #loop N times recv message and append

            conn.shutdown(1)
            conn.close()
        else:
            conn.send("bad_otp\n")
            conn.shutdown(1)
            conn.close()
