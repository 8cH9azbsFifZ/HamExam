#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os

class Statistic:
   def IncreaseCounter(self, id, how):
      return

   def __init__(self,filename="DL-A-2007.stat.xml"):
      self.filename=filename
      self.stat = minidom.parse (self.filename)
      self.root = self.stat.documentElement
      self.date = self.root.getAttribute ("date")
      self.version = self.root.getAttribute ("version")
      self.name = self.root.getAttribute ("name")

      id=[]
      c=[]     #correct
      cs=[]
      ws=[]
      w=[]     #wrong
      for q in self.root.getElementsByTagName("question"):
         id.append (q.getAttribute ("id"))
         c.append (q.getAttribute ("c"))
         cs.append (q.getAttribute ("cs"))
         ws.append (q.getAttribute ("ws"))
         w.append (q.getAttribute ("w"))
         a_code=[]
         a_time=[]
         a_when=[]
         answers=[a_code,a_time,a_when]
         for a in q.childNodes:
            if a.nodeType == Node.ELEMENT_NODE:
               a_code.append (a.getAttribute("answer_code"))
               a_time.append (a.getAttribute("needed_time"))
               a_when.append (a.getAttribute("datetime"))
               
      print id[0],c[0],cs[0],ws[0],w[0],answers


