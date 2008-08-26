#!/usr/bin/python
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import posixpath, urllib, os

import framework

class MyHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      if self.path.endswith(".afu"):
         self.AFU()
      else:
         f = self.send_head()
         if f:
            self.copyfile(f, self.wfile)
            f.close()
         
   def do_HEAD(self):
     f = self.send_head()
     if f:
         f.close()

   def send_head(self):
      path = self.translate_path(self.path)
      if os.path.isdir(path):
         self.send_error(403, "Directory listing not supported")
         return None
      try:
         f = open(path, 'rb')
      except IOError:
         self.send_error(404, "File not found")
         return None
      self.send_response(200)
      self.send_header("Content-type", self.guess_type(path))
      self.end_headers()
      return f

   def translate_path(self, path):
      path = posixpath.normpath(urllib.unquote(path))
      words = string.splitfields(path, '/')
      words = filter(None, words)
      path = os.getcwd()
      for word in words:
         drive, word = os.path.splitdrive(word)
         head, word = os.path.split(word)
         if word in (os.curdir, os.pardir): continue
         path = os.path.join(path, word)
      return path

   def copyfile(self, source, outputfile):
      BLOCKSIZE = 8192
      while 1:
         data = source.read(BLOCKSIZE)
         if not data: break
         outputfile.write(data)

   def guess_type(self, path):
      base, ext = posixpath.splitext(path)
      if self.extensions_map.has_key(ext):
         return self.extensions_map[ext]
      ext = string.lower(ext)
      if self.extensions_map.has_key(ext):
         return self.extensions_map[ext]
      else:
         return self.extensions_map['']

   extensions_map = {
      '': 'text/plain',   # Default, *must* be present
      '.html': 'text/html',
      '.htm': 'text/html',
      '.gif': 'image/gif',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      }

   def AFU(self):
      if self.path.endswith("a.afu") or self.path.endswith("b.afu") or self.path.endswith("c.afu") or self.path.endswith("d.afu"):
         answer = (self.path.split("/")[-1]).replace(".afu","")
         if not f.EvalQuestion (answer):
            self.WrongAnswer()
         else:
            self.AskQuestion()
      elif self.path.endswith("hint.afu"):
         self.DisplayHint()
      elif self.path.endswith("menue.afu"):
         self.DisplayMenu()
      elif self.path.endswith("askquestion.afu"):
         self.AskQuestion()
      else:
         self.StartDisplay()

   def DisplayHint(self):
      self.SendHeader() 
      print "Hint:",f.hint
      self.wfile.write ("<html><head><meta http-equiv=refresh content=\"0; URL=/"+f.hint+"\"></head></html>")

   def SendHeader(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

   def DisplayQuestion(self):
      self.wfile.write("<div class=id>"+f.id+"</div>")
      self.wfile.write("<div class=question>")
      self.wfile.write(f.question)
      self.wfile.write("</div>")

   def WrongAnswer(self):
      self.SendHeader() 
      self.base="http://127.0.0.1:8080"
      self.wfile.write("<html><head><base href="+self.base+"/Questions/></head><body>")
      self.wfile.write("<b>Falsche Antwort<b><br>")
      self.DisplayQuestion()
      self.wfile.write("<div class=correctanswer>"+f.answera+"</div>")
      

   def StartDisplay(self):
      self.SendHeader()
      self.base="http://127.0.0.1:8080"

      self.wfile.write("<frameset border=0 frameborder=0 framespacing=0 marginwidth=0 rows=70px,*>")
      self.wfile.write("<frame name=menue src=menue.afu scrolling=no noresize>")
      self.wfile.write("<frame name=main src=askquestion.afu scrolling=auto noresize>")
      self.wfile.write("</frameset>")

   def AskQuestion(self):
      self.base="http://127.0.0.1:8080"
      self.wfile.write("<html><head><base href="+self.base+"/Questions/></head><body>")

      f.AskQuestion()
      self.DisplayQuestion()

      self.wfile.write("<div class=answer>")
      self.wfile.write("<a href="+self.base+"/a.afu class=button>A</a>"+f.answera+"<br>")
      self.wfile.write("<a href="+self.base+"/b.afu class=button>B</a>"+f.answerb+"<br>")
      self.wfile.write("<a href="+self.base+"/c.afu class=button>C</a>"+f.answerc+"<br>")
      self.wfile.write("<a href="+self.base+"/d.afu class=button>D</a>"+f.answerd+"<br>")
      self.wfile.write("</div>")

      self.wfile.write("<div class=hint>")
      self.wfile.write("<a href="+self.base+"/hint.afu>Hinweis</a></div>")

      self.wfile.write("</body></html>")

   def DisplayMenu(self):
      self.SendHeader()
      self.base="http://127.0.0.1:8080"
      self.stylefile=""

      self.wfile.write("<html><head><base target=main><link href="+self.stylefile+" rel=stylesheet type=text/css></head>")
      self.wfile.write("<body><div class=menue>")
      self.wfile.write("<a class=menue href="+self.base+"/askquestion.afu>Abfragen</a>")
      self.wfile.write("</div></body></html>")
      

   def do_POST(self):
      global rootnode
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
          query=cgi.parse_multipart(self.rfile, pdict)
      self.send_response(301)
      
      self.end_headers()
      upfilecontent = query.get('upfile')
      print "filecontent", upfilecontent[0]
      self.wfile.write("<HTML>POST OK.<BR><BR>");
      self.wfile.write(upfilecontent[0]);
         
def main():
   try:
      global f 
      f = framework.Framework()
      server = HTTPServer(('', 8080), MyHandler)
      print 'started httpserver...'
      server.serve_forever()
   except KeyboardInterrupt:
      print '^C received, shutting down server'
      server.socket.close()

if __name__ == '__main__':
    main()
