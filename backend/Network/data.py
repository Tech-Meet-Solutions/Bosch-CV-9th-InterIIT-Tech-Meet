import asyncio
import websockets

async def main(message):
	async with websockets.connect('ws://51.103.155.221:5000') as websocket:
		try:
			await websocket.send(message)
			print('data updated')
		except Exception as e:
			print(e)

def send(message):
	asyncio.get_event_loop().run_until_complete(main(message))