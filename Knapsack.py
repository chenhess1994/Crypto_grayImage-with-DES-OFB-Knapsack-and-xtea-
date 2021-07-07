# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:52:22 2021

@author: irago
"""

import struct
import random as rand
import numpy as np
from Tools import modinv

class Knapsack_MH():
# =============================================================================
#     
#     
# =============================================================================
    def __init__(self,msg_len=16):
        self.msg_len=msg_len

        
# =============================================================================
#   function purpose: create private and public key
#   function description:saves public Key and sends private key to user (not saving it)            
# =============================================================================
    def get_key(self):
        simple_knapsack=self.create_simple_knapsack()
      # self.p=int( ( 2 *  self.simple_knapscak[-1] ) + self.msg_len)
        p=int( (2 *simple_knapsack[-1])  + rand.randint(1, self.msg_len))
        u=self.find_co_prime(p)
        self.create_hard_knapsack(p,u,simple_knapsack)
        u_inv= modinv(u,p)
        return simple_knapsack,p,u_inv
        
    
    
    def get_public_key(self):
        return self.hard_ks
# =============================================================================
#         
#         
# =============================================================================
    def create_simple_knapsack(self):
        simple_ks=np.zeros(self.msg_len , dtype=int)
        simple_ks[0]=rand.randint(1, self.msg_len)
        #simple_ks[0]=self.msg_len
        sum_ks=simple_ks[0]
        for i in range(1,self.msg_len):
            extra=rand.randint(1, self.msg_len)
            #extra=self.msg_len
            simple_ks[i]=sum_ks+extra
            sum_ks=sum_ks+simple_ks[i]
            
            
        return simple_ks   
    
    
# =============================================================================
#     
#     
# =============================================================================
    def find_co_prime(self,p):
        section = rand.randint(1, 3)
        if section==1:
            for i in range(2,int(p/4)):
                if np.gcd(i,p)==1:
                    return i
        elif section == 2:
            for i in range(int(p/4)+1,int(p/2)):
                if np.gcd(i,p)==1:
                    return i
        
        elif section==3:
            for i in range(int(p/2)+1,int(3*p/4)):
                if np.gcd(i,p)==1:
                    return i
        else:
            for i in range(int(3*p/4)+1,p):
                if np.gcd(i,p)==1:
                    return i

            
# =============================================================================
#       
#             
# =============================================================================
    def create_hard_knapsack(self,p,u,simple_knapsack):
        self.hard_ks=np.zeros(self.msg_len , dtype=np.uint64)
        for i in range(len(simple_knapsack)):
            self.hard_ks[i]=(int(simple_knapsack[i])*u)%p
          
    @classmethod        
    def encryption(cls,message,hard_ks):
        cipher_text=0
        binary_list=[np.binary_repr(ord(ch),width=8) for ch in message]
        for i in range(len(binary_list)):
            for j in range(len(binary_list[i])):
                cipher_text = int(cipher_text+(hard_ks[i*len(binary_list[i])+j] * (ord(binary_list[i][j])-ord('0'))))
        return int(cipher_text)
        
        

    def decryption(self,cipher,simple_knapsack,p,u_inv):
        m=int((cipher*u_inv)%p)
        msg_list=[]
        knapsack_vec=np.zeros(self.msg_len,dtype=int)
        for i in range(self.msg_len-1,-1,-1):
            if(simple_knapsack[i]<=m):
                knapsack_vec[i]=1
                m=int(m-simple_knapsack[i])
        decrypted_msg=0
        for i in range(0,int(self.msg_len/8)):
            for j in range(7,-1,-1):
                if knapsack_vec[i*8 + j]==1:
                    decrypted_msg= decrypted_msg+2**(7-j)
                
            msg_list.append(chr(decrypted_msg))
            decrypted_msg=0
                
    
                
 
        decrypted_msg="".join(msg_list)
        return decrypted_msg
        
# =============================================================================
# =============================================================================
# knap=Knapsack_MH()
# simple_knapsack,p,u_inv=knap.get_key()
# pub=knap.get_public_key()
# s=knap.encryption('ab')
# dec=knap.decryption(s, simple_knapsack,p, u_inv)
# 
# 
# 
# =============================================================================
