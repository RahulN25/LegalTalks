from django.contrib import admin
from .models import Question, Answer

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'question_slug': ('question_title',)}
admin.site.register(Question)
admin.site.register(Answer)
