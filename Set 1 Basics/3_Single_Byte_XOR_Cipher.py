#!/usr/bin/python3

import binascii
import optparse
import sys


def score(string):
	eng_freqency={
	'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
	'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
	'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
	'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
	}
	score=0
	for i in range(len(string)):
		char=string[i].lower()
		if char in eng_freqency:
			score+=eng_freqency[char]
	return score


def xor(cipher):
	m = []
	cipher=bytes.fromhex(cipher)
	for key in range(1,256):
		out = ''
		for byte in cipher:
			out += str(chr(byte ^ key))
		data = {
			'message': out,
			'score': score(out),
			'key': chr(key)
			}
		m.append(data)
	S=sorted(m, key=lambda x: x['score'], reverse=True)[0]
	return S


def main():
	parser=optparse.OptionParser(sys.argv[0]+' '+'-a <string>')
	parser.add_option('-a',dest='a',type='string',help=' xor\'d string to be decoded_single byte key ')
	(options,args)=parser.parse_args()

	a=options.a

	if (a == None):
		print (parser.usage)
		sys.exit(0)
	else:
		result=xor(a)
		print('\ndecrypted result = ',result['message'])
		print('key = ',result['key'])
		print('readability score = ',result['score'])

if __name__ == "__main__":
	main()
