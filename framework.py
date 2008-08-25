import questions, statistic

class Framework:
   def AskQuestion(self):
      qid = "TB305" 
      q.AskQuestion (qid)
      f.id = qid
      f.question = q.question
      f.answera = q.answera
      f.answerb = q.answerb
      f.answerc = q.answerc
      f.answerd = q.answerd

   def EvalQuestion(self, answer):
      if q.correct == answer:
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
