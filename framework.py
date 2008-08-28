import questions, statistic
import random as r

class Framework:
   def AskQuestion(self):
      if self.method == "BadQuestions":
         #FIXME
         qid = self.FindBadQuestion()
      elif self.method == "GoodQuestions":
         #FIXME
         qid = self.FindGoodQuestion()
      elif self.method == "NewQuestions":
         #FIXME
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
      self.correct, self.wrong = self.s.ThisQuestion (self.id)

   def EvalQuestion(self, answer):
      if self.q.correct == answer:
         c = True
      else:
         c = False

      self.s.IncreaseCounter (self.id, c, self.q.RealAnswer(answer))

      return c

   def FindAnyQuestion(self):
      nq = int (r.random()*self.q.nquestions)
      return self.q.questions[nq][0]

   def FindNewQuestion(self):
      nq = r.randint(0,self.s.nnewquestion)
      return self.s.newquestion[nq]

   def FindBadQuestion(self):
      nq = r.randint(0,self.s.nbadquestion)
      return self.s.badquestion[nq]

   def FindGoodQuestion(self):
      nq = r.randint(0,self.s.ngoodquestion)
      return self.s.goodquestion[nq]

   def Close(self):
      self.s.WriteFile()

   def __init__(self,method=""):
      self.q = questions.Questions()
      self.s = statistic.Statistic()
      self.method = method
