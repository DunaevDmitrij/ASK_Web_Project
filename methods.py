# For generateToken
import random
import string
# For popularTags
from ask.models import Tag,Question
import operator
# For lastUsers
from ask.models import User
# For countRating
from ask.models import Rates
# For sortQuest
from ask.models import Question
# For mailNotify
from django.core.mail import send_mail
# For lastNotifs
from ask.models import Notifications

#----------------------------
symbols = " ".join(string.letters).split();
for i in range(10):
  symbols.append(str(i));
#----------------------------
def generateToken(length):
  token = ""
  for i in range(int(length)):
    token = token + symbols[random.randrange(len(symbols))]
  return token

def popularTags(amount):
  tags = Tag.objects.all()
  frequency = {}
  for tag in tags:
    frequency[tag.name]=0
  questions = Question.objects.all()
  for question in questions:
    for tag in question.tag.all():
      frequency[tag.name]+=1
  popular = sorted(frequency.items(),key=lambda x:x[1],reverse=True)
  popularTags = []
  for elem in popular:
    popularTags.append(tags.get(name=elem[0]))
  return popularTags[:amount]

def lastUsers(amount):
  users = sorted(User.objects.all(),key = lambda User:User.regDate,reverse=True)
  return users[:amount]

def countRating(questionData):
  questionRates = Rates.objects.filter(question=questionData)
  rating = 0
  for rate in questionRates:
    if (rate.rate == True):
      rating = rating + 1
    else:
      rating = rating - 1
  return rating

def sortQuest(typeOfSort):
  quests = Question.objects.all()
  if (typeOfSort == "date"):
    return sorted(quests,key=lambda Question:Question.createDate,reverse=True)
  else:
    return sorted(quests,key=lambda x:countRating(x),reverse=True)

def mailNotify(notification):
  if (notification.answer_comment):
    mailData = "You have got new comment to: " + notification.comment.content_object.content + " - "+notification.comment.text
    send_mail(subject="ASK Notification",message=mailData,from_email='ask.dunaev.mail@gmail.com',recipient_list=[notification.comment.content_object.author.email])
  else:
    mailData= "You have got new answer to: " + notification.answer.question.content + " - " + notification.answer.content
    send_mail(subject="ASK Notification",message=mailData,from_email='ask.dunaev.mail@gmail.com',recipient_list=[notification.question.author.email])
  return mailData

def lastNotifs(userData,amount):
  notifsLast = sorted(Notifications.objects.filter(user=userData),key = lambda Notifications:Notifications.createDate,reverse=True)
  return notifsLast[:amount]

