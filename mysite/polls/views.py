from django.shortcuts import render

# Create your views here.
from typing import Any
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import FormMixin
from .forms import VoterForm


from .models import Question, Choice,Voter

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.all()
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     context = {
#         "latest_question_list":latest_question_list,
#         "dummy":"some dummy value"
#         }
#     return render(request,"polls/index.html",context)
class IndexView(generic.ListView):

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.all()
    

# def detail(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     choices = Choices.objects.filter(question=question) # get all choices for this question
    
#     context = {
#         "question":question,
#         "choices":choices
#     }
#     # return HttpResponse(" You are looking at questions number %s"%question_id)
#     return render(request, "polls/detail.html",context)

class DetailView(FormMixin,generic.DetailView):
    template_name = "polls/detail.html"
    model=Question
    form_class = VoterForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['choices'] = self.object.choice_set.all().order_by('id')
        context['form'] = self.get_form()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     question_id = self.kwargs.get('question_id')
    #     question = get_object_or_404(Question, pk=question_id)
    #     context['question'] = question
    #     context['choices'] = Choices.objects.filter(question=question).order_by('id')
    #     return context

def results(request, question_id):
    print("In results view")
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    print("Choices",choices)
    context = {
        "question":question,
        "choices":choices
    }
    return render(request, "polls/results.html",context)

class ResultsView(generic.TemplateView):
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        context['question'] = question
        context['choices'] = Choice.objects.filter(question=question).order_by('id')
        return context

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = VoterForm(request.POST)
    # selected_choice = Choice.objects.get(pk=request.POST["choice"])
    # selected_choice.votes = F('votes') + 1
    # selected_choice.save()
    # return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with error message
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "form": form,
                "error_message": "You didn't select a choice.",
            },
        )
    
    if form.is_valid():
        # Save the voter information
        voter = form.save(commit=False)
        voter.choice = selected_choice
        voter.save()
        
        # Update the vote count
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    else:
        # If the form is invalid, redisplay the form with errors
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "form": form,
                "error_message": "Please correct the errors below.",
            },
        )

def dummyvote(request):
    return HttpResponse("This is dummy text - from vignes")

class VoterChoiceView(generic.ListView):
    model = Voter
    template_name = 'polls/voter.html'
    context_object_name = 'voter_list'