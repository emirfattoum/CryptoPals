#!/usr/bin/python3

import optparse
import sys
from Padding import appendPadding as padding	# pip3 install Padding #https://pypi.org/project/Padding/


def pad_man_junior(text,blocksize):
	pad_size=blocksize-len(text)
	pad=b''
	if pad_size>0:
		for i in range(pad_size):
			pad+=bytes([pad_size])
		padded=text+pad
		return padded
	else:
		return text


def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'--block <string>'+' '+'--target-block-size <int>')
	parser.add_option('--block',dest='b',type='string',help='block to be padded with PKCS#7')
	parser.add_option('--target-block-size',dest='s',type='int',help='target block size')
	(options,args) = parser.parse_args()
	b = options.b
	s = options.s
	if (b == None) or (s == None):
		print (parser.usage)
		sys.exit(0)
	else:
		print('\nOriginal Block = ',b,'// length=',len(b))
		b=bytes(b,'utf-8')
		padded=pad_man_junior(b,s)
		print('Padded Block = ',padded,'// length=',len(padded))





if __name__ == "__main__":
	main()