from django.urls import path
from apps.creators.views import CreatorPublicView, CreatorsListView

app_name = 'creators'

urlpatterns = [
    path('all/', CreatorsListView.as_view(), name='creator_profiles_list'),
    path('<slug:slug>/', CreatorPublicView.as_view(), name='creator_public_view'),
]