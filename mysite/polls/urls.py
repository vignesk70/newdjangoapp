from django.urls import path

from . import views
app_name ="polls"
urlpatterns =[
    # path("",views.index,name="index"),
    path("",views.IndexView.as_view(),name="index"),
    path("<int:pk>/",views.DetailView.as_view(),name="detail"),
    # path("<int:pk>/",views.DetailView.as_view(),name="detail"),
    path("<int:question_id>/results/",views.ResultsView.as_view(),name="results"),
    path("<int:question_id>/vote/",views.vote,name="vote"),
    path("vote/",views.dummyvote,name="dummy"),
    path("dummyvote/",views.dummyvote,name="dummyvote"),
    path('voter/',views.VoterChoiceView.as_view(), name='voter'),
]