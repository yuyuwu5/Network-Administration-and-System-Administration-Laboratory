#!/usr/bin/env python2
import signal, sys, os, time
import hashlib
import secret
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pwn import*
my=4
p = 262603487816194488181258352326988232210376591996146252542919605878805005469693782312718749915099841408908446760404481236646436295067318626356598442952156854984209550714670817589388406059285064542905718710475775121565983586780136825600264380868770029680925618588391997934473191054590812256197806034618157751903  
password = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for mm in range(10):
	for k in range(1,21):
		a = remote('linux13.csie.org', 7122)
		b = remote('linux13.csie.org', 7122)
		for j in range(10):
			a.recvuntil('Server sends: ', drop=True)
			getA = a.recvuntil("\n", drop=True)
			b.recvuntil('Server sends: ', drop=True)
			getB = b.recvuntil("\n", drop=True)
			if (j != mm):
				a.sendline(getB)
				b.sendline(getA)
			else:
				A = int(getA)
				B = int(getB)
				pwd = int(hashlib.sha512(str(k)).hexdigest(), 16)
				g = pow(pwd, 2, p)
				M = pow(g, my ,p)
				a.sendline(str(M))
				b.sendline(str(M))
				Ka = pow(A, my, p)
				key_a = int(hashlib.sha512(str(Ka)).hexdigest(),16)
				Kb = pow(B, my, p)
				key_b = int(hashlib.sha512(str(Kb)).hexdigest(),16)
		a.recvuntil('FLAG is: ', drop=True)
		tmp_a = a.recvuntil("\n", drop=True)
		b.recvuntil('FLAG is: ', drop=True)
		tmp_b = b.recvuntil("\n",drop=True)
		if (int(tmp_a)^int(tmp_b)^key_a^key_b == 0):
			password[mm] = k
			continue
		a.close()
		b.close()

password = [int(hashlib.sha512(str(i)).hexdigest(), 16) for i in password]
key = 0
new = remote('linux13.csie.org', 7122)
for i, pwd in enumerate(password):
    	new.recvuntil('Server sends: ', drop=True)
	A = int(new.recvuntil("\n", drop=True))
	g = pow(pwd, 2, p)        
    	M = pow(g, my ,p)
	new.sendline(str(M))
	K = pow(A, my, p)
	key ^= int(hashlib.sha512(str(K)).hexdigest(), 16)
new.recvuntil('FLAG is: ', drop=True)
tmp = int(new.recvuntil("\n", drop=True))
kk=tmp^key
kk=str(hex(kk))
kk=kk[2:]
FLAG = kk.decode('hex')
print FLAG

