# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:49:47 2021

@author: irago
"""
from DSA import My_DSA


class PublicUser():
    def __init__(self,name,public_key=None,is_from_private=False,a_dsa=None):
        self.name=name
        if is_from_private:
            self.signauture_alg=a_dsa
            self.public_signature_key=public_key
        else:
            self.signauture_alg=My_DSA()
            self.set_key()
        
        
    def get_name(self):
        return self.name
    
    def verfiy(self,msg, r, s, publicKey):
        return self.signauture_alg.verify(msg, r, s, publicKey)
    
    def set_key(self):
        
         temp_public_signature_key,_=self.signauture_alg.get_key()
         
         self.public_signature_key={"q":temp_public_signature_key[0],"p":temp_public_signature_key[1],"g":temp_public_signature_key[2],"y":temp_public_signature_key[3]}
         
    def get_public_key(self):
        return self.public_signature_key



class PrivateUser(PublicUser):
    
        def __init__(self,name,symmetric_key):    
            super().__init__(name)
            self.symmetric_key=symmetric_key
            self.set_key()
             
        def set_key(self):
            
            temp_public_signature_key,self.private_signature_key=self.signauture_alg.get_key()
            self.public_signature_key={"q":temp_public_signature_key[0],"p":temp_public_signature_key[1],"g":temp_public_signature_key[2],"y":temp_public_signature_key[3]}
        def get_private_key(self):
            return self.private_signature_key
        def create_public_instance(self):
            dsa=self.signauture_alg
            return PublicUser(self.name,public_key=self.public_signature_key,is_from_private=True,a_dsa=dsa)
            
        
# =============================================================================
#         
# pri=PrivateUser("ira", "01234567")
# user_dict={}           
# public_users=[PublicUser("chen"),PublicUser("idan"),PublicUser("bar"),pri.create_public_instance()]
# for pubuser in public_users:
#     pubuser.set_key()
#     user_dict[pubuser.get_name()]=pubuser
# =============================================================================


