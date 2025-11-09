from django.contrib import admin
# Register your models here.
from .models import Question,Choice,Dummy,Voter

admin.site.site_header = " My Polls Administration"
admin.site.site_title = "Polls Admin"
admin.site.index_title = "Welcome to the Polls Admin"

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "pub_date","was_published_recently")
    inlines = [ChoiceInline] #adding inline choices to question admin view
    search_fields = ["question_text"]

    
# admin.site.register(Choice)
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "choice_text", "votes")


admin.site.register(Dummy)
admin.site.register(Voter)

