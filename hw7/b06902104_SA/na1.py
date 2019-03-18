#!/usr/bin/env python3
import sys,os,signal
import hashlib
import string
from struct import*
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from AESCipher import *

class SecureEncryption(object):
    def __init__(self, keys):
        assert len(keys) == 4
        self.keys = keys
        self.ciphers = []
        for i in range(4):
            self.ciphers.append(AESCipher(keys[i]))

    def dec(self, ciphertext):
        three      = AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        two        = AESCipher._unpad(self.ciphers[2].decrypt(three))
        one        = AESCipher._unpad(self.ciphers[1].decrypt(two))
        plaintext  = AESCipher._unpad(self.ciphers[0].decrypt(one))
        return plaintext
   
    def dec_4(self,ciphertext,target):
        a=self.ciphers[3].decrypt(ciphertext)
        b=a[144:-1]
        if b==target:
            return True
        return False
    def dec_3(self,ciphertext,target):
        three= AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        a=self.ciphers[2].decrypt(three)
        b=a[112:-1]
        if b==target:
            return True
        return False
    def dec_2(self,ciphertext,target):
        three= AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        two        = AESCipher._unpad(self.ciphers[2].decrypt(three))
        a=self.ciphers[1].decrypt(two)
        b=a[80:-1]
        if b==target:
            return True
        return False
    def dec_1(self,ciphertext,target,i):
        three= AESCipher._unpad(self.ciphers[3].decrypt(ciphertext))
        two        = AESCipher._unpad(self.ciphers[2].decrypt(three))
        one        = AESCipher._unpad(self.ciphers[1].decrypt(two))
        a=self.ciphers[0].decrypt(one)
        #print(len(a))
        b=a[60:-1]
        #print(b)
        if b==target:
            return True
        return False



filename = sys.argv[1]
cipher = open(filename, "rb").read()
###try password (the forth key,digit 7 8)
key='aaaaaa'
new=bytes([16,16,16,16,16,16,16,16,16,16,16,16,16,16,16])
digit_7='0'
digit_8='0'
for seven in list(string.printable):
    key=key+seven
    for eight in list(string.printable):
        key=key+eight
        user_input = key.encode('utf-8')
        i = len(user_input) // 4
        keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
                hashlib.sha256(user_input[0:i]).digest(),
	        hashlib.sha256(user_input[i:2*i]).digest(),
	        hashlib.sha256(user_input[2*i:3*i]).digest(),
                hashlib.sha256(user_input[3*i:4*i]).digest(),
    	    ]
        s = SecureEncryption(keys)
        if s.dec_4(cipher,new)==True:
            digit_7=seven
            digit_8=eight
            break;
        key='aaaaaa'+seven
    key='aaaaaa'
###try password (the third key,digit 5 6)
cipher = open(filename, "rb").read()
key='aaaa'
digit_5='0'
digit_6='0'
for five in list(string.printable):
    key=key+five
    for six in list(string.printable):
        key=key+six+digit_7+digit_8
        user_input = key.encode('utf-8')
        i = len(user_input) // 4
        keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
                hashlib.sha256(user_input[0:i]).digest(),
                hashlib.sha256(user_input[i:2*i]).digest(),
                hashlib.sha256(user_input[2*i:3*i]).digest(),
                hashlib.sha256(user_input[3*i:4*i]).digest(),
    	    ]
        s = SecureEncryption(keys)
        if s.dec_3(cipher,new)==True:
            digit_5=five
            digit_6=six
            break;
        key='aaaa'+five
    key='aaaa'
###try password (the second key,digit 3 4)
cipher = open(filename, "rb").read()
key='aa'
digit_3='0'
digit_4='0'
for three in list(string.printable):
    key=key+three
    for four in list(string.printable):
        key=key+four+digit_5+digit_6+digit_7+digit_8
        user_input = key.encode('utf-8')
        i = len(user_input) // 4
        keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
                hashlib.sha256(user_input[0:i]).digest(),
                hashlib.sha256(user_input[i:2*i]).digest(),
                hashlib.sha256(user_input[2*i:3*i]).digest(),
                hashlib.sha256(user_input[3*i:4*i]).digest(),
    	    ]
        s = SecureEncryption(keys)
        if s.dec_2(cipher,new)==True:
            digit_3=three
            digit_4=four
            break;
        key='aa'+three
    key='aa'
###try password (the first key,digit 1 2)
cipher = open(filename, "rb").read()
key=''
digit_1=[]
digit_2=[]
count=0
'''
for i in range(2,16):
    l=[i for c in range(i)]
    print(l)
'''
for b in range(2,17):
    l=[b for c in range(3)]
    new=bytes(l)
    for one in list(string.printable):
        key=key+one
        for two in list(string.printable):
            key=key+two+digit_3+digit_4+digit_5+digit_6+digit_7+digit_8
            user_input = key.encode('utf-8')
            i = len(user_input) // 4
            keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
                    hashlib.sha256(user_input[0:i]).digest(),
                    hashlib.sha256(user_input[i:2*i]).digest(),
                    hashlib.sha256(user_input[2*i:3*i]).digest(),
                    hashlib.sha256(user_input[3*i:4*i]).digest(),
        	    ]
            s = SecureEncryption(keys)
            if s.dec_1(cipher,new,b)==True:
                count+=1;
                digit_1=one
                digit_2=two
                break;
            key=''+one
        key=''


cipher = open(filename, "rb").read()
key=digit_1+digit_2+digit_3+digit_4+digit_5+digit_6+digit_7+digit_8
user_input = key.encode('utf-8')
i = len(user_input) // 4
keys = [ # Four times 256 is 1024 Bit strength!! Unbreakable!!
    hashlib.sha256(user_input[0:i]).digest(),
    hashlib.sha256(user_input[i:2*i]).digest(),
    hashlib.sha256(user_input[2*i:3*i]).digest(),
    hashlib.sha256(user_input[3*i:4*i]).digest(),
]
s = SecureEncryption(keys)
plaintext = s.dec(cipher)
print(plaintext)

