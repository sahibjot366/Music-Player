from tkinter import *
from PIL import Image,ImageTk
import time
import os
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as msg
import pygame
import json
import random
import _thread
import threading

pygame.mixer.init()
pygame.display.init()
mp3list=[]
events_in_program={}
file=""
rasta=""
root=Tk()
subroot=Toplevel()
cd=0
cs=0
ct=-5
frts=[]
queuesong=[]
loop=0
currpos1=0.0
shuffvar=0
frame1=Frame(root,width=80)
scrollbar=Scrollbar(frame1)
listbox1=Listbox(frame1,bg="gray8",selectmode=SINGLE,bd=6,width=60,selectbackground="violet",fg="darkviolet",yscrollcommand=scrollbar.set,font="'' 11 bold",height=22)
listbox3=Listbox(frame1,bg="gray8",selectmode=SINGLE,bd=6,width=60,selectbackground="violet",fg="darkviolet",yscrollcommand=scrollbar.set,font="'' 11 bold",height=22)
def get():
    ''' Opens file and set value of events_in_program  '''
    global events_in_program
    with open("mp3player_events.txt") as fh:
        events_in_program=json.load(fh)
        
def set():
    '''  Opens file in write mode and dumps the event_in_program  '''
    with open("mp3player_events.txt","w") as fh:
        json.dump(events_in_program, fh)
        
def recents():
    ''' Shows recent music played '''
    global events_in_program
    txt=""
    recent=Toplevel()
    recent.geometry("970x280")
    recent.resizable(width=False, height=False)
    recent.iconphoto(False,photo)
    recent.config(bg="gray21")
    recent.title("Recents")
    recent_frame=Frame(recent,bg="gray21")
    recent_label=Label(recent_frame,font="arial 15 bold",bg="gray21",fg="darkviolet")
    get()
    if len(events_in_program['recents'])>10:
#         for i in range(len(events_in_program['recents'])):
#             if i<(len(events_in_program['recents'])-10):
#                 print(i)
#                 print(events_in_program['recents'][i])
#                 events_in_program['recents'].remove(events_in_program['recents'][i])
        del events_in_program['recents'][0:(len(events_in_program['recents'])-10)]
    for i in reversed(events_in_program['recents']):
        txt+=i+"\n"
    set()
    recent_frame.pack()
    recent_label.config(text=txt)
    recent_label.pack(anchor=CENTER,padx=15,pady=10)
    recent.mainloop()
def favourites():
    global frame1
    global listbox3
    global scrollbar
    k=0
    if listbox1.winfo_exists() and frame1.winfo_exists() and scrollbar.winfo_exists():
        listbox1.destroy()
        frame1.destroy()
        scrollbar.destroy()
    frame1=Frame(root,width=80)      
    scrollbar=Scrollbar(frame1)
    listbox3=Listbox(frame1,bg="gray8",selectmode=SINGLE,bd=6,width=60,selectbackground="violet",fg="darkviolet",yscrollcommand=scrollbar.set,font="'' 11 bold",height=22)
    get()
    for i,j in events_in_program['favourites'].items():
        listbox3.insert(k,i)
        frts.append(j)
        k+=1
    if len(frts)==0:
        msg.showerror("Status","No items in favourite list")
    else:
        scrollbar.config(command=listbox3.yview)
        scrollbar.pack(side=RIGHT,fill="y")
        frame1.pack(side=BOTTOM,pady=30)
        listbox3.pack()
        listbox3.bind("<Double-Button-1>",player)

def bandkro():
    ''' It hides all the widgets in root  '''
    slabel1.pack_forget()
    slabel2.pack_forget()
    volume.pack_forget()
    sframe1.pack_forget()
    buttback.pack_forget()
    buttfwd.pack_forget()
    buttpause.pack_forget()
    buttstop.pack_forget()
    sframe2.pack_forget()
    buttfavplus.pack_forget()
    buttonce.pack_forget()
    buttqueue.pack_forget()
    subroot.deiconify()
def stop():
    '''  Command for stop button '''
    global cd
    pygame.mixer.music.stop()
    bandkro()
    cd=1


