#!/usr/bin/python
import string,cgi,time,posixpath, urllib, os
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
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
      self.SendHeader()
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
      elif self.path.endswith("method.afu"):
         self.DisplayMethod()
      elif self.path.endswith("statistics.afu"):
         self.DisplayStatistics()
      elif self.path.endswith("askquestion.afu"):
         self.AskQuestion()
      elif self.path.endswith("showquestion.afu"):
         self.AskQuestion(update=False)
      else:
         self.StartDisplay()

   def DisplayStatistics(self):
      self.ShowHead()
      self.wfile.write ("<h2>Statistics...</h2>")

   def DisplayMethod(self):
      self.ShowHead()
      self.wfile.write ("<h2>Abfragemethode</h2>")

      self.wfile.write ("<h2>Fragenkatalog</h2>")

   def ShowHead(self,question=False):
      self.wfile.write ("<html><head><base href="+base+question_dir+">")
      self.wfile.write ("<link href="+stylefile+" rel=stylesheet type=text/css>")
      self.wfile.write ("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf8\">")
      
      if question:
         self.wfile.write ("<SCRIPT LANGUAGE=\"JavaScript\">")
         self.wfile.write ("var inNav = navigator.appVersion.indexOf(\"MSIE\") < 0;")
         self.wfile.write ("function eval_key (event) {")
         self.wfile.write ("var key = (inNav==1) ? event.which : event.keyCode;")
         self.wfile.write ("if (key == 65) {   window.location = \""+base+"/a.afu\";")
         self.wfile.write ("} else if (key == 66) {  window.location = \""+base+"/b.afu\";")
         self.wfile.write ("} else if (key == 67) {  window.location = \""+base+"/c.afu\";")
         self.wfile.write ("} else if (key == 68) {  window.location = \""+base+"/d.afu\";")
         self.wfile.write ("}")
         self.wfile.write ("}")
         self.wfile.write ("document.onkeydown = eval_key;")
         self.wfile.write ("</script>")

      self.wfile.write ("</head><body>")
            
   def DisplayHint(self):
      print "Hint:",f.hint
      self.wfile.write ("<html><head><meta http-equiv=refresh content=\"0; URL=/"+f.hint+"\"></head></html>")

   def SendHeader(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

   def DisplayQuestion(self):
      self.wfile.write("<div class=id>"+f.id+"</div>")
      self.wfile.write("<div class=question>")
      self.wfile.write(f.question.encode("utf8"))
      self.wfile.write("</div>")
      self.wfile.write("<div class=statistics>Richtig: "+f.correct+" <br>Falsch: "+f.wrong+"</div>")

   def WrongAnswer(self):
      self.ShowHead()
      self.wfile.write("<div class=wronganswer>Falsche Antwort</div>")
      self.DisplayQuestion()
      self.wfile.write("<div class=correctanswer>"+f.answercorrect.encode("utf8")+"</div>")
      

   def StartDisplay(self):
      self.wfile.write("<frameset border=0 frameborder=0 framespacing=0 marginwidth=0 rows=30px,*>")
      self.wfile.write("<frame name=menue src=menue.afu scrolling=no noresize>")
      self.wfile.write("<frame name=main src=askquestion.afu scrolling=auto noresize>")
      self.wfile.write("</frameset>")

   def AskQuestion(self,update=True):
      self.ShowHead(question=True)
      self.wfile.write("<body>")

      if update:
         f.AskQuestion()

      self.DisplayQuestion()

      self.wfile.write("<div class=answer>")
      self.wfile.write("<a href="+base+"/a.afu class=button1>A</a>"+f.answera.encode("utf8")+"<br>")
      self.wfile.write("<a href="+base+"/b.afu class=button1>B</a>"+f.answerb.encode("utf8")+"<br>")
      self.wfile.write("<a href="+base+"/c.afu class=button1>C</a>"+f.answerc.encode("utf8")+"<br>")
      self.wfile.write("<a href="+base+"/d.afu class=button1>D</a>"+f.answerd.encode("utf8")+"<br>")
      self.wfile.write("</div>")

      self.wfile.write("<div class=button>")
      self.wfile.write("<a href="+base+"/a.afu class=button>A</a>")
      self.wfile.write("<a href="+base+"/b.afu class=button>B</a>")
      self.wfile.write("<a href="+base+"/c.afu class=button>C</a>")
      self.wfile.write("<a href="+base+"/d.afu class=button>D</a>")
      self.wfile.write("</div>")

      self.wfile.write("<div class=hint>")
      self.wfile.write("<a href="+base+"/hint.afu target=hint>Hinweis</a></div>")

      self.wfile.write("</body></html>")

   def DisplayMenu(self):
      self.wfile.write("<html><head><base target=main><link href="+stylefile+" rel=stylesheet type=text/css></head>")
      self.wfile.write("<body class=menue><div class=menue>")
      self.wfile.write("<a class=menue href="+base+"/askquestion.afu>Abfragen</a>")
      self.wfile.write("<a class=menue href="+base+"/method.afu>Abfragemethode</a>")
      self.wfile.write("<a class=menue href="+base+"/statistic.afu>Statistik</a>")
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
   global f,port,base,stylefile,question_dir
   port = 8080
   base = "http://127.0.0.1:"+str(port)+"/"
   question_dir = "/TechnikA/www.oliver-saal.de/software/afutrainer/download/"
   stylefile = base+"/style.css"

   try:
      f = framework.Framework()
      server = HTTPServer(('', port), MyHandler)
      print 'Started httpserver on port',port
      print "Terminate with Ctrl+C"
      server.serve_forever()
   except KeyboardInterrupt:
      print '^C received, shutting down http server'
      f.Close()
      server.socket.close()

if __name__ == '__main__':
    main()
