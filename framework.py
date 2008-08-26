import questions, statistic
import random as r

class Framework:
   def AskQuestion(self):
      qid = str("TB305")
      self.q.AskQuestion (qid)
      self.id = qid
      self.question = self.q.question
      self.answera = self.q.answera
      self.answerb = self.q.answerb
      self.answerc = self.q.answerc
      self.answerd = self.q.answerd
      self.answercorrect = self.q.answercorrect
      self.hint = self.q.hint

   def EvalQuestion(self, answer):
      if self.q.correct == answer:
         c = True
      else:
         c = False

      self.s.IncreaseCounter (self.id, c)

      return c

   def FindNewQuestion(self):
      nq = int (r.random()*self.q.nquestions)
      return self.q.questions[nq][0]

   def FindBadQuestion(self):
      return

   def FindGoodQuestion(self):
      return

   def __init__(self):
      self.q = questions.Questions()
      self.s = statistic.Statistic()
