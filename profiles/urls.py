from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('', ProfileListView.as_view(), name='all-profile-view'),
    path('invite-profiles/', invite_profiles_list_view, name='invite-list'),
    path('send-invitation/', send_invitation, name='send-invitation'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('my-invites/accept/', accept_invitation, name='accept-invitation'),
    path('my-invites/reject/', reject_invitation, name='reject-invitation'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),

]
