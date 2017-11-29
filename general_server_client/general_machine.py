import configparser
import logging
from time import gmtime, strftime
import os

class GeneralMachine:
	"""GeneralMachine is the general clss for client and server"""
	def __init__(self, ConfigName='config.ini', LoggerName=__name__, loggerType=logging.DEBUG):
		try:
			self.logger = self.logger_setup(LoggerName, loggerType)	
			self.config = configparser.ConfigParser()
		except Exception as exc:
			self.logger.error('An error occured when log and conf init has begun {}'.format(exc))	

		try:
			self.config.read(ConfigName)
		except Exception as exc:
			self.logger.error('Unable to read config file {} because of {}'.format(ConfigName, exc))

	def get_config(self, section, key):
		ConfItem = 'Empty'
		try:
			ConfItem = self.config[section][key]
		except Exception as exc:
			self.logger.error('Unable to get key from conf {}'.format(exc))
		return ConfItem		

	def logger_setup(self, logger_name, logging_type=logging.DEBUG):
		try:
			os.stat('log/')
		except Exception as exc:
			os.mkdir('log/')
		
		logfile_name = logger_name 
		logfile_name = '{}{}'.format('log/', logfile_name)
		current_time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
		logfile_name = '{0}-{1}'.format(logfile_name, current_time)
		
		l = logging.getLogger(logger_name)
		formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
		fileHandler = logging.FileHandler(logfile_name, mode='w')
		fileHandler.setFormatter(formatter)
		l.setLevel(logging_type)
		l.addHandler(fileHandler)

		return logging.getLogger(logger_name) 			

def main():
	GM = GeneralMachine('config.ini')
	print(GM.get_config('SERVER','Host'))	

if __name__ == '__main__':
	main()		