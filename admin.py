from django.contrib import admin
from ask.models import User,Question,Answer,Comments,Tag,UserTokens,Rates

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comments)
admin.site.register(Tag)
admin.site.register(UserTokens)
admin.site.register(Rates)
