from django.urls import path
from .views import *

app_name = 'polls'

urlpatterns = [
    path('', addpoll, name='index'),
    path('<int:question_id>/vote/', vote, name='vote'),
    path('resultsdata/<str:obj>/', resultsData, name="resultsdata"),
    path('liked/', like_unlike_poll, name='like-poll-view'),
    path('voted/', vote_poll, name='vote-poll'),
    path('<pk>/delete/', PollDeleteView.as_view(), name='poll-delete'),
    path('<pk>/update/', PollUpdateView.as_view(), name='poll-update'),

]