def pauseplay():
    ''' Command for Pause and play button  '''
    if buttpause.cget('image')==str(imagepause):
        pygame.mixer.music.pause()
        buttpause.config(image=imageplay)
    else:
        pygame.mixer.music.unpause()
        buttpause.config(image=imagepause)
def previous():
    '''  Command for back button '''
    global ct
    global rasta
    pygame.mixer.music.stop()
    if ct==-5:
        ct=cs[0]
    ct=ct-1
      
    if ct<0:
        msg.showerror("Status","No music file")
    else:
        if listbox1.winfo_exists():
            file =listbox1.get(ct)
            get()
            events_in_program["recents"].append(file)
            if file in events_in_program['favourites'].keys():
                buttfavplus.config(image=imagefavminus)
            else:
                buttfavplus.config(image=imagefavplus)
            set()
            slabel1.configure(text=file)
            play_music(rasta, file)
        elif listbox3.winfo_exists():
            file =listbox3.get(ct)
            rasta=frts[ct]
            get()
            events_in_program["recents"].append(file)
            if file in events_in_program['favourites'].keys():
                buttfavplus.config(image=imagefavminus)
            else:
                buttfavplus.config(image=imagefavplus)
            set()
            slabel1.configure(text=file)
            play_music(rasta, file)
def next():
    '''  Command for next button '''
    global ct
    global rasta
    pygame.mixer.music.stop()
    if ct==-5:
        ct=cs[0]
    ct=ct+1
    if listbox1.winfo_exists():
        if ct==len(mp3list):
            msg.showerror("Status","No music file ahead")
        else:
            file =listbox1.get(ct)
            get()
            events_in_program["recents"].append(file)
            if file in events_in_program['favourites'].keys():
                buttfavplus.config(image=imagefavminus)
            else:
                buttfavplus.config(image=imagefavplus)
            set()
            slabel1.configure(text=file)
            play_music(rasta, file)
    elif listbox3.winfo_exists():
        if ct==len(frts):
            msg.showerror("Status","No music file ahead")
        else:
            file =listbox3.get(ct)
            rasta=frts[ct]
            get()
            events_in_program["recents"].append(file)
            if file in events_in_program['favourites'].keys():
                buttfavplus.config(image=imagefavminus)
            else:
                buttfavplus.config(image=imagefavplus)
            set()
            slabel1.configure(text=file)
            play_music(rasta, file)
def vol(currvol):
    ''' Command for volume Scale widget '''
    currvol=float(int(currvol)/100)
    pygame.mixer.music.set_volume(currvol)
    
def favchange():
    if buttfavplus.cget('image')==str(imagefavplus):
        get()
        events_in_program['favourites'].update({slabel1.cget('text'):rasta})
        buttfavplus.config(image=imagefavminus)
        set()
    else:
        get()
        del events_in_program['favourites'][slabel1.cget('text')]
        buttfavplus.config(image=imagefavplus)
        set()
        

    
def queue():
    ''' Command for Queue button.. Only one music file can be queued '''
    #Currently not working
    def abcd(adc):
        queuesong.clear()
        queuesong.append(listbox2.get(listbox2.curselection()))
        while pygame.mixer.music.get_busy()==True:
            continue
        else:
            get()
            if queuesong[0] in events_in_program['favourites'].keys():
                buttfavplus.config(image=imagefavminus)
            else:
                buttfavplus.config(image=imagefavplus)
            slabel1.config(text=queuesong[0])
            pygame.mixer.music.load(rasta+"\\"+queuesong[0])
            queuesong.clear()
            pygame.mixer.music.play(0)

    def selectqueue(event):
        
        try:
            _thread.start_new_thread(abcd,(1,))
        except Exception as e:
            msg.showerror("Status",e)
       
    queuetop=Toplevel()
    queuetop.title("Queue")
    queuetop.geometry("516x500")
    queuetop.iconphoto(False,photo)
    queueframe1=Frame(queuetop,width=80)      
    queuescrollbar=Scrollbar(queueframe1)
    listbox2=Listbox(queueframe1,bg="gray8",selectmode=SINGLE,bd=6,width=60,selectbackground="violet",fg="darkviolet",yscrollcommand=queuescrollbar.set,font="'' 11 bold",height=22)
    for i in range(len(mp3list)):
        listbox2.insert(i,mp3list[i])
    queuescrollbar.config(command=listbox2.yview)
    queuescrollbar.pack(side=RIGHT,fill="y")
    queueframe1.pack(side=BOTTOM,pady=30)
    listbox2.pack()
    listbox2.bind("<Double-Button-1>",selectqueue)
    queuetop.mainloop()
    
