import asyncio
import argparse
import platform
if platform.system() != 'Windows':
	from daemonize import Daemonize


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
		parser.add_argument("-s", "--stop", dest="stop", action='store_true', help="send stop signal to running server from instant client", default=False)
		parser.add_argument("-d", "--daemon", dest="daemon", action='store_true', help="run server as daemon", default=False)
		args = parser.parse_args()
		if args.stop:
			self.stop()

		if args.daemon and platform.system() != 'Windows':
			self.daemonize()
		else:
			self.on_initialize()		

	def start(self):
		self.loop = asyncio.get_event_loop()
		coro = asyncio.start_server(self.fetch, self.get_config('SERVER','Host'), self.get_config('SERVER','Port'), loop=self.loop)
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
		"""Event handler when the data received.
		You should to implement it in the child class"""
		pass

	def daemonize(self):
		daemon = Daemonize(app=self.get_config('DAEMON','app'), pid=self.get_config('DAEMON','pid'), action=self.on_initialize, chdir=self.get_config('DAEMON','chdir'))
		daemon.start()

	def on_initialize(self):
		"""Event handler when it initialize
		You should to implement it in the child class"""
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