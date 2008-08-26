#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os

class Questions:
   loud = False

   def GetQuestions(self):   
      if self.loud:
         print "Get Questions"

      self.GetHints ()

      self.questions = []

      for q in self.file.getElementsByTagName("question"):
         id = q.getAttribute ("id")
         
         hint = self.GetHint(id)

         answers = []
         for c in q.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:

               content=[]
               for child in c.childNodes:
                  if child.nodeType == Node.TEXT_NODE:
                     content.append(child.nodeValue)
               if content:
                  strContent = string.join(content)

               if c.nodeName == "textquestion":
                  textquestion = strContent
               elif c.nodeName == "textanswer":
                  if c.getAttribute("correct") == "true":
                     correct = True
                  else:
                     correct = False
                  answer = content
                  answers.append ([answer, correct])

         self.questions.append ([id, textquestion,answers, hint])

   def GetHints(self):
      if self.loud:
         print "Get hints"

      self.hints = []
      for h in self.root.getElementsByTagName ("hint"):
         id = h.getAttribute ("question")
         content=[]
         for child in h.childNodes:
            if child.nodeType == Node.TEXT_NODE:
               content.append(child.nodeValue)
         if content:
            strContent = string.join(content)

         ss = strContent.split("<a href=\"")[1].split("\">")[0]

         self.hints.append ([id, ss])

   def GetHint(self,id):
      if self.loud:
         print "Get hint:",id

      for h in self.hints:
         if h[0] == id:
            return h[1]
      return ""

   def GetChapters(self):
      if self.loud:
         print "Get chapters"

      chapters=[]
      for c in self.root.childNodes:
         if c.nodeType == Node.ELEMENT_NODE:
            if c.nodeName == "chapter":
               id1 = c.getAttribute("id")
               name1 = c.getAttribute("name")
         for d in c.childNodes:
            if d.nodeType == Node.ELEMENT_NODE:
               if d.nodeName == "chapter":
                  id2 = d.getAttribute("id")
                  name2 = d.getAttribute("name")
            for e in d.childNodes:
               if e.nodeType == Node.ELEMENT_NODE:
                  if e.nodeName == "chapter":
                     id3 = e.getAttribute("id")
                     name3 = e.getAttribute("name")

   def GetBasicProperties(self):
      if self.loud:
         print "Get basic properties"

      #self.title = self.root.getAttribute("title")
      #publisher
      #version -published
      #contact
      #exam id="T" name="Technische Kenntnisse / Klasse A" duration="90" maxerrorpoints="13"
      return

   def AskQuestion(self,id):
      if self.loud:
         print "Ask question:",id

      for q in self.questions:
         if q[0] == id:
            break

      self.id = id
      self.question = q[1]
      self.correct = "a" #FIXME
      self.answera = q[2][0][0][0]
      self.answerb = q[2][1][0][0]
      self.answerc = q[2][2][0][0]
      self.answerd = q[2][3][0][0]
      self.hint = q[3]

   def __init__(self,filename="Questions/questions.xml"):
      self.filename=filename
      self.file = minidom.parse (self.filename)
      self.root = self.file.documentElement

      self.GetQuestions()


#q = Questions()

#q.AskQuestion("TB305")
