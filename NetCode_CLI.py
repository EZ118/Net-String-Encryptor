import requests
import base64
import sys

Current_Dict = ""
DefaultDict = "asdf1234ghjk5678lqwe90-=rtyu[]\;iopz',./xcvb`~!@nmMN#$%^BVCX&*()ZLKJ_+{}HGFD|:\"<SAQW>?ERTY UIOP"

def encode(st):
    return str(base64.b64encode(st.encode('utf-8'))).replace("b'", "").replace("'", "")

def decode(st):
    return str(base64.b64decode(st).decode("utf-8"))

def CreateDict(url):
    dic = ""
    codes = requests.get(url).text.replace("\\n","")
    codes = encode(url) + str(codes) + DefaultDict

    for i in str(codes):
        if i in dic:
            continue
        else:
            dic += i
    return dic

def NetEncode(dic, txt):
    final_txt = ""
    orig_txt = encode(txt)
    
    for i in orig_txt:
        if i in dic:
            final_txt += str(dic.find(i)) + " "
        else:
            final_txt += "* "
    
    final_txt = encode(final_txt)
    return final_txt

def NetDecode(dic, txt):
    final_txt = ""
    orig_txt = decode(txt).replace("*", "")

    for i in orig_txt.split(" "):
        try:
            final_txt += dic[int(i)]
        except:
            continue
    
    final_txt = decode(final_txt)
    return str(final_txt)

if __name__ == '__main__':
    try:
        tmp = sys.argv[1]
    except:
        a = input("Encode or Decode?     [e/d] ")
    
    branchURL = input("URL: ")
    print("[*] ok, please wait...")
    Current_Dict = CreateDict(branchURL)
    print("[+] done!")

    orig_txt = input("TEXT: ")
    
    try:
        if sys.argv[1] == "-e":
            print("[+] " + NetEncode(Current_Dict, orig_txt))
        elif sys.argv[1] == "-d":
            print("[+] " + NetDecode(Current_Dict, orig_txt))
            
    except:
        if a == "e":
            print("[+] " + NetEncode(Current_Dict, orig_txt))
        else:
            print("[+] " + NetDecode(Current_Dict, orig_txt))
