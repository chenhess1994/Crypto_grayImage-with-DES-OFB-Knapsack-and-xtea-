# -*- coding: utf-8 -*-

import OFB
from User import PublicUser,PrivateUser
from Knapsack import Knapsack_MH
from Tools import setPicFormat
import numpy as np
from PIL import Image 

# =============================================================================
#  
# 
# 
# =============================================================================
user_dict={}  

client=None
connected_user={}



# =============================================================================
# send\recive encrypted image  
# 
# 
# 
# 
# 
# 
# =============================================================================


def decrypt_image():
    global connected_user
    plain =  OFB.ofbDec(connected_user["cipher_text"], connected_user['connection']['symmetric key'], connected_user["iv"])
    decrypted_pic=Image.frombytes("L", connected_user["size"], plain)
    close_connection()
    return decrypted_pic




def load_image():
    global client
    global connected_user
    pic=setPicFormat(client.image_path)
    pic_arr=np.array(pic,dtype=np.uint8)
    shape0=pic_arr.shape[0]
    shape1=pic_arr.shape[1]

    pic_arr=np.reshape(pic_arr,(pic_arr.shape[1] * pic_arr.shape[0]))

    iv, cipher_text = OFB.ofbEnc(pic_arr, client.symmetric_key)
    connected_user["iv"]=iv
    connected_user["cipher_text"]=cipher_text
    connected_user["size"]=(shape1,shape0) 
    return iv,cipher_text, (shape1,shape0) 


def save_image(image_path):
    global client
    client.image_path=image_path
    
 










# =============================================================================
#  establish secure connection
# 
# 
# 
# 
# 
# 
# 
# =============================================================================





def setup_connection(user_to_connect):
    global client
    encrypted_msg=send_symmetric_key(user_to_connect)
    return recive_symmetric_key_msg(encrypted_msg, client.get_name())

def establish_connection(user_to_connect):
    global connected_user
    decrypter=user_dict.get(user_to_connect)
    knap=Knapsack_MH()
    private_key=knap.get_key()
    if not bool(connected_user):
        connected_user.update({"connected":decrypter,"knapsack":knap,"private_key":private_key})
    return knap.get_public_key()
    


def close_connection():
    global connected_user
    connected_user.clear()
    print("connection was closed")


def send_symmetric_key(user_to_connect):
    global client
    hard_ks = establish_connection(user_to_connect)
    #msg=[]
    encrypted_msg=[]
    for i in range(0,int(len(client.symmetric_key)),2):
        #msg.append((client.symmetric_key[i],client.symmetric_key[i+1]))
        encrypted_msg_seg=Knapsack_MH.encryption(client.symmetric_key[i:i+2],hard_ks)
        print("encrypting:",client.symmetric_key[i:i+2])
        seg_signature=[client.signauture_alg.sign(encrypted_msg_seg.to_bytes(4,"little"),client.private_signature_key)]
        print(encrypted_msg_seg)
        #value in list -> tuple, values in tuple-> [0] encrypted msg,[1] signauture (a tuple)->[0] r, [1] s
        encrypted_msg.append([encrypted_msg_seg,seg_signature[0]])
       
        seg_signature.clear()
       
    return encrypted_msg
        
    
def recive_symmetric_key_msg(encrypted_msg,encrypter):
    global connected_user
    global user_dict
    encrypter=user_dict[encrypter]
    decrypter=connected_user["connected"]
    knap=connected_user.pop("knapsack")
    pr_key=connected_user.pop("private_key")
    msg=[]
    
    for msg_segment in encrypted_msg:
        if not decrypter.verfiy(msg_segment[0].to_bytes(4,"little"),msg_segment[1][0],msg_segment[1][1],encrypter.get_public_key()):
            return "Secure connection failed: message sender verification failed"
        print("decrypting:",msg_segment[0])
            
        msg.append(knap.decryption(msg_segment[0],pr_key[0],pr_key[1],pr_key[2]))
    connected_user["connection"]={"name":encrypter.get_name(),"symmetric key":"".join(msg)}
    return "Secure connection established"
    
    
    
    
    



# =============================================================================
# set database and log in and out user
# 
# 
# 
# 
# =============================================================================
def init_default_system_users(list_of_connected_users=["Chen","Bar","Idan"]):
    global user_dict
    for user in list_of_connected_users:

        user_dict[user]=PublicUser(user)
        


def log_in_user(name="ira",symm_key="HI-ATTACKER_XTEA"):
    global client
    global user_dict
    if  client==None:
        
        client=PrivateUser(name,symm_key)
    
        user_dict[name]=client.create_public_instance()
    else: 
        return
       # print("can't log in to pepole at the same time")
    

def log_out_user():
    global client
    client=None
    
    
    
    
    
def list_of_users():
    global user_dict
    global client
    list_of_users_names=[]
    for user in user_dict:
        if client.get_name() !=user:
            list_of_users_names.append(user)
    return list_of_users_names


# =============================================================================
# init_default_system_users()
# log_in_user()
# print(setup_connection("chen"))
# print(list_of_users())
# encrypted_image=load_image('E:/study/semester_8/Crypto/final Project/cheburashka.jpg')
# img=decrypt_image(encrypted_image[0], encrypted_image[1], encrypted_image[2])
# 
# img.show()
# #img=decrypt_image(encrypted_image)
# 
# 
# 
# 
# 
# =============================================================================









    
# =============================================================================
# 
# pic=setPicFormat(r'E:\study\semester_8\Crypto\final Project\cheburashka.jpg')
# 

# 
# 
# 
# plain =  OFB.ofbDec(result, key, iv)
# 
# decrypted_pic=Image.frombytes("L", (shape1,shape0), plain)
# decrypted_pic.show()
# =============================================================================

# =============================================================================
# plain=np.array(result,dtype=np.uint8)
# plain=np.reshape(plain,(shape0 , shape1))
# decrypted_pic=Image.fromarray(plain,mode="L")
# decrypted_pic.show()
# =============================================================================

