from sockets import SocketP2P
from threading import Thread
import sys

def receive(peer):
    while(True):
        packet = peer.receive()
        print('Received: {}'.format(packet))
        
def chat(args):
    ip = args[:args.find('/')]
    port = args[args.find('/')+1:]
    peer = SocketP2P(ip, int(port))
    peer.connect()

    th = Thread(target = receive, args=[peer])

    if peer.peer_type()=='server':
        th.start()
        while(True):
            packet = input()
            peer.send(packet)

    elif peer.peer_type()=='client':
        th.start()
        while(True):
            packet = input()
            peer.send(packet)

    return
def main():
    try:
        args = sys.argv[1]
    except:
        print('Error: inform ip/port')
        return
    
    chat(args)

if __name__ == '__main__':
	main()