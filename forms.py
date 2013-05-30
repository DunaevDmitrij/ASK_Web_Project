from django import forms

class LoginForm (forms.Form):
  name = forms.CharField(max_length = 32)
  password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm (forms.Form):
  username = forms.CharField(max_length = 32)
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)

class NewQuestionForm (forms.Form):
  header = forms.CharField(max_length = 64)
  content = forms.CharField(max_length = 1024,widget=forms.Textarea)
  tag1 = forms.CharField(required=False)
  tag2 = forms.CharField(required=False)
  tag3 = forms.CharField(required=False)

class NewAnswerForm (forms.Form):
  content = forms.CharField(widget=forms.Textarea)

class SearchForm (forms.Form):
  question = forms.CharField(max_length = 64)

class NewCommentForm (forms.Form):
  text = forms.CharField(widget=forms.Textarea)

class ActivationForm (forms.Form):
  token = forms.CharField(max_length = 64, min_length = 64)