def once_loop_shuffle():
    global loop
    global currpos1
    if loop==0:
        currpos1=0.0
        loop=1
    currpos=currpos1+float(pygame.mixer.music.get_pos()/1000)
    currpos1=currpos
    print(currpos,currpos1)
    if buttonce.cget('image')==str(imageonce):
        pygame.mixer.music.play(-1,currpos)
        buttonce.config(image=imageloop)
    else:
        pygame.mixer.music.play(0,currpos)
        buttonce.config(image=imageonce)
    currpos=0.0
# def checkend(hello):
#     global loop
#     global currpos1
#     while True:
#         while pygame.mixer.music.get_endevent()==True:
#             continue
#         else:
#             root=0
#             currpos1=0.0
# _thread.start_new(checkend,("hello",))
def search_list():
    num=0
    item=str(srch.get())
    item=item.lower()
    if listbox1.winfo_exists():
        for i in mp3list:
            if item in str(i).lower():
                listbox1.see(num)
                listbox1.itemconfig(num,bg="gold",fg="darkviolet")
                root.after(10000,lambda:listbox1.itemconfig(num,bg="gray8",fg="darkviolet"))
                break
            num+=1
        else:
            msg.showerror("Status","No such item found!!")
    elif listbox3.winfo_exists():
        get()
        for i in events_in_program['favourites'].keys():
            if item in str(i).lower():
                listbox3.see(num)
                listbox3.itemconfig(num,bg="gold",fg="darkviolet")
                root.after(10000,lambda:listbox3.itemconfig(num,bg="gray8",fg="darkviolet"))
                break
            num+=1
        else:
            msg.showerror("Status","No such item found!!")
    srch.set("")
root.geometry("516x750")
root.resizable(width=False, height=False)
photo=PhotoImage(file="icon.png")
root.iconphoto(False,photo)
root.title("Sangeet")
ct=0

def pics(w,h,name):
    ''' Resize Image. Requires three parameters : width,height and name of image file '''
    photos=Image.open(name)
    photos=photos.resize((w,h),Image.ANTIALIAS)
    initialphoto=ImageTk.PhotoImage(photos)
    return initialphoto

imagepause=pics(25,25,"pause.png")
imageplay=pics(25,25,"play.png")
imagebackward=pics(32,32,"backward.png")
imageforward=pics(32,32,"forward.png")
imagefavplus=pics(32,32,"favplus.png")
imagefavminus=pics(32,32,"favminus.png")
imagestop=pics(32,32,"stop.png")
imageonce=pics(32,32,"once.png")
imagequeue=pics(32,32,"queue.png")
imageicon=pics(300,300,"icon.png")
imageloop=pics(32,32,"loop.png")

slabel1=Label(subroot,text=file,bg="gray21",fg="white",font="lucida 10")
slabel2=Label(subroot,image=imageicon,bd=0)
volume=Scale(subroot,from_=0,to=100,tickinterval=10,label="Volume",orient=HORIZONTAL,bg="darkviolet",fg="gold",length=200,bd=8,relief=SUNKEN,command=vol)
sframe1=Frame(subroot,bg="darkviolet")
buttback=Button(sframe1,image=imagebackward,bd=0,command=previous)
buttfwd=Button(sframe1,image=imageforward,bd=0,command=next)
buttpause=Button(sframe1,image=imagepause,bd=0,command=pauseplay)
buttstop=Button(sframe1,image=imagestop,bd=0,command=stop)
sframe2=Frame(subroot,bg="darkviolet")
buttfavplus=Button(sframe2,image=imagefavplus,bd=0,command=favchange)
buttonce=Button(sframe2,image=imageonce,bd=0,command=once_loop_shuffle)
buttqueue=Button(sframe2,image=imagequeue,bd=0,command=queue)
srch=StringVar()
srch.set("")

# currlist=[]
# currsong=random.choice(mp3list)

