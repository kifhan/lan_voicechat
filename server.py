# Echo server program
import socket
import pyaudio
import wave
import time

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
RECORD_SECONDS = 4000

#HOST = '127.0.0.1' or 192.168.0.11
HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)    #connection setup done and client connected.
        p = pyaudio.PyAudio()
        # for receiving data
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
        # for sending data
        stream2 = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        i=0
        while True:
            try:			# receiving data
                data = conn.recv(1024)
            except KeyboardInterrupt:
                break
            except:
                pass

            if not data:
                continue
            stream.write(data)
            # print(i)
            i=i+1

            try:		# sending data
                data2  = stream2.read(CHUNK)
                conn.sendall(data2)
            except KeyboardInterrupt:
                break
            except:
                pass
