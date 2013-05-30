# Create your views here.
from django.template import loader, Context
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from ask.models import User,Question,Answer,Comments,Tag,UserTokens,Rates,Notifications
from django.contrib.auth import authenticate,login,logout
from ask.forms import LoginForm,RegistrationForm,NewQuestionForm,NewAnswerForm,SearchForm,NewCommentForm,ActivationForm
from django.core.mail import send_mail
from ask.methods import generateToken,popularTags,lastUsers,countRating,sortQuest,mailNotify,lastNotifs
from django.utils import simplejson

defaultDict = {
          "newQuestionForm":NewQuestionForm(),
          "loginForm":LoginForm(),
          "searchForm":SearchForm(),
          "tags":popularTags(5),
          "lastUsers":lastUsers(5),
          }

mimetype = 'application/json'

QuestionConTypeID = 10
AnswerConTypeID = 12

def index(request):
  newDict = defaultDict
  newDict["curUser"]=request.user
  return render(
          request,
          "index.html",
          newDict
          )

def ajaxTests(request):
  newDict = defaultDict
  newDict["curUser"]=request.user
  return render(
          request,
          "ajaxTests.html",
          newDict
          )

def ajaxIndexSend(request):
  if request.is_ajax():
    dataJSON=simplejson.loads(request.raw_post_data)
    return HttpResponse(dataJSON["sendData"])
  else:
    redirect('/quesion')

def ajaxIndexAnswer(request):
  if request.is_ajax():
    quest = Question.objects.get(id=31)
    data = {'bool':True}
    json = simplejson.dumps(data)
    return HttpResponse(json)
  else:
    redirect('/question')

def question(request):
  newDict = defaultDict 
  if ((request.method == u'GET') and (request.GET.has_key("sort"))):
    questions = sortQuest(request.GET["sort"])
    newDict["sort"]="sort="+request.GET["sort"]
  else:
    questions = sortQuest("date")
  paginator = Paginator(questions,20)
  newDict = defaultDict
  if ((request.method == u'GET') and (request.GET.has_key("page"))):
    pageNumber = int(request.GET["page"])
  else:
    pageNumber = 1
  page=paginator.page(pageNumber)
  newDict["page"]=page
  newDict["curUser"]=request.user
  return render(
              request,
              "question.html",
              newDict
              )

def questionID(request,qID):
  quest = Question.objects.get(id=qID)
  answs = Answer.objects.filter(question=quest)
  questComments = Comments.objects.filter(object_id = qID, content_type = QuestionConTypeID)
  Comms = Comments.objects.filter(content_type = AnswerConTypeID)
  quest.counter += 1;
  quest.save();
  if (Rates.objects.filter(user=request.user,question=quest).count()==0):
    rateStatData=True 
  else:
    rateStatData=False
  paginator = Paginator(answs,30)
  if ((request.method == u'GET') and (request.GET.has_key("page"))):
    pageNumber = int(request.GET["page"])
  else:
    pageNumber = 1
  page = paginator.page(pageNumber)
  answComments = []
  for a in page:
    answComments.append(Comms.filter(object_id = a.id))
  newDict = defaultDict
  newDict["quest"]=quest
  newDict["page"]=page
  newDict["newAnswerForm"]=NewAnswerForm()
  newDict["answComments"]=answComments
  newDict["questComments"]=questComments
  newDict["newCommentForm"]=NewCommentForm()
  newDict["curUser"]=request.user
  newDict["rating"]=countRating(quest)
  newDict["rateStat"]=rateStatData
  if (request.user.id==quest.author.id):
    newDict["mine"]=True
  else:
    newDict["mine"]=False
  return render(
            request,
            "questionID.html",
            newDict
            )

def loginator(request):
  if (request.method=='POST'):
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(username=form.cleaned_data['name'],password=form.cleaned_data['password'])
    else:
      newDict = defaultDict
      newDict["stat"]="badData"
      newDict["curUser"]=request.user
      return render(request,
                    "login.html",
                    newDict
                    )
    if user is not None:
      if not user.is_active:
        newDict = defaultDict
        newDict["stat"]="unactive"
        newDict["curUser"]=request.user
        return render(request,
                      "login.html",
                      newDict
                      )
      else:
        login(request,user)
        return redirect('/user/'+user.username)
    else:
      newDict = defaultDict
      newDict["stat"]="badData"
      newDict["curUser"]=request.user
      return render(request,
                    "login.html",
                    newDict
                    )
  else:
    if (request.user.is_authenticated):
      newDict = defaultDict
      newDict["curUser"]=request.user
      return render(request,
                    "login.html",
                    newDict
                    )

