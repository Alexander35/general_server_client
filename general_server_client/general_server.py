import asyncio

if __name__ != '__main__':
	from . import GeneralMachine
else: 
	from general_machine import GeneralMachine	

class GeneralServer(GeneralMachine):
	""" This server listen for a messages"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def start(self):
		self.loop = asyncio.get_event_loop()
		coro = asyncio.start_server(self.fetch, self.config['SERVER']['Host'], self.config['SERVER']['Port'], loop=self.loop)
		self.server = self.loop.run_until_complete(coro)

		self.logger.info('Serving on {}'.format(self.server.sockets[0].getsockname()))
		try:
		    self.loop.run_forever()
		except KeyboardInterrupt as exc:
			self.logger.error('an exception has been recieved {}'.format(exc))
			self.stop()		

	def on_fetch(self, msg):
		pass		

	async def fetch(self, reader, writer):
	    data = b''
	    while True:
		    tmp = await reader.read(1024)
		    if not tmp: break
		    data = data + tmp
	    message = data
	    addr = writer.get_extra_info('peername')
	    self.logger.info("Received %r from %r" % (message, addr))
	    if(message == b'stop().'):
	    	self.stop()
	    writer.close()
	    self.on_fetch(message)

	def stop(self):
		self.logger.info('server stopping.')
		self.server.close()
		self.loop.stop() 
		self.logger.info('server stopped') 	

def main():
	S = GeneralServer()
	S.start()

if __name__ == '__main__':
	main()		            