
import socket

# USB Transceiver
# PID: N3TOA09033C
# IP: 192.168.1.254 / 192.168.1.159
# Current: 9.9.9.34 (usb?)
# port: 34048

HOST1 = '255.255.255.255'
PORT1 = 8901
HOST2 = '192.168.1.55'
PORT2 = 7003

socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket1.bind((HOST1, PORT1))
socket1.listen()

socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket2.bind((HOST2, PORT2))

# TODO
# get data from usb (host1) on pc1
# send it to pc2 with axis studio with bvh broadcast source pc2's wifi
# from pc1 send to wifi pc2 and then get raw data back

# also TODO
# source in bvh broadcast is server -> this set to setudpserver
# destination is destination -> set udp port

# CONLUSION
# transceiver IP ...254 should be multicast and it is "coded" in driver how trans. and axis studio can create connection
# source in bvh broadcast is ip of server (axis studio)
