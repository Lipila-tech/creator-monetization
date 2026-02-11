from django.urls import path
from apps.creators.views import CreatorPublicView, CreatorsListView, UpdateProfileView

app_name = 'creators'

urlpatterns = [
    path('all/', CreatorsListView.as_view(), name='creator_profiles_list'),
    path('<slug:slug>/', CreatorPublicView.as_view(), name='creator_public_view'),
    path('profile/me/', UpdateProfileView.as_view(), name='update_creator_profile'),
]