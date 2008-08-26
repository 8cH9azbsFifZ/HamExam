#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os
import datetime

class Statistic:
   def IncreaseCounter(self, id, how):

      #<question w="0" id="TA101" ws="0" c="6" cs="6" >
      #   <answer_clicked datetime="2007-09-13T02:56:34" answer_code="1" needed_time="14543" />

      return

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
      
