import socket
import sys
import os
import configparser


def read_config(key):
	try:
		path = os.path.dirname(os.path.realpath(__file__))
		cfg = configparser.ConfigParser()
		cfg.read(path + '/config.ini')
		return cfg.get('monitor', key)
	except Exception as e:
		print(e)
		print("Erro ao ler configuracao no arquivo config.ini")

HOST = read_config('host')
PORT = int(read_config('port'))

if len(sys.argv) > 1:
	sys.argv.remove('teste.py')
	msg = ' '.join([str(item) for item in sys.argv])

	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST, PORT))
			s.sendall(msg.encode())
	except:
		print(f'Sem conexao com {HOST} na porta {PORT}')
		