def shuffle():
    def shuff(nouse):
        currlist=[]
        while True:
            if listbox1.winfo_exists() and listbox1.winfo_ismapped:
                currsong=random.choice(mp3list)
            elif listbox3.winfo_ismapped():
                pass
            if currsong in currlist:
                continue
            elif currlist==mp3list:
                msg.showinfo("Status","All the songs have been played once")
                break
            else:
                currlist.append(currsong)
                slabel1.configure(text=currsong)
                pygame.mixer.music.load(rasta+"\\"+currsong)
                pygame.mixer.music.play(0)
                while pygame.mixer.music.get_busy()==True:
                    continue
                else:continue                
    subroot.geometry("516x750")
    subroot.title("Sangeet")
    subroot.iconphoto(False,photo)
    subroot.resizable(width=False, height=False)
    subroot.config(bg="gray21")
    pygame.mixer.music.stop()
    
    
    slabel1.configure(text=file)
    slabel1.pack(pady=3)
    slabel2.pack(pady=30)
    volume.set(100)
    volume.pack(pady=5)
    # TODO: ADD PROGRESS BAR
    sframe1.pack(fill="x",pady=40)
    buttback.image=imagebackward
    buttfwd.image=imageforward
    buttpause.image=imagepause
    buttstop.image=imagestop
    buttback.pack(side=LEFT,padx=47)
    buttpause.pack(side=LEFT,padx=47)
    buttstop.pack(side=LEFT,padx=47)
    buttfwd.pack(side=LEFT,padx=47)
    sframe2.pack(pady=20,fill="x")
    buttfavplus.pack(anchor=CENTER)
    _thread.start_new_thread(shuff,(0,))
    subroot.mainloop()
def subinit():
    pass
def player(event):
    '''  Plays music according to choice in Listbox1
    Displays all widgets in First Top Level  '''
    global file
    global recentlist
    global subroot
    global cs
    global ct
    global rasta
    global root
    global currpos1
    root=0
    currpos1=0.0
    subroot.geometry("516x750")
    subroot.title("Sangeet")
    subroot.iconphoto(False,photo)
    subroot.resizable(width=False, height=False)
    subroot.config(bg="gray21")
    pygame.mixer.music.stop()
    if listbox1.winfo_exists() and listbox1.winfo_ismapped:
        cs=listbox1.curselection()
        file=listbox1.get(cs)
    elif listbox3.winfo_ismapped():
        cs=listbox3.curselection()
        file=listbox3.get(cs)
        rasta=frts[cs[0]]
    get()
    events_in_program["recents"].append(file)
    if file in events_in_program['favourites'].keys():
        buttfavplus.config(image=imagefavminus)
    else:
        buttfavplus.config(image=imagefavplus)
    set()
    ct=-5
    slabel1.configure(text=file)
    slabel1.pack(pady=3)
    slabel2.pack(pady=30)
    volume.set(100)
    volume.pack(pady=5)
    # TODO: ADD PROGRESS BAR
    sframe1.pack(fill="x",pady=40)
    buttback.image=imagebackward
    buttfwd.image=imageforward
    buttpause.image=imagepause
    buttstop.image=imagestop
    buttback.pack(side=LEFT,padx=47)
    buttpause.pack(side=LEFT,padx=47)
    buttstop.pack(side=LEFT,padx=47)
    buttfwd.pack(side=LEFT,padx=47)
    sframe2.pack(pady=20,fill="x")
    buttfavplus.pack(side=LEFT,padx=67)
    buttonce.image=imageonce
    buttonce.pack(side=LEFT,padx=67)
    buttqueue.image=imagequeue
    buttqueue.pack(side=LEFT,padx=67)
    play_music(rasta, file)
    subroot.mainloop()
    


    
def play_music(rasta,file):
    ''' Loads and Plays music  '''
    pygame.mixer.music.load(rasta+"\\"+file)
    pygame.mixer.music.play(0)
#     subroot.mainloop()

def opn():
    global ct
    global mp3list
    if ct==0:
        ct=1
        pass
    else:
        global listbox1
        global scrollbar
        global frame1
        global rasta
        if (listbox1.winfo_exists() and frame1.winfo_exists() and scrollbar.winfo_exists()):
            listbox1.destroy()
            frame1.destroy()
            scrollbar.destroy()
        if (listbox3.winfo_exists() and frame1.winfo_exists() and scrollbar.winfo_exists()):
            listbox3.destroy()
            frame1.destroy()
            scrollbar.destroy()
    try:       
        frame1=Frame(root,width=80)      
        scrollbar=Scrollbar(frame1)
        listbox1=Listbox(frame1,bg="gray8",selectmode=SINGLE,bd=6,width=60,selectbackground="violet",fg="darkviolet",yscrollcommand=scrollbar.set,font="'' 11 bold",height=22)
        rasta=filedialog.askdirectory(initialdir = "C:\\Users\\sahib\\Desktop",title = "Select your Music Folder")
        if rasta=="":
            pass
        else:
            list_rasta=os.listdir(rasta)
            mp3list=[i for i in list_rasta if ".mp3" in i]
            if len(mp3list)==0:
                msg.showerror("Status","No music files found!!")
            else:
                for i in range(len(mp3list)):
                    listbox1.insert(i,mp3list[i])
                scrollbar.config(command=listbox1.yview)
                scrollbar.pack(side=RIGHT,fill="y")
                frame1.pack(side=BOTTOM,pady=30)
                listbox1.pack()
                listbox1.bind("<Double-Button-1>",player)
    except:
        pass


def initialize():
    ''' Start Up screen 
    No function. Just for decorative purpose'''
    global photo
    root.config(bg="black")
    initialphoto=pics(512,384,"initializer.jpg")
    label1=Label(root,image=initialphoto,bd=0)
    label1.image=initialphoto
    label1.pack(pady=50)
    label2=Label(root,text="SANGEET",font="lucida 35 bold",bg="black",fg="gold")
    label2.pack(pady=20)
    label3=Label(root,text="..Let the music take you away..",font="lucida 16 bold",bg="black",fg="gold")
    label3.pack(pady=15)
    root.update()
    time.sleep(2)
    label1.destroy()
    label2.destroy()
    label3.destroy()
    root.update()
    
def display_screen1():
    ''' Main root window'''
    root.config(bg="gray21")
    mainmenu=Menu(root)
    mainmenu.add_command(label="open",command=opn)
    root.config(menu=mainmenu)
    imagerecents=pics(65,65,"rec.jpg")
    imagefavourites=pics(65,65,"fav.jpg")
    imageshuffle=pics(65,65,"shu.jpg")
    frame2=Frame(root,bg="gray21")
    frame2.pack(fill="x",side="top",pady=15)
    buttrecents=Button(frame2,image=imagerecents,command=recents)
    buttfavourites=Button(frame2,image=imagefavourites,command=favourites)
    buttshuffle=Button(frame2,image=imageshuffle,command=shuffle)
    buttrecents.image=imagerecents
    buttshuffle.image=imageshuffle
    buttfavourites.image=imagefavourites
    buttrecents.pack(side=LEFT,padx=48)
    buttfavourites.pack(side=LEFT,padx=48)
    buttshuffle.pack(side=LEFT,padx=48)
    frame3=Frame(root,bg="gray21")
    frame3.pack(fill="x")
    label1=Label(frame3,text="Recents",font="arial 10 bold",bg="gold",fg="darkviolet")
    label2=Label(frame3,text="Favourites",font="arial 10 bold",bg="gold",fg="darkviolet")
    label3=Label(frame3,text="Shuffle",font="arial 10 bold",bg="gold",fg="darkviolet")
    label1.pack(side=LEFT,padx=53)
    label2.pack(side=LEFT,padx=53)
    label3.pack(side=LEFT,padx=53)
    frame4=Frame(root,bg="gray21")
    frame4.pack(fill="x",pady=16)
    buttsearch=Button(frame4,text="Search",bg="gold",fg="darkviolet",command=search_list)
    entry=Entry(frame4,fg="darkviolet",width=30,font="'' 18 bold",textvariable=srch)
    entry.pack(anchor=CENTER,padx=40,pady=50)
    buttsearch.pack(padx=5,anchor=CENTER,pady=1)
    opn()
    

initialize()
display_screen1()
root.mainloop()