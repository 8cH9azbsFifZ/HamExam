#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os
import datetime

from xml.dom.ext import PrettyPrint
from StringIO import StringIO

def toprettyxml_fixed (node): #, encoding='utf-8'):
   tmpStream = StringIO()
   PrettyPrint(node, stream=tmpStream)# , encoding=encoding)
   return tmpStream.getvalue()

class Statistic:
   def IncreaseCounter(self, qid, how, answer, time):
      """
      Return True, is question is good
      """
      nq = self.FindQuestion (qid)
      if nq >= 0:
         for q in  self.root.getElementsByTagName("question"):
            id = q.getAttribute ("id")
            if id == qid:
               break
         
         c = int(q.getAttribute ("c"))
         w = int(q.getAttribute ("w"))
         cs = int(q.getAttribute ("cs"))
         ws = int(q.getAttribute ("ws"))
      
      else:
         print "NEU",qid
         q = self.stat.createElement(u'question')
         q.setAttribute("id",qid)

         sss = self.root.getElementsByTagName("learning")[0]
         sss.appendChild(q)

         c=0
         w=0
         cs=0
         ws=0

         self.statistics.append ([qid, c, cs, ws, w, ""])
         nq = self.FindQuestion (qid)

      if how == True:
         c += 1
         cs += 1
         ws = max(ws-1,0)
      else:
         w += 1
         ws += 1
         cs = min(cs-1,0)

      if c < 0:
         c = 0
      if cs < 0:
         cs = 0
      if w < 0:
         w = 0
      if ws < 0:
         ws = 0
     
      # in-memory statistics
      self.statistics[nq][1] = c
      self.statistics[nq][2] = cs
      self.statistics[nq][3] = ws
      self.statistics[nq][4] = w

      # xml file stuff
      q.setAttribute("c",str(c))
      q.setAttribute("w",str(w))
      q.setAttribute("cs",str(cs))
      q.setAttribute("ws",str(ws))
      

      t = self.Timestamp()
      a = [1,2,4,8][(["a","b","c","d"]).index(answer)]
      nt = int(time*1000)
   
      qq = self.stat.createElement("answer_clicked")
      qq.setAttribute ("datetime", str(t))
      qq.setAttribute ("answer_code", str(a))
      qq.setAttribute ("needed_time", str(nt))
      q.appendChild(qq)

      if float(ws) > 0.:
         rr = 0.
      else:
         rr = float(cs)*self.norm

      return rr >= self.ratio

   def WriteFile(self):
      print "Writing statistics file",self.filename
      ss=toprettyxml_fixed(self.root)
      f=open(self.filename,"w")
      print >>f,"<!DOCTYPE AFUTrainerStatistics>"
      f.write(ss)
      f.close()
   
   def OpenFile(self):
      print "Opening statistics file",self.filename
      self.stat = minidom.parse (self.filename)
      self.root = self.stat.documentElement

      self.date = self.root.getAttribute ("date")
      self.version = self.root.getAttribute ("version")
      self.name = self.root.getAttribute ("name")


   def GetStatistics(self):
      print "Parsing statistics xml"
      self.statistics = []

      self.ratio = .75
      self.mincorrect = 5.
      self.newquestion = []
      self.goodquestion = []
      self.badquestion = []
      self.norm = 1./self.mincorrect

      for q in self.root.getElementsByTagName("question"):
         id = q.getAttribute ("id")
         c = q.getAttribute ("c") 
         cs = q.getAttribute ("cs")
         ws = q.getAttribute ("ws")
         w = q.getAttribute ("w")

         if float(ws) > 0.:
            rr = 0.
         else:
            rr = float(cs)*self.norm

         if rr >= self.ratio:
            self.goodquestion.append (id)
         elif rr >= 0:
            self.badquestion.append (id)
         else: # never reached
            self.newquestion.append (id)

         answers = []
         for a in q.childNodes:
            if a.nodeType == Node.ELEMENT_NODE:
               code = a.getAttribute("answer_code")
               time = a.getAttribute("needed_time")
               when = a.getAttribute("datetime")
               answers.append ([code,time,when])

         self.statistics.append ([id, c, cs, ws, w, answers])

   def GetPriority(self,qid):
      return

   def FindQuestion(self,qid):
      i = 0
      for s in self.statistics:
         if s[0]  == qid:
            return i
         i += 1
      return -1

   def ThisQuestion(self,qid):
      q = self.FindQuestion (qid)
      if q >= 0:
         c = self.statistics[q][1]
         w = self.statistics[q][4]
         cs = self.statistics[q][2]
         ws = self.statistics[q][3]
      else:
         c=str(0)
         w=str(0)
         cs=str(0)
         ws=str(0)
      return [str(c),str(w),str(cs),str(ws)]

   def Timestamp(self):
      return str(datetime.datetime.today().isoformat()).split(".")[0]

   def __init__(self,filename="DL-A-2007.stat.xml"):
      self.filename=filename
      
      self.OpenFile()
      self.GetStatistics()
