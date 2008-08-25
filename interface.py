#!/usr/bin/python
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import posixpath, urllib, os

import questions, statistic

class MyHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      if self.path.endswith(".afu"):
         self.Good()
      else:
         f = self.send_head()
         if f:
            self.copyfile(f, self.wfile)
            f.close()
         
   def do_HEAD(self):
     """Serve a HEAD request."""
     f = self.send_head()
     if f:
         f.close()

   def send_head(self):
      """Common code for GET and HEAD commands.

      This sends the response code and MIME headers.

      Return value is either a file object (which has to be copied
      to the outputfile by the caller unless the command was HEAD,
      and must be closed by the caller under all circumstances), or
      None, in which case the caller has nothing further to do.

      """
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
      """Translate a /-separated PATH to the local filename syntax.

      Components that mean special things to the local file system
      (e.g. drive or directory names) are ignored.  (XXX They should
      probably be diagnosed.)

      """
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
      """Copy all data between two file objects.

      The SOURCE argument is a file object open for reading
      (or anything with a read() method) and the DESTINATION
      argument is a file object open for writing (or
      anything with a write() method).

      The only reason for overriding this would be to change
      the block size or perhaps to replace newlines by CRLF
      -- note however that this the default server uses this
      to copy binary data as well.

      """

      BLOCKSIZE = 8192
      while 1:
         data = source.read(BLOCKSIZE)
         if not data: break
         outputfile.write(data)

   def guess_type(self, path):
      """Guess the type of a file.

      Argument is a PATH (a filename).

      Return value is a string of the form type/subtype,
      usable for a MIME Content-type header.

      The default implementation looks the file's extension
      up in the table self.extensions_map, using text/plain
      as a default; however it would be permissible (if
      slow) to look inside the data to make a better guess.

      """

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

 

   def Good(self):
      self.send_response(200)
      self.send_header('Content-type',	'text/html')
      self.end_headers()
      self.wfile.write("<html><head><base href=\"http://127.0.0.1:8080/Questions/\"></head><body>")

      q.AskQuestion("TB305")
      
      self.wfile.write(q.question)
      self.wfile.write(q.answera)
      self.wfile.write(q.answerb)
      self.wfile.write(q.answerc)
      self.wfile.write(q.answerd)

      self.wfile.write("</body></html>")



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
      global q 
      q = questions.Questions()
      server = HTTPServer(('', 8080), MyHandler)
      print 'started httpserver...'
      server.serve_forever()
   except KeyboardInterrupt:
      print '^C received, shutting down server'
      server.socket.close()

if __name__ == '__main__':
    main()
