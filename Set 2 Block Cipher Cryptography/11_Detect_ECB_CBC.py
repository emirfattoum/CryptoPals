#!/usr/bin/python3

import optparse
import sys
import os
import secrets
import random
import binascii
from Crypto.Cipher import AES


def random_key(size):
	#crypto-safe byte generation
	#random module is no 100% random so not good for cryptographic use
	key1=os.urandom(size)	#using os module
	key2=secrets.token_bytes(size)	#using secrets module
	return(key2)


def encrypt_CBC(data,key,IV):
	cipher=AES.new(key,AES.MODE_CBC,IV)
	encrypted=cipher.encrypt(data)
	return encrypted


def encrypt_ECB(data,key):
	cipher=AES.new(key,AES.MODE_ECB)
	encrypted=cipher.encrypt(data)
	return encrypted


def occurence(cipher,blocksize):
	blocks=[]
	for i in range(0,len(cipher),blocksize):
		blocks.append(cipher[i:i+blocksize])
	reps=len(blocks)-len(set(blocks))
	result={
	'cipher':cipher,
	'reps':reps,
	}
	return result

def pad_man(text,blocksize):
	#padding text so it's composed of blocks of length blocksize :: last block is of length 16
	blocks=[]
	for i in range(0,len(text),blocksize):
		blocks.append(text[i:i+blocksize])
	if len(blocks[-1]) == 16:
		return text
	else:
		pad_size=blocksize-len(blocks[-1])
		pad=b''
		for i in range(pad_size):
			pad+=bytes([pad_size])
		padded=text+pad
		return padded


def oracle_of_detection(cipher,blocksize):
	analysis=occurence(cipher,blocksize)
	if analysis['reps']!=0 :
		return ('ECB')
	else:
		return ('CBC')


def oracle_of_encrytion(text,blocksize):
	count=random.randrange(5,11)
	before=secrets.token_bytes(count)
	count=random.randrange(5,11)
	after=secrets.token_bytes(count)
	text=before+text+after
	padded=pad_man(text,blocksize)
	#print('final ciphertext = ',padded,' // length = ',len(padded))
	key=random_key(blocksize)
	if secrets.randbelow(2)==1:
		IV=secrets.token_bytes(blocksize)
		cipher=encrypt_CBC(padded,key,IV)
		crypt={
		'cipher':cipher,
		'Encryption_mode':'CBC'
		}
		return (crypt)
	else:
		cipher=encrypt_ECB(padded,key)
		crypt={
		'cipher':cipher,
		'Encryption_mode':'ECB'
		}
		return (crypt)

def main():
	parser = optparse.OptionParser(sys.argv[0]+' '+'--text <input>'+' '+'-n <int>')
	parser.add_option('--text',dest='text',type='string',help='input text')
	parser.add_option('-n',dest='n',type='int',help='number of tests')
	(options,args) = parser.parse_args()
	text = options.text
	n = options.n
	if (text == None) or (n==None):
		print (parser.usage)
		sys.exit(0)
	else:
		blocksize=AES.block_size
	# you need enough volume of data so that the occurency of blocks happen in case of EBC mode
	# we only need 1 pair of identical blocks to say it's ECB , CBC will never have identical blocks
	# 100 % accurency from data with leght 48 bytes   
		text=text*3
		text=bytes(text,'utf-8')
		x=0
		for i in range(1,n+1):
			crypt=oracle_of_encrytion(text,blocksize)
			print('\nTest N°:',i,'\nEncryption_mode = ',crypt['Encryption_mode'])
			oracle=oracle_of_detection(crypt['cipher'],blocksize)
			print('Detected MODE = ',oracle)
			if crypt['Encryption_mode'] == oracle:
				x+=1
		print('\nTotal N° of tests :',n)
		print('Total N° of Correct Guess :',x)
		print('Success Rate :',(x/n)*100,'%')

if __name__ == "__main__":
	main()