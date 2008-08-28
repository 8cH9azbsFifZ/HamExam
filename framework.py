import questions, statistic
import random as r

class Framework:
   def AskQuestion(self):
      if self.method == "BadQuestions":
         print "Bad question"
         qid = self.FindBadQuestion()
      elif self.method == "GoodQuestions":
         qid = self.FindGoodQuestion()
      elif self.method == "NewQuestions":
         qid = self.FindNewQuestion()
      else:
         qid = self.FindAnyQuestion()

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

   def EvalQuestion(self, answer):
      if self.q.correct == answer:
         c = True
      else:
         c = False

      self.s.IncreaseCounter (self.id, c, self.q.RealAnswer(answer))

      return c

   def Method(self,method="AnyQuestion"):
      self.method=method

   def FindAnyQuestion(self):
      nq = r.randint(0,self.q.nquestions)
      return self.q.questions[nq][0]

   def FindNewQuestion(self):
      nq = r.randint(0,self.s.nnewquestion-1)
      return self.s.newquestion[nq]

   def FindBadQuestion(self):
      nq = r.randint(0,self.s.nbadquestion-1)
      return self.s.badquestion[nq]

   def FindGoodQuestion(self):
      nq = r.randint(0,self.s.ngoodquestion-1)
      return self.s.goodquestion[nq]

   def Close(self):
      self.s.WriteFile()

   def CategorizeQuestions(self):
      print "Categorize questions"
      for q in self.q.questions:
         if not (q[0] in self.s.goodquestion):
            if not (q[0] in self.s.badquestion):
               if not (q[0] in self.s.newquestion):
                  self.s.newquestion.append (q[0])
                  self.s.nnewquestion+=1
      print "total, good, bad, new:",self.q.nquestions,self.s.ngoodquestion,self.s.nbadquestion,self.s.nnewquestion

   def __init__(self,method="",catalog="TechnikA"):
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
