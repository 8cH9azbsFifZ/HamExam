import questions, statistic
import random as r
import time

class Framework:
   def AskQuestion(self):
      if self.method == "BadQuestions":
         print "Bad question"
         qid = self.FindBadQuestion()
      elif self.method == "GoodQuestions":
         print "Good questions"
         qid = self.FindGoodQuestion()
      elif self.method == "NewQuestions":
         print "New question"
         qid = self.FindNewQuestion()
      else:
         qid = self.FindAnyQuestion()

      qid = "TE320" #"TD218"
      self.q.AskQuestion (qid)
      self.id = qid
      self.question = self.q.question
      self.answera = self.q.answera
      self.answerb = self.q.answerb
      self.answerc = self.q.answerc
      self.answerd = self.q.answerd
      self.answercorrect = self.q.answercorrect
      self.hint = self.q.hint
      self.correct, self.wrong, self.correct_successive, self.wrong_successive = self.s.ThisQuestion (self.id)

      self.time0 = time.time()

   def EvalQuestion(self, answer):
      if self.q.correct == answer:
         c = True
      else:
         c = False

      print "Answer was:",answer
      print "Correct was:",self.q.correct

      self.time1 = time.time()
      dt = self.time1-self.time0

      self.s.IncreaseCounter (self.id, c, self.q.RealAnswer(answer), dt)

      return c

   def Method(self,method="AnyQuestion"):
      self.method=method

   def FindAnyQuestion(self):
      return r.sample(self.q.questions,1)[0]

   def FindNewQuestion(self):
      return r.sample(self.s.newquestion,1)[0]

   def FindBadQuestion(self):
      return r.sample(self.s.badquestion,1)[0]

   def FindGoodQuestion(self):
      return r.sample(self.s.newquestion,1)[0]

   def Close(self):
      self.s.WriteFile()

   def CategorizeQuestions(self):
      print "Categorize questions"
      for q in self.q.questions:
         if not (q[0] in self.s.goodquestion):
            if not (q[0] in self.s.badquestion):
               if not (q[0] in self.s.newquestion):
                  self.s.newquestion.append (q[0])
      print "total, good, bad, new:",len(self.q.questions),len(self.s.goodquestion),len(self.s.badquestion),len(self.s.newquestion)

   def __init__(self,method="BadQuestions",catalog="TechnikA"):
      if catalog == "TechnikA":
         stat = "TechnikA/DL-A-2007.stat.xml"
      elif catalog == "TechnikE":
         stat = "TechnikE/DL-E-2007.stat.xml"
      elif catalog == "BetriebAE":
         stat = "BetriesAE/FIXMEtat.xml" #FIXME
   
      self.question_dir = catalog+"/www.oliver-saal.de/software/afutrainer/download/"
      self.hint_dir = catalog+"/"
      quest = self.question_dir + "questions.xml"

      self.q = questions.Questions(filename=quest)
      self.s = statistic.Statistic(filename=stat)
      self.method = method
      self.CategorizeQuestions()
