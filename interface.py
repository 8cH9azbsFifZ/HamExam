#!/usr/bin/python
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import questions, statistic

class MyHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      self.send_response(200)
      self.send_header('Content-type',	'text/html')
      self.end_headers()

      self.wfile.write("abc")



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

   def __init__(self):
      self.q = questions.Questions()
         
def main():
   try:
      server = HTTPServer(('', 8080), MyHandler)
      print 'started httpserver...'
      server.serve_forever()
   except KeyboardInterrupt:
      print '^C received, shutting down server'
      server.socket.close()

if __name__ == '__main__':
    main()
