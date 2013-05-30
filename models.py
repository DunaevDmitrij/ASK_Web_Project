from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class User (User):
	regDate = models.DateField(auto_now_add=True)
	photo = models.ImageField(upload_to='/users_photos/',blank=True, null=True)
	bookmarks = models.ManyToManyField('Question',blank=True, null=True)

class UserTokens (models.Model):
  token = models.CharField(max_length=64)
  user = models.ForeignKey('User')

class Question (models.Model):
  header = models.CharField(max_length=64)
  content = models.CharField(max_length=1024)
  author = models.ForeignKey('User')
  createDate = models.DateField(auto_now_add=True)
  counter = models.IntegerField(default=0)
  solved = models.BooleanField(default=False)
  tag = models.ManyToManyField('Tag')
  files = models.FileField(upload_to='/question_files/',blank=True, null=True)#--
  comment = generic.GenericRelation('Comments')
  def __unicode__(self):
    return self.header

class Rates (models.Model):
  user = models.ForeignKey('User')
  question = models.ForeignKey('Question')
  rate = models.BooleanField() # 1 -> + ; 0 -> -

class Answer (models.Model):
	content = models.CharField(max_length=512)
	question = models.ForeignKey('Question')
	author = models.ForeignKey('User')
	rightFlag = models.BooleanField(default=False)
	createDate = models.DateField(auto_now_add=True)
	comment = generic.GenericRelation('Comments')
	def __unicode__(self):
		return self.content

class Comments (models.Model): 
	text = models.CharField(max_length=512)	
	author = models.ForeignKey('User')
	createDate = models.DateField(auto_now_add=True)
	content_type = models.ForeignKey(ContentType, limit_choices_to = {"model__in": ("Question", "Answer")})
	object_id = models.IntegerField()
	content_object = generic.GenericForeignKey('content_type','object_id')
	def __unicode__(self):
		return self.text

class Tag (models.Model):
	name = models.CharField(max_length=64)
	def __unicode__(self):
		return self.name

class Notifications (models.Model):
  user = models.ForeignKey('User')
  answer = models.ForeignKey('Answer', null=True)
  comment = models.ForeignKey('Comments', null=True)
  answer_comment = models.BooleanField() #0 -> answer, 1 -> comment
  createDate = models.DateField(auto_now_add=True)
