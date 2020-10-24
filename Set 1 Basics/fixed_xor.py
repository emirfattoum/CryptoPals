#!/usr/bin/python3

import binascii
import optparse
import sys


def xor(a,b):

	if len(a)==len(b):	
		A=bytes.fromhex(a)
		B=bytes.fromhex(b)
		x=bytes(i^j for i,j in zip(A,B))
		print ('\nresult = ',str(x,'utf-8'))
		print ('result in hex = ',str(binascii.hexlify(x),'utf-8'))
	else:
		print ("entered buffers are not with exact same lenght")


def main():
	parser=optparse.OptionParser(sys.argv[0]+' '+'-a <string>'+' '+'-b <string>')
	parser.add_option('-a',dest='a',type='string',help='first string to be xored')
	parser.add_option('-b',dest='b',type='string',help='second string to be xored')
	(options,args)=parser.parse_args()

	a=options.a
	b=options.b

	if (a == None) or (b == None):
		print (parser.usage)
		sys.exit(0)
	else:
		xor(a,b)

if __name__ == "__main__":
	main()

