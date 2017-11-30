import asyncio
import argparse

if __name__ != '__main__':
	from . import GeneralMachine
	from . import GeneralClient
else: 
	from general_machine import GeneralMachine
	from general_client import GeneralClient	

class GeneralServer(GeneralMachine):
	""" This server listen for a messages"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		parser = argparse.ArgumentParser()
		parser.add_argument("-s", "--stop", dest="stop", action='store_true', help="stop running server", default=False)
		args = parser.parse_args()
		if args.stop:
			self.stop()

	def start(self):
		self.loop = asyncio.get_event_loop()
		coro = asyncio.start_server(self.fetch, self.config['SERVER']['Host'], self.config['SERVER']['Port'], loop=self.loop)
		self.server = self.loop.run_until_complete(coro)

		self.logger.info('Serving on {}'.format(self.server.sockets[0].getsockname()))
		try:
		    self.loop.run_forever()
		except KeyboardInterrupt as exc:
			self.logger.error('an exception has been recieved {}'.format(exc))
			self.terminate()

	def stop(self):
		Terminator = GeneralClient()
		Terminator.send(b'stop().')
		quit(0)

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
	    	return self.terminate()

	    writer.close()
	    self.on_fetch(message)

	def terminate(self):
		self.logger.info('server stopping.')
		self.server.close()
		self.loop.stop() 
		self.logger.info('server stopped')

def main():
	S = GeneralServer()
	S.start()

if __name__ == '__main__':
	main()		            