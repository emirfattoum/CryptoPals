#!/usr/bin/python3

import optparse
import sys
import binascii


def rep_key_xor(a,k):

	print ('\n')
	print ('original string = ',a)
	print ('encryption key = ',k)
	#a=binascii.hexlify(bytes(a,'utf-8'))
	#print(a)
	l=0
	encoded=[]
	for i in range(0,len(a)):
		encoded.append(ord(a[i])^ord(k[l]))
		l+=1
		if l==len(k):
			l=0
	R = bytes(encoded).hex()
	# R=binascii.hexlify(bytearray(encoded))
	return R


def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'-a <string>'+' '+'-k <key>')
	parser.add_option('-a',dest='a',type='string',help=' string to be encypted using repeating key xor technique ')
	parser.add_option('-k',dest='k',type='string',help=' key ')
	(options,args) = parser.parse_args()

	a = options.a
	k = options.k
	if (a == None)or(k==None):
		print (parser.usage)
		sys.exit(0)
	else:
		R = rep_key_xor(a,k)
		print ('Encrypted Result = ',R)

if __name__ == "__main__":
	main()