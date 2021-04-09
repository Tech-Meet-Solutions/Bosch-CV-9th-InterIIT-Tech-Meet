import asyncio
import time
import websockets

async def receive(websocket):
	name = await websocket.recv()
	print(f"name = {name}")

async def main(message):
	async with websockets.connect('ws://51.103.155.221:5000') as websocket:
		try:
			# This now waits for 1s to receive any message  If no message received the task is 
			# timed out and we proceed further. 
			# Note that any message is not lost. If we do not recieve now, it will be recieved when we call receive again
			# But if we disconnect socket and reconnect again, then obviously we do not receive the message
			# Read more at : https://websockets.readthedocs.io/en/stable/api.html#websockets.protocol.WebSocketCommonProtocol.recv
			# try:
			# 	await asyncio.wait_for(receive(websocket), timeout=1.0)
			# except asyncio.TimeoutError:
			# 	print('timeout!')
			await websocket.send(input("Enter message: "))
			print('data updated')
		except Exception as e:
			print(e)

def send(message):
	asyncio.get_event_loop().run_until_complete(main(message))