def deloginator(request):
  logout(request)
  return redirect('/')

def userpage(request,ususername):
  if (User.objects.filter(username=ususername).count()!=0):
    user=User.objects.get(username=ususername)
    questions = Question.objects.filter(author=user)
    newDict = defaultDict
    newDict["user"]=user
    newDict["questions"]=questions
    newDict["curUser"]=request.user
    newDict["answers"]=Answer.objects.filter(author=user)
    newDict["lastNotifs"]=lastNotifs(user,5)
    return render(
            request,
            "user.html",
            newDict
            )
  else:
    return redirect("/")

def user(request):
  if (request.user.username != "AnonymousUser"):
    return userpage(request,request.user.username)
  else:
    return redirect("/login/")

def registration(request):
  if (request.method=="POST"):
    form = RegistrationForm(request.POST)
    if form.is_valid():
      if (User.objects.filter(username=form.cleaned_data['username']).count()==0):
        usernamedata = username=form.cleaned_data['username']
        passworddata = form.cleaned_data["password"]
        emaildata = form.cleaned_data["email"]
        user = User.objects.create_user(username=usernamedata,email=emaildata)
        user.set_password(passworddata)
        user.is_active = False;
        user.save()
        usertoken = generateToken(64)
        ustok = UserTokens(user=user,token=usertoken)
        ustok.save()
        actStr = 'Copy string in form ASK/activate: ' + usertoken
        send_mail(subject='ASK registration',message=actStr,from_email='ask.dunaev.mail@gmail.com',recipient_list=[emaildata])
        newDict = defaultDict
        newDict["status"]="registered"
        newDict["curUser"]=request.user
        return render(
                request,
                "registration.html",
                newDict
               )
      else:
        newDict = defaultDict
        newDict["status"]="alreadyEx"
        newDict["curUser"]=request.user
        return render(
                request,
                "registration.html",
                newDict
            )
  else:
      newDict = defaultDict
      newDict["status"]="newPage"
      newDict["curUser"]=request.user
      return render(
              request,
              "registration.html",
              newDict
              )

def newquestion(request):
  if (request.method=="POST"):
    form = NewQuestionForm(request.POST)
    if (form.is_valid):
     if (Question.objects.filter(header=request.POST["header"]).count()==0):
        uscontent=request.POST["content"]
        usheader=request.POST["header"]
        ususer=User.objects.get(username=request.user.username)
        quest = Question(header=usheader,content=uscontent,author=ususer)
        quest.save()
        if ((request.POST.has_key("tag1")) and (Tag.objects.filter(name=request.POST["tag1"]).count()!=0)):
          tag = Tag.objects.get(name=request.POST["tag1"])
          quest.tag.add(tag)
        return redirect('/user/')
        if ((request.POST.has_key("tag2")) and (Tag.objects.filter(name=request.POST["tag2"]).count()!=0)):
          tag = Tag.objects.get(name=request.POST["tag2"])
          quest.tag.add(tag)
        return redirect('/user/')
        if ((request.POST.has_key("tag3")) and (Tag.objects.filter(name=request.POST["tag3"]).count()!=0)):
          tag = Tag.objects.get(name=request.POST["tag3"])
          quest.tag.add(tag)
        return redirect('/user/')
     else:
        newDict = defaultDict
        newDict["status"]="alreadyEx"
        newDict["curUser"]=request.user
        return render(
                 request,
                 "newquestion.html",
                 newDict
                )
  else:
    newDict = defaultDict
    newDict["status"]="newPage"
    newDict["curUser"]=request.user
    return render(request,
                  "newquestion.html",
                  newDict
                  )

def answer(request):
  if (request.method=="POST"):
    form = NewAnswerForm(request.POST)
    if (form.is_valid):
      uscontent=request.POST["content"]
      ususer=User.objects.get(username=request.user.username)
      usquestionID=int(request.POST["question"])
      usquestion=Question.objects.get(id=usquestionID)
      answ=Answer(content=uscontent,question=usquestion,author=ususer)
      answ.save()
      return questionID(request,usquestionID)
  else:
    return redirect('/question')

