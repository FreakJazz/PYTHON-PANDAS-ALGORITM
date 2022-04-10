from bluetooth import *

def input_and_send():
    print("\nType something\n")
    while True:
        data = input()
        if len(data) == 0: break
        sock.send(data)
        sock.send("\n")
        
def rx_and_echo():
    print("recibir")
#     sock.send("\nsend anything\n")
    while True:
        data = sock.recv(buf_size)
        if data:
            sock.send('hola')
            print(data)
    
            
#MAC address of ESP32
addr = "E8:7F:6B:E1:B5:E0"
#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
#service_matches = find_service( uuid = uuid, address = addr )
service_matches = find_service( address = addr )

buf_size = 1024;

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

for s in range(len(service_matches)):
    print("\nservice_matches: [" + str(s) + "]:")
    print(service_matches[s])
    
first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

port=2
print("connecting to \"%s\" on %s, port %s" % (name, host, port))

# Create the client socket
sock=BluetoothSocket(RFCOMM)
sock.connect((host, port))

print("connected")

# input_and_send()
rx_and_echo()

sock.close()
print("\n--- bye ---\n")

