import questions, statistic
import random as r

class Framework:
   def AskQuestion(self):
      if self.method == "BadQuestions":
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
      return

   def FindBadQuestion(self):
      return

   def FindGoodQuestion(self):
      return

   def Close(self):
      self.s.WriteFile()

   def __init__(self):
      self.q = questions.Questions()
      self.s = statistic.Statistic()
      self.method = ""
