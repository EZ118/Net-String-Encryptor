#-*- coding:utf-8 -*-
import requests
import base64

Current_Dict = ""
DefaultDict = "asdf1234ghjk5678lqwe90-=rtyu[]\;iopz',./xcvb`~!@nmMN#$%^BVCX&*()ZLKJ_+{}HGFD|:\"<SAQW>?ERTY UIOP"


def encode(st):
  return str(base64.b64encode(st.encode('utf-8'))).replace("b'", "").replace(
    "'", "")


def decode(st):
  return str(base64.b64decode(st).decode("utf-8"))


def CreateDict(url):
  dic = ""
  codes = requests.get(url).text.replace("\\n", "")
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


from http.server import HTTPServer, BaseHTTPRequestHandler
from furl import furl


class RequestHandler(BaseHTTPRequestHandler):

  def log_message(self, format: str, *args):
    return

  Page = open("./index.html", "r").read()

  # 处理一个GET请求
  def do_GET(self):
    self.urldata = ""
    self.txtdata = ""
    self.result = ""
    self.ff = ""
    self.tp = ""

    self.tp = self.path + "?"
    self.tp = self.tp.split("?")

    if self.tp[0] == "/" or self.tp[0] == "/index.html":
      if self.tp[1] != "":
        try:
          self.ff = furl(self.path)
          self.urldata = self.ff.args['url']
          self.txtdata = self.ff.args['text']

          self.dict = CreateDict(self.urldata)

          if self.ff.args['ctype'] == "encode":
            self.result = NetEncode(self.dict, self.txtdata)
          elif self.ff.args['ctype'] == "decode":
            self.result = NetDecode(self.dict, self.txtdata)

        except:
          self.result = "Error"
      else:
        self.result = ""

      self.Page = self.Page.replace("{{result}}", self.result)
      self.Page = str.encode(self.Page)

    elif self.tp[0] == "/api" or self.tp[0] == "/api/":
      if self.tp[1] != "":
        try:
          self.ff = furl(self.path)
          self.urldata = self.ff.args['url']
          self.txtdata = self.ff.args['text']

          self.dict = CreateDict(self.urldata)

          if self.ff.args['ctype'] == "encode":
            self.result = NetEncode(self.dict, self.txtdata)
          elif self.ff.args['ctype'] == "decode":
            self.result = NetDecode(self.dict, self.txtdata)

        except:
          self.result = "{'result':'','url':'','error_code':2,'message':'Unexpected parameter'}"
      else:
        self.result = "{'result':'','url':'" + self.urldata + "','error_code':1,'message':'Missing incoming parameter'}"

      self.Page = "{'result':'" + self.result + "','url':'" + self.urldata + "','error_code':0,'message':'ok'}"
      self.Page = str.encode(self.Page)
    else:
      self.Page = "{'error_code':404,'message':'File not found'}"
      self.Page = str.encode(self.Page)

    self.send_response(200)
    self.send_header("Content-Type", "text/html")
    self.send_header("Content-Length", str(len(self.Page)))
    self.end_headers()
    self.wfile.write(self.Page)


if __name__ == '__main__':
  serverAddress = ('', 8080)
  server = HTTPServer(serverAddress, RequestHandler)
  server.serve_forever()
