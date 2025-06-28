from django.urls import path
from .import views
app_name = 'core'

urlpatterns = [
    path('spaces/', views.SpaceListView.as_view(),name="space_list"),
    path('spaces/<slug:slug>', views.SpaceListView.as_view(), name="space_detail" )
    
]
