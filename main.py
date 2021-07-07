import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import sys
import time
import Logic as logic

approved_file_types=[".gif"]

"""GUI Logic"""
class ProgController():
    def __init__(self,root,frameTitleList,approved_file_types,index):
        self.root=root
        self.approved_file_types=approved_file_types
        self.frameTitleList=frameTitleList
        self.textbox = Text(root)
        self.index=index
        
    def next_send_index(self):
        if self.index<4:
            self.index=self.index+1
        return self.index
    
#    def next_viewIndex(self)
    def back_index(self):
        if self.index!=0:
            self.index=self.index -1
        return self.index
# =============================================================================
#     def redirector(self,inputStr):
#         self.textbox.insert(INSERT, inputStr)
# 
# =============================================================================
    def loadNextStage(self,index,send_or_recv):
        mainFrame= Frame(self.root)
        self.next_send_index()        
        if send_or_recv=="sender":                   
            #upload
            if index==0:
                 #need to add lameda in controller
                 newFrame=UploadFrame(self, mainFrame, self.frameTitleList[self.index], self.index)
                 
            elif index==1:
                 #need to add lameda in controller
                 newFrame=ListFrame(self, mainFrame, self.frameTitleList[self.index], self.index)   
            elif index==2:
                logic.load_image()
                self.index=0
                self.startProg()
                return
        elif send_or_recv=="reciever":
            if index==0:
                  newFrame=ViewFrame(self, mainFrame, self.frameTitleList[self.index], self.index)
            elif index==1:
                  self.index=0
                  self.startProg()
                  return
             
        newFrame.send_or_recv=send_or_recv
        return
    
    def startProg(self):
          mainFrame= Frame(self.root)
          startFrame=LogFrame(self,mainFrame, self.frameTitleList[0],0)
          welcomeLabel=Label(startFrame.frame,bg="yellow",text="Welcome To Grayscale encryption \n\n\n\n\nCreated by:Ira Goor,Chen Hess,Bar Dermer And Idan Brauner").pack()
          mainFrame.place(anchor="center",relx=.5,rely=.5)
          mainFrame.configure(bg="yellow")
          logic.init_default_system_users()
          
            
""""General frame base controller """
class ProgFrame():
    def __init__(self,controller,mainFrame,title,stage_index):
        
        self.controller=controller
        self.mainFrame=mainFrame
        self.frame=LabelFrame(self.mainFrame,text=title,bg="#49DEE6")
        self.stage_index=stage_index
# =============================================================================
#         self.exit_frame=LabelFrame(self.mainFrame,text='Exit Program',bg="white")
#         self.exit_btn=Button(self.exit_frame,text="EXIT",command=self.exitProg)
#         self.exit_btn.pack(side=RIGHT)
# =============================================================================
        self.frame.pack(side=TOP)
 
        self.stage_scroller=LabelFrame(self.mainFrame,text='Stages',bg="yellow")
        self.stage_scroller.pack(side=BOTTOM,fill=BOTH)
        
        if self.stage_index!=0:
            self.NextStageButton=Button(self.stage_scroller,text="Next",bg="GRAY",command=self.nextStage,padx=40,pady=20)
            self.NextStageButton.pack(side=RIGHT)
        mainFrame.pack()
        
    def exitProg(self):
        self.controller.root.close()
    def lastStage(self):
        pass
        
    def nextStage(self):
        if self.checkCorrectness():
            self.mainFrame.destroy()
            self.controller.loadNextStage(self.stage_index,self.send_or_recv)
        return
               
    def checkCorrectness(self):
        return True
    


    
class LogFrame(ProgFrame):
    def __init__(self,controller,mainFrame,title,stage_index):
        super().__init__(controller, mainFrame, title, stage_index)  
        
        self.label=Label(self.stage_scroller,text = "Enter a name:",bg="yellow")
        self.label.pack()
        
        self.logTextField=Text(self.stage_scroller,height=1,width=20)
        self.logTextField.pack()
        
         #need to add lameda in controller
        self.send_btn=Button(self.stage_scroller,text="login as a viewer ",bg="red",command=self.viewPic,padx=40,pady=20)
        self.send_btn.pack(side=RIGHT)
        #need to add lameda in controller
        self.view_btn=Button(self.stage_scroller,text="login as a sender ",bg="green",command=self.sendPic,padx=40,pady=20) 
        self.view_btn.pack(side=LEFT)
        
    def viewPic(self):
        self.send_or_recv="reciever"
        if len(self.logTextField.get("1.0", "end-1c"))==0:
            return
        logic.log_in_user(name=self.logTextField.get("1.0", "end-1c"))
       
        self.nextStage()
        return
    def sendPic(self):
        self.send_or_recv="sender"
        if len(self.logTextField.get("1.0", "end-1c"))==0:
            return
        logic.log_in_user(name=self.logTextField.get("1.0", "end-1c"))
        
        self.nextStage()
        return
    
class UploadFrame(ProgFrame):
    def __init__(self,controller,mainFrame,title,stage_index):
        super().__init__(controller, mainFrame, title, stage_index)
        self.imgNameText=tk.StringVar()
        self.imgNameText.set("please choose a file:")
        self.imgName=Label(self.frame,textvariable=self.imgNameText)    
        self.imgName.pack(side=TOP)          
        self.upload=Button(self.frame,text="Upload",bg="green",command=self.browseFiles,padx=40,pady=20)      
        self.upload.pack(side=BOTTOM)
        
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/",title="Select a File"
                                                            , filetypes=(("JPEG file","*.jpg*")
                                                            , ("all files","*.*")))
        logic.save_image(filename)
        listPath=filename.split("/")
        self.imgNameText.set(listPath[-1])
        
        img = Image.open(filename)
        img = img.resize((500, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.frame, image=img)
        panel.image = img
        panel.pack()
        
class ListFrame(ProgFrame):
    def __init__(self,controller,mainFrame,title,stage_index):
        super().__init__(controller, mainFrame, title, stage_index)
         
        label = Label(self.frame,text = "A list of people:")  
        label.pack()  
        
        self.listbox = Listbox(self.frame)  
        list_name=logic.list_of_users()
        for i in range (len(list_name)):
            self.listbox.insert(i+1,list_name[i])

        self.listbox.pack()  
        
    def establish_connection (self):
     print(logic.setup_connection(self.listbox.get(self.listbox.curselection())))
     
    def nextStage(self):
        if self.send_or_recv=="sender":
            self.establish_connection()
        super().nextStage()
        
        
class ViewFrame(ProgFrame):
    def __init__(self,controller,mainFrame,title,stage_index):
        super().__init__(controller, mainFrame, title, stage_index)
        self.imgName=Label(self.frame)    
        self.imgName.pack(side=TOP)
        img = logic.decrypt_image()
        img = img.resize((500, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.frame, image=img)
        panel.image = img
        panel.pack()
        

"""MAIN"""
root=Tk()
root.geometry("700x700")
root.configure(bg="#49DEE6")

progController=ProgController(root, ["Intro","List","Picture","results"], approved_file_types,0)
#sys.stdout.write = progController.redirector #whenever sys.stdout.write is called, redirector is called.

progController.startProg()
root.mainloop()






