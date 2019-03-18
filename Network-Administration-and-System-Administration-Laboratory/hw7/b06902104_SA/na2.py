#!/usr/bin/env python3
from Crypto.Cipher import AES

class DoubleAES():
	def __init__(self, key0, key1):
		self.aes128_0 = AES.new(key=key0, mode=AES.MODE_ECB)
		self.aes128_1 = AES.new(key=key1, mode=AES.MODE_ECB)
	def encrypt(self, s):
		return self.aes128_1.encrypt(self.aes128_0.encrypt(s))
	def decrypt(self, data):
		return self.aes128_0.decrypt(self.aes128_1.decrypt(data))
def int2bytes(n):
	return bytes.fromhex('{0:032x}'.format(n))

def encrypt(key0, data):
	aes128_0 = AES.new(key=key0, mode=AES.MODE_ECB)
	return aes128_0.encrypt(data)
def decrypt(key1, data):
	aes128_1 = AES.new(key=key1, mode=AES.MODE_ECB)
	return aes128_1.decrypt(data)


plaintext = 'NoOneUses2AES_QQ'
inside = {}
key_0 = -1
key_1 = -1
cipher = bytes.fromhex('f1a0cff39c4351102e5cad9d63acc3ef')

for i in range(2**23):
	back = int2bytes(i)
	cipher0 = encrypt(back, plaintext)
	inside[cipher0] = i

for i in range(2**23):
	back = int2bytes(i)
	cipher1 = decrypt(back, cipher)
	if (cipher1 in inside):
		key_0 = inside[cipher1]
		key_1 = i
		break

flag = bytes.fromhex('019847278c949131611d267c3bb1f833bdb8e692f12f237b90d900aeb17be714')
aes2 = DoubleAES(key0=int2bytes(key_0), key1=int2bytes(key_1))
flag = aes2.decrypt(flag)
print (flag)
