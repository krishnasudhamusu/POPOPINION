from django.urls import path
from .views import *

app_name = 'confessions'

urlpatterns = [
    path('', confession_comment_create_list_view, name='main-confession-view'),
    path('liked/', like_unlike_confession, name='like-confession-view'),
    path('<pk>/delete/', ConfessionDeleteView.as_view(), name='confession-delete'),
    path('<pk>/update/', ConfessionUpdateView.as_view(), name='confession-update'),
]
