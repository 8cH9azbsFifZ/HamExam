#!/usr/bin/python
import sys, string
from xml.dom import minidom, Node
import os

class Questions:
   def __init__(self):
      self.filename="Questions/questions.xml"
      self.file = minidom.parse (self.filename)
      self.root = self.file.documentElement
      self.date = self.root.getAttribute ("date")
      self.version = self.root.getAttribute ("version")
      self.name = self.root.getAttribute ("name")

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



      def GetQuestions():      
         for q in self.file.getElementsByTagName("question"):
            id = q.getAttribute ("id")
            
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
                     correct = c.getAttribute("correct")
                     answer = content
                     answers.append ([answer, correct])

            print id, textquestion, answers

q=Questions()

