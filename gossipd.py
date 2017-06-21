#TODO: DRY refactor for sending messages, sending errors
#TODO: Parcel size tuning
import multiprocessing
import socket
import random
import base64
import json

LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 5555
SOCKET_BACKLOG = 10
PARCEL_SIZE = 2048
CONTROL_STRING = '#!'

random.seed()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((LISTEN_IP, LISTEN_PORT))
sock.listen(SOCKET_BACKLOG)

peers = {'sina': {'key': 'aaa', 'past_ips': ['127.0.0.1']}}
messages = [{'timestamp': 'x', 'from': 'sina', 'source': 'alice', 'text': "best msg is best"}]

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
            #    for ip in peer['past_ips']:
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
        
        if data.startswith("%shello " % CONTROL_STRING):
            name_data = data.split(" ")

            if len(name_data) == 1:
                conn.send("%sbad_hello\r\n" % CONTROL_STRING)
                conn.shutdown(1)
                conn.close()
                break

            name = name_data[1].strip()

            if name not in peers.keys():
                conn.send("%sunknown_peer\r\n" % CONTROL_STRING)
                conn.shutdown(1)
                conn.close()
                break

            challenge = base64.encode("areyoureal") #TODO: Generate OTP
            conn.send("%schallenge %s\r\n" % (CONTROL_STRING, challenge))
            
            response = conn.recv(PARCEL_SIZE).strip()
            if response == "%sresponse %s" % (CONTROL_STRING, challenge):
                conn.send("%smessages %d\r\n" % (CONTROL_STRING, len(messages)))
                for message in messages:
                    conn.send("%smessage %s\r\n" % (CONTROL_STRING, base64.encode(json.dumps(message))))

                #TODO:
                #recv #!messages N 
                #loop N times recv message and append

                conn.shutdown(1)
                conn.close()
                break
            else:
                conn.send("%sbad_otp\r\n" % CONTROL_STRING)
                conn.shutdown(1)
                conn.close()
                break
