#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os
import datetime

class Statistic:
   def IncreaseCounter(self, qid, how, answer):
      nq = self.FindQuestion (qid)
      for q in  self.root.getElementsByTagName("question"):
         id = q.getAttribute ("id")
         if id == qid:
            break
      
      c = int(q.getAttribute ("c"))
      w = int(q.getAttribute ("w"))
      cs = int(q.getAttribute ("cs"))
      ws = int(q.getAttribute ("ws"))

      if how == True:
         c += 1
         cs += 1
      else:
         w += 1
         ws += 1
      
      q.setAttribute("c",str(c).encode("utf8"))
      q.setAttribute("w",str(w).encode("utf8"))
      q.setAttribute("cs",str(cs).encode("utf8"))
      q.setAttribute("ws",str(ws).encode("utf8"))
      

      t = self.Timestamp()
      a = [1,2,4,8][(["a","b","c","d"]).index(answer)]
      nt = 15000 # FIXME
      
      # FIXME
      #qq = q.createElement ("answer_clicked")
      #qq.setAttribute ("datetime", str(t).encode("utf8"))
      #qq.setAttribute ("answer_code", str(a).encode("utf8"))
      #qq.setAttribute ("needed_time", str(nt).encode("utf8"))
      #qq.appendChild()

      print "Yeas",qid,id,c,cs,ws,w,t

   def GetStatistics(self):
      self.stat = minidom.parse (self.filename)
      self.root = self.stat.documentElement
      self.date = self.root.getAttribute ("date")
      self.version = self.root.getAttribute ("version")
      self.name = self.root.getAttribute ("name")

      self.statistics = []

      for q in self.root.getElementsByTagName("question"):
         id = q.getAttribute ("id")
         c = q.getAttribute ("c") 
         cs = q.getAttribute ("cs")
         ws = q.getAttribute ("ws")
         w = q.getAttribute ("w")

         answers = []
         for a in q.childNodes:
            if a.nodeType == Node.ELEMENT_NODE:
               code = a.getAttribute("answer_code")
               time = a.getAttribute("needed_time")
               when = a.getAttribute("datetime")
               answers.append ([code,time,when])

         self.statistics.append ([id, c, cs, ws, w, answers])

   def FindQuestion(self,qid):
      i = 0
      for s in self.statistics:
         if s[0]  == qid:
            return i
         i += 1
      return -1

   def ThisQuestion(self,qid):
      q = self.FindQuestion (qid)
      c = self.statistics[q][1]
      w = self.statistics[q][4]
      return [c,w]

   def Timestamp(self):
      return str(datetime.datetime.today().isoformat()).split(".")[0]

   def __init__(self,filename="DL-A-2007.stat.xml"):
      self.filename=filename

      self.GetStatistics()
      
