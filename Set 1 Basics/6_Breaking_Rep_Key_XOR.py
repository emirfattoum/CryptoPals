#!/usr/bin/python3

import optparse
import sys
import binascii
from base64 import b64decode




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

def ascii_to_bytes(string):
	text=bytearray.fromhex(string.encode('utf-8').hex())
	return text

def hamming_distance(a,b):
	# both a & b must be of exact length or else this will fail
	assert len(a) == len(b), 'hamming distance of 2 blocks with diffrent lenghts '
	distance=0
	for i,j in zip(a,b):
		x=bin(i^j)
		#print(x)
		distance+=x.count('1')
	return distance

def keysize_guess(cipher):
	
	average_distance=[]

	for keysize in range (2,40):
		
		distances=[] 

		#selecting relative start & end of block
		start = 0
		end = start	+ keysize	
		
		while (1):

			# selecting 2 neighbor blocks that are keysize long

			block_A = cipher[start:end]
			block_B = cipher[start+keysize:end+keysize]

			# if we reach the end of the cipher
			# we ignore the last bit if it's not keysize long
			if (len(block_B) < keysize):
				break
			# getting the hamming distance of the tow blocks
			
			distance = hamming_distance(block_A,block_B)

			#normalising the distance so it's comparable across all keysizes
			distances.append(distance/keysize) 

			# next couple of blocks
			start = end + keysize
			end = start + keysize

		result={
		'key':keysize,
		'key_distance': sum(distances)/len(distances)
		}

		average_distance.append(result)


	# filtering for the lowest scored distance and it's relevant keysize
	sorted_distances=sorted(average_distance,key=lambda x: x['key_distance'])[0]

	return sorted_distances

def single_char_xor(cipher,char):
	out = ''
	for byte in cipher:
		out += str(chr(byte ^ char))
	return (out)
	
def bruteforce_key(cipher):
	m = []
	for key in range(1,256):
		bytess = single_char_xor(cipher,key)
		data = {
			'message': bytess,
			'score': score(bytess),
			'key': key
			}
		m.append(data)
	S=sorted(m, key=lambda x: x['score'], reverse=True)[0]
	return S

def repeating_key_xor(cipher, key):
	decrypted= b''
	i = 0
	for byte in cipher:
		decrypted += bytes([byte ^ key[i]])
		if (i + 1) == len(key):
			i = 0
		else:
			i += 1
	return decrypted

def guess_key(cipher,keysize):
	key=b''
	for i in range(keysize):

		block=b''
		for j in range(i,len(cipher),keysize):
			block+=bytes([cipher[j]])
		bruted=	bruteforce_key(block)
		key += bytes([bruted['key']])
	return key

def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'-f <file>')
	parser.add_option('-f',dest='f',type='string',help=' file')
	(options,args) = parser.parse_args()

	f = options.f
	
	if (f == None):
		print (parser.usage)
		sys.exit(0)
	else:
		
		#verifing hamming distance 
		assert hamming_distance(ascii_to_bytes('this is a test'), ascii_to_bytes('wokka wokka!!!')) == 37, "incorrect Hamming distance calculation"
		
		file = open( f , 'r' )
		data = file.read()
		data = b64decode(data)
		keysize=keysize_guess(data)
		print("\nPotential key size ",keysize['key'])
		possible_key=guess_key(data,keysize['key'])
		print('\nPotential key = ',str(possible_key,'utf-8'))
		res = str(repeating_key_xor(data,possible_key),'utf-8')
		s = score(res)
		print('\nReadability score = ',s)
		print('\nDecrypted Data :\n',res)

		key = str(possible_key,'utf-8')
if __name__ == "__main__":
	main()