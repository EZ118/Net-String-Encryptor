import requests
import base64
from tkinter import *
import sys


global DefaultDict
DefaultDict = "asdf1234ghjk5678lqwe90-=rtyu[]\;iopz',./xcvb`~!@nmMN#$%^BVCX&*()ZLKJ_+{}HGFD|:\"<SAQW>?ERTY UIOP"

def encode(st):
    return str(base64.b64encode(st.encode('utf-8'))).replace("b'", "").replace("'", "")

def decode(st):
    return str(base64.b64decode(st).decode("utf-8"))

def hex2int(num):
    return int(num, 16)

def int2hex(num):
    ss = str(format(num, 'x'))
    if len(ss) < 2:
        ss = "0" + ss
    return ss

def CreateDict():
    url = Entry1.get()

    dic = ""
    codes = requests.get(url).text.replace("\\n","")
    codes = encode(url) + str(codes) + DefaultDict

    for i in str(codes):
        if i in dic:
            continue
        else:
            dic += i
    global Current_Dict
    Current_Dict = dic
    
def NetEncode(dic, txt):
    final_txt = ""
    orig_txt = encode(txt)
    
    for i in orig_txt:
        if i in dic:
            final_txt += int2hex(dic.find(i))
        else:
            final_txt += "**"
    
    final_txt = encode(final_txt)
    return final_txt

def NetDecode(dic, txt):
    final_txt = ""
    orig_txt = decode(txt).replace("**", "")
    
    for i in range(1, len(orig_txt), 2):
        try:
            final_txt += str( dic[ hex2int( orig_txt[i - 1] + orig_txt[i] ) ] )
        except:
            continue
            
    final_txt = decode(final_txt)
    return str(final_txt)

def clear_console():
    console.delete('1.0','end')

def DeG():
    ipt = console.get("1.0","end").replace("\\n", "")
    t = NetDecode(Current_Dict, ipt)
    clear_console()
    console.insert("end", t)
    
    
def EnG():
    ipt = console.get("1.0","end")
    t = NetEncode(Current_Dict, ipt)
    clear_console()
    console.insert("end", t)
    



if __name__ == '__main__':
    win = Tk()
    win.title('Net String Encryptor')
    win.geometry('264x344+100+100')
    
    global Entry1
    Entry1 = Entry(win, font=('黑体', 12))
    Entry1.place(y=10, x=14, width=234, height=25)
    Entry1.focus_set()

    Button1 = Button(win, text='Dict', font=('黑体', 11), command = CreateDict).place(y=40, x=20, width=65, height=28)
    Button2 = Button(win, text='Encode', font=('黑体', 11), command = EnG).place(y=40, x=99, width=40, height=28)
    Button3 = Button(win, text='Decode', font=('黑体', 11), command = DeG).place(y=40, x=153, width=40, height=28)
    Button4 = Button(win, text='Clear', font=('黑体', 11), command = clear_console).place(y=40, x=207, width=40, height=28)

    global console
    console = Text(win, font=('黑体', 11))
    console.place(y=82, x=15, width=236, height=241)

    win.mainloop()
