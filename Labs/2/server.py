#!/usr/bin/env python
import socket
import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib import animation
from Cryptodome.Cipher import AES

# Server Network Configurations
SERVER_IP_ADDRESS = "192.168.4.56"
PORT = 50123

time = [i for i in range(50)]
ax_points = [0.0] * 50
ay_points = [0.0] * 50
az_points = [0.0] * 50

print("Starting UDP Server Setup")
sys.stdout.flush()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP_ADDRESS, PORT))

print("Waiting for Data to Receive")
sys.stdout.flush()

KEY = b'3874460957140850'
IV = b'9331626268227018'

fig, ax = plt.subplots()
ax.set_xlim(0, 50)
ax.set_ylim(-2, 2)
lineX, = ax.plot([], [], lw=2, label='X-axis')
lineY, = ax.plot([], [], lw=2, label='Y-axis')
lineZ, = ax.plot([], [], lw=2, label='Z-axis')

plt.legend()

def init():
    lineX.set_data([], [])
    lineY.set_data([], [])
    lineZ.set_data([], [])
    return lineX, lineY, lineZ

def updateData(i):
    decryption_suite = AES.new(KEY, AES.MODE_CBC, IV=IV)
    data, addr = sock.recvfrom(128)  # Ensure enough buffer size for encrypted data
    print(''.join('{:02x}'.format(x) for x in data))
    
    plain_text = decryption_suite.decrypt(data).rstrip(b'\x00')  # Remove padding bytes
    data_str = plain_text.decode('utf-8', errors='ignore')
    
    try:
        ax_val, ay_val, az_val, _ = data_str.split(",")
        ax_val, ay_val, az_val = float(ax_val), float(ay_val), float(az_val)
    except ValueError as e:
        print(f"Data format error: {e}")
        return lineX, lineY, lineZ

    print(f"ADXL345 X-Axis: {ax_val}\tY-Axis: {ay_val}\tZ-Axis: {az_val}\t" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    sys.stdout.flush()
    
    ax_points.append(ax_val)
    ay_points.append(ay_val)
    az_points.append(az_val)
    
    del ax_points[0]
    del ay_points[0]
    del az_points[0]

    lineX.set_data(time, ax_points)
    lineY.set_data(time, ay_points)
    lineZ.set_data(time, az_points)
    
    return lineX, lineY, lineZ

anim = animation.FuncAnimation(fig, updateData, init_func=init, frames=200, interval=20, blit=True)
plt.show()
