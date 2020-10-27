#!/usr/bin/python3

import optparse
import sys
from Crypto.Cipher import AES
from base64 import b64decode



def decrypt_CBC(data,key,IV):
	cipher=AES.new(key,AES.MODE_CBC,IV)
	decrypted=cipher.decrypt(data)
	return decrypted



def encrypt_CBC(data,key,IV):
	cipher=AES.new(key,AES.MODE_CBC,IV)
	encrypted=cipher.encrypt(data)
	return encrypted



def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'-f <file>'+' '+'-key <string>')
	parser.add_option('-f',dest='f',type='string',help='<file>')
	parser.add_option('-k',dest='k',type='string',help='key')
	(options,args) = parser.parse_args()
	f = options.f
	key = options.k
	if (f == None) or (k==None):
		print (parser.usage)
		sys.exit(0)
	else:
		file = open( f , 'r' )
		data = file.read()
		data = b64decode(data)
		V = b'\x00'*AES.block_size
		print('\nInitialization vector = ',V)
		decrypted=decrypt_CBC(data,key,V)
		print('\nDecrypted data :\n',str(decrypted,'utf-8'))


if __name__ == "__main__":
	main()