import questions, statistic

class Framework:
   def AskQuestion(self):
      qid = str("TB305" )
      self.q.AskQuestion (qid)
      self.id = qid
      self.question = self.q.question
      self.answera = self.q.answera
      self.answerb = self.q.answerb
      self.answerc = self.q.answerc
      self.answerd = self.q.answerd

   def EvalQuestion(self, answer):
      if self.q.correct == answer:
         c = True
      else:
         c = False
      return c

   def FindNewQuestion(self):
      return

   def FindBadQuestion(self):
      return

   def FindGoodQuestion(self):
      return

   def __init__(self):
      self.q = questions.Questions
      self.s = statistic.Statistic
