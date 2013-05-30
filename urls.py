from django.conf.urls.defaults import *
import ask.views

urlpatterns = patterns('',
  url(r'^$',ask.views.index),
  url(r'^question$',ask.views.question),
    url(r'^question/(\d+)/$',ask.views.questionID),
  url(r'^login/$',ask.views.loginator),
  url(r'^user/$',ask.views.user),
    url(r'^user/(\w+)/$',ask.views.userpage),
  url(r'^registration/$',ask.views.registration),
  url(r'^newquestion/$',ask.views.newquestion),
  url(r'^activate/$',ask.views.activate),
  url(r'^search$',ask.views.search),
  url(r'^contacts/$',ask.views.contacts),
  url(r'^rules/$',ask.views.rules),

  url(r'^logout/$',ask.views.deloginator),
  url(r'^answer/$',ask.views.answer),

  url(r'ajax/indexSend$',ask.views.ajaxIndexSend),
  url(r'ajax/indexAnswer$',ask.views.ajaxIndexAnswer),
  url(r'ajax/comment$',ask.views.ajaxComment),
  url(r'ajax/rate$',ask.views.ajaxRate),
  url(r'ajax/answer$',ask.views.ajaxAnswer),
  url(r'ajax/solver$',ask.views.ajaxSolver),

  url(r'ajax/tests$',ask.views.ajaxTests),
)
