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

         a_code=[]
         a_time=[]
         a_when=[]
         answers=[a_code,a_time,a_when]
         for a in q.childNodes:
            if a.nodeType == Node.ELEMENT_NODE:
               a_code.append (a.getAttribute("answer_code"))
               a_time.append (a.getAttribute("needed_time"))
               a_when.append (a.getAttribute("datetime"))

         self.staticstics.append ([id, c, cs, ws, w, answers])
 
   def Timestamp(self):
      return str(datetime.datetime.today().isoformat()).split(".")[0]

   def __init__(self,filename="DL-A-2007.stat.xml"):
      self.filename=filename

      self.GetStatistics()
