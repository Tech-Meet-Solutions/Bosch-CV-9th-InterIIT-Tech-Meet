from channels.generic.websocket import WebsocketConsumer
import json

class SocketConsumer(WebsocketConsumer):
	groups = ["broadcast"]

	def connect(self):
		# Called on connection.
		# To accept the connection call:
		self.accept()
		self.send("connected")
		# To reject the connection, call:
		self.close()

	def receive(self, text_data=None, bytes_data=None):
		print(text_data)
		# Called with either text_data or bytes_data for each frame
		# You can call:
		self.send(text_data="Hello world!")
		# Or, to send a binary frame:
		self.send(bytes_data="Hello world!")
		# Want to force-close the connection? Call:
		self.close()
		# Or add a custom WebSocket error code!
		self.close(code=4123)
		
	def send_message_to_frontend(self,event):
		print("EVENT TRIGERED")
		# Receive message from room group
		message = event['message']
		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'message': message
		}))

	def disconnect(self, close_code):
		pass
		# Called when the socket closes