import socket
import os
import sys
import configparser
from time import ctime

class Monitor():

	def __init__(self) -> None:
		self.HOST = self.read_config('host')
		self.PORT = int(self.read_config('port'))
		print(ctime(),'Aguardando comandos...')

	def read_config(self, key):
		path = os.path.dirname(os.path.realpath(__file__))
		try:
			cfg = configparser.ConfigParser()
			cfg.read(path + '/config.ini')
			return cfg.get('monitor', key)
		except Exception as e:
			print(e)
			print("Erro ao ler configuracao no arquivo config.ini")

	def restart_robots(self):
		print(ctime(),"Fechando todos os robos...")
		os.system("pkill mate-terminal")
		print(ctime(),"Abrindo todos os robos...")
		os.system("/home/robo/Desktop/OpenAll.sh")

	def process_cmd(self, command):
		if command == 'restart':
			self.restart_robots()
		else:
			print(f'Understand command "{command}"')


	def main(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.HOST, self.PORT))
			s.listen(1)

			while True:
				conn, client = s.accept()
				pid = os.fork()
				if pid == 0:
					s.close()
					while True:
						msg = conn.recv(1024)
						if not msg: break
						self.process_cmd(msg.decode("utf-8"))
					conn.close()
					sys.exit(0)
				else:
					conn.close()

if __name__ == '__main__':
	Monitor().main()