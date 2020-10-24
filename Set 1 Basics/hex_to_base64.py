#!/usr/bin/python3


import base64 
import optparse
import sys


def hex_to_b64(S):

	byte=bytes.fromhex(S)
	b64 = base64.b64encode(byte).decode()
	return b64


def main():
	parser=optparse.OptionParser(sys.argv[0]+' '+'--hex-to-b64 <string>')
	parser.add_option('--hex-to-b64',dest='S',type='string',help='hex string to be converted to base64')
	(options,args)=parser.parse_args()

	S=options.S

	if (S == None):
		print('no argument is present')
		print (parser.usage)
		sys.exit(0)
	else:
		print(hex_to_b64(S))

if __name__ == "__main__":
	main()


