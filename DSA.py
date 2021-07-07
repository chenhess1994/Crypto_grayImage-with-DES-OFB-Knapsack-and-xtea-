


# =============================================================================
# ['C:\\Users\\irago\\anaconda3\\python38.zip', 'C:\\Users\\irago\\anaconda3\\DLLs', 'C:\\Users\\irago\\anaconda3\\lib', 'C:\\Users\\irago\\anaconda3', '', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\win32', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\win32\\lib', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\Pythonwin', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\IPython\\extensions', 'C:\\Users\\irago\\.ipython']
# ['C:\\Users\\irago\\anaconda3\\python38.zip', 'C:\\Users\\irago\\anaconda3\\DLLs', 'C:\\Users\\irago\\anaconda3\\lib', 'C:\\Users\\irago\\anaconda3', '', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\win32', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\win32\\lib', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\Pythonwin', 'C:\\Users\\irago\\anaconda3\\lib\\site-packages\\IPython\\extensions', 'C:\\Users\\irago\\.ipython']
# =============================================================================

import random as rand



from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import DSA
from Tools import modinv

key=DSA.generate(1024)
publicKey = key.publickey()

class My_DSA():
    #Init function, using library to generate part of the DSA key.
    #Generate prime number p represented between 1023-1024 bits
    #Generate prime number q represented between 159-160 bits where q divides p-1.
    def __init__(self):
        self.is_key_set=False     
    #Set a new public key, and because the public key must have a
    #Part build on the private key, generating the private key also
    #Returning a tuple public key 0-2, private key 3.
    def get_key(self):
# =============================================================================
#         
#         randNum=rand.randint(1,self.p-1)
#         factor=int(self.p-1 / self.q)
#         self.g=pow(randNum,factor) % self.p
#         x=self.getPrivateKey()
# =============================================================================
        if self.is_key_set ==False:
            key=DSA.generate(1024)
            self.is_key_set =True
        else:
            key=DSA.generate(1024,domain=(self.p,self.q,self.g))
        
        self.p = key.p
        self.q = key.q
        self.g=key.g
        self.y=key.y
        return (self.q, self.p, self.g, self.y), key.x
        

# =============================================================================
#send public key: creation must be called after getPrivateKey 
#     
# =============================================================================
    def get_public_key(self):
        return self.q, self.p, self.g,self.y

    #Set a new private key and set the public key part from the privte key
    #Disconnect from the getKey in order to been able to change the 
    #Private key and the public key without regenerating the large prime numbers.
# =============================================================================
#     def getPrivateKey(self):
#         x=rand.randint(1,self.q-1)
#         self.y = int(pow(self.g,x) % self.p
#         return x
#     
# =============================================================================
    #Signing function, creating signature r and s 
    #Using SHA256 for creating a random msg signature k.
    def sign(self,msg,x):
        k=rand.randint(1,self.q-1)
        r=pow(self.g, k , self.p) % self.q
        kInverse=modinv(k, self.q)
        hashMsg=SHA256.new(msg)
        digest=hashMsg.digest()
        digest=int.from_bytes(digest,"little")
        s=(kInverse*(digest+(x*r))) % self.q
        return r,s
    
    
    
    
    #Comparing the digest of the signature and the msg sent 
    #Using public key of the messenger.
    def verify(self, msg, r, s, publicKey):
       w=int(modinv(s, publicKey["q"]) % publicKey["q"])
       hashMsg=SHA256.new(msg)
       digest=hashMsg.digest()
       digest=int.from_bytes(digest,"little")
       u1=int((digest*w) % publicKey["q"])
       u2=int((r*w) % publicKey["q"])
       v=((pow(publicKey["g"],u1,publicKey["p"])*pow(publicKey["y"],u2,publicKey["p"])) % publicKey["p"]) % publicKey["q"]
       return v==r
        

# =============================================================================
# 
# a=My_DSA()
# b,c=a.get_key()
# d,e=a.get_key()
# 
# =============================================================================

