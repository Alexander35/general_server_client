import asyncio
from . import GeneralMachine

class GeneralClient(GeneralMachine):
	"""This client just send a data to server """
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.loop = asyncio.get_event_loop()
		
	async def async_send(self):
		try:
			reader, writer = await asyncio.open_connection(self.get_config('SERVER','Host'), self.get_config('SERVER','Port'), loop=self.loop)
			writer.write(self.curr_msg)
			writer.close()
		except Exception as exc:
			self.logger.error('An error occured when had connection attempt {}'.format(exc))	

	def send(self, msg):
		try:
			self.curr_msg = msg
			self.loop.run_until_complete(self.async_send())  
			self.loop.close()
		except Exception as exc:
			self.logger.error('Unable to send the data {}'.format(exc))	

def main():
	GC = GeneralClient()
	GC.send('MSG')

if __name__ == '__main__':
	main()