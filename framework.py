import questions, statistic

class Framework:
   def AskQuestion(self):
      qid = "TB305" 
      self.q.AskQuestion (qid)
      f.id = qid
      f.question = self.q.question
      f.answera = self.q.answera
      f.answerb = self.q.answerb
      f.answerc = self.q.answerc
      f.answerd = self.q.answerd

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