def ajaxAnswer(request):
  if request.is_ajax():
    dataJSON=simplejson.loads(request.raw_post_data)
    textData = dataJSON["text"]
    userData=User.objects.get(id=dataJSON["author"])
    questionData=Question.objects.get(id=dataJSON["question"])
    answ=Answer(content=textData,question=questionData,author=userData)
    answ.save()
    notif = Notifications(user = questionData.author, answer=answ, answer_comment=False)
    notif.save()
    mailNotify(notif)
    return HttpResponse("success")
  else:
    redirect('/question')

def ajaxSolver(request):
  if request.is_ajax():
    dataJSON=simplejson.loads(request.raw_post_data)
    aIDData = dataJSON["aID"]
    answer = Answer.objects.get(id=aIDData)
    answer.rightFlag = True
    answer.save()
    question = answer.question
    question.solved = True
    question.save()
    return HttpResponse("success")
  else:
    redirect('/question')

def activate(request):
  if ((request.method == 'POST') and (request.POST.has_key('token'))):
    activationData = request.POST['token']
    if (UserTokens.objects.filter(token=activationData).count()!=0):
      userToken = UserTokens.objects.get(token=activationData)
      userToken.user.is_active = True
      userToken.user.save()
      newDict = defaultDict
      newDict["status"]="actSuccess"
      newDict["curUser"]=request.user
      return render(
              request,
              "activation.html",
              newDict
              )
    else:
      newDict = defaultDict
      newDict["status"]="actFail"
      newDict["curUser"]=request.user
      return render(
              request,
              "activation.html",
              newDict
              )
  else:
    newDict = defaultDict
    newDict["curUser"]=request.user
    newDict["activationForm"]=ActivationForm()
    return render(
            request,
            "activation.html",
            newDict
            )

def search(request):
  if (request.method=="GET"):
    data = []
    newDict = defaultDict
    if ("question" in request.GET):
      data = Question.objects.all();
      data = data.filter(header__contains=request.GET["question"])
      newDict["search"]=request.GET["question"] 
    if ("tag" in request.GET):
      if (data == []):
        data = Question.objects.all();
      data = data.filter(tag=Tag.objects.get(name=request.GET["tag"]))
      newDict["tag"]=request.GET["tag"]
    newDict["data"]=data
    newDict["curUser"]=request.user
    return render(
            request,
            "search.html",
            newDict
            )
  else:
    newDict = defaultDict
    newDict["data"]=data
    newDict["curUser"]=request.user
    return render(
            request,
            "search.html",
            newDict
            )

def ajaxComment(request):
  if request.is_ajax():
    dataJSON=simplejson.loads(request.raw_post_data)
    textData = dataJSON["text"]
    authorIDData = User.objects.get(id=int(dataJSON["author"]))
    typeData = dataJSON["type"]
    idData = int(dataJSON["id"])
    if (typeData == QuestionConTypeID):
      objectData = Question.objects.get(id=idData)
    if (typeData == AnswerConTypeID):
      objectData = Answer.objects.get(id=idData)
    commentData = Comments(text=textData,author=authorIDData,content_object=objectData)
    commentData.save()
    notif = Notifications(user=commentData.content_object.author,comment=commentData,answer_comment=True)
    notif.save()
    mailNotify(notif)
    return HttpResponse("success")
  else:
    redirect('/question')

def ajaxRate(request):
  if request.is_ajax():
    dataJSON=simplejson.loads(request.raw_post_data)
    userData = User.objects.get(id=dataJSON["userID"])
    questionData = Question.objects.get(id=dataJSON["questionID"])
    rateData = dataJSON["rate"]
    if (Rates.objects.filter(user=userData,question=questionData).count()==0):
      rate = Rates(user=userData,question=questionData,rate=rateData)
      rate.save()
      return HttpResponse("success")
    else:
      return HttpResponse("error-already")
  else:
    redirect('/question')


def contacts(request):
  newDict = defaultDict
  newDict["curUser"]=request.user
  return render(
            request,
            "contacts.html",
            newDict
            )

def rules(request):
  newDict = defaultDict
  newDict["curUser"]=request.user
  return render(
            request,
            "rules.html",
            newDict
        )
