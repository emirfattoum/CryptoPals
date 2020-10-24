#!/usr/bin/python3

import optparse
import sys


def occurence(cipher,blocksize,l):
	blocks=[]
	for i in range(0,len(cipher),blocksize):
		blocks.append(cipher[i:i+blocksize])
	reps=len(blocks)-len(set(blocks))
	result={
	'cipher':cipher,
	'reps':reps,
	'line':l+1
	}
	return result


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
		lines = file.readlines()
		occurences=[]
		blocksize=16
		for l in range(0,len(lines)) :
			occurences.append(occurence(lines[l],blocksize,l))

		top=sorted(occurences,key=lambda x: x['reps'],reverse=True)[0]
		print('ECB mode detected in line ',top['line'])
		print('similar occurences = ',top['reps'])
		print('ciphertext = ',top['cipher'])




if __name__ == "__main__":
	main()