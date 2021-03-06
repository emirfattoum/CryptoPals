#!/usr/bin/python3

import optparse
import sys
from Crypto.Cipher import AES
from base64 import b64decode


def decrypt_ECB(data,key):
	cipher=AES.new(key,AES.MODE_ECB)
	decrypted=cipher.decrypt(data)
	return decrypted

def encrypt_ECB(data,key):
	cipher=AES.new(key,AES.MODE_ECB)
	encrypted=cipher.encrypt(data)
	return encrypted



def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'-f <file>')
	parser.add_option('-f',dest='f',type='string',help='<file>')
	(options,args) = parser.parse_args()
	f = options.f
	if (f == None):
		print (parser.usage)
		sys.exit(0)
	else:
		file = open( f , 'r' )
		data = file.read()
		data = b64decode(data)
		key = b'YELLOW SUBMARINE'
		decrypted=decrypt_ECB(data,key)
		print(str(decrypted,'utf-8'))


if __name__ == "__main__":
	main()