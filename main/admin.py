from django.contrib import admin
from .models import Question, KakaoUser, Selection, Constitution

# Register your models here.
admin.site.register(Question)
admin.site.register(Selection)
admin.site.register(KakaoUser)
admin.site.register(Constitution)