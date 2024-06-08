import bluetooth #needed for bluetooth communication
import thingspeak #needed for thingspeak

bluetooth_addr = "00:22:02:01:02:F6" #The Address from the HC-06 Sensor
bluetooth_port = 1 #Channel 1 for RFCOMM
bluetoothSocket = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
bluetoothSocket.connect((bluetooth_addr, bluetooth_port))

#thingspeak information
channel_id = 2572427 #Chennel ID from Thingspeak
key = "Y60VWOJK9RO4NETY" #From Thingspeak
url = 'https://api.thingspeak.com/update' #Default URL to update thingspeak
ts = thingspeak.Channel(channel_id, key, url)

while 1:
	try:
		received_data = bluetoothSocket.recv(1024)
		temperature = int.from_bytes(received_data, byteorder='big')
		print("Current Temperature: %d" % temperature)
		thingspeak_field1 = {"field1": temperature}
		ts.update(thingspeak_field1) #Update Thingspeak
	
	except KeyboardInterrupt:
		print("Keyboard Interrupt Detected")
		break
bluetoothSocket.close()
