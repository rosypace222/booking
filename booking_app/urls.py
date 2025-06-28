from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('create/<int:space_id>/', views.BookingCreateView.as_view(), name='create'),
    path('list/', views.BookingListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.BookingUpdateView.as_view(), name='update'),
    path('cancel/<int:pk>/', views.BookingCancelView.as_view(), name='cancel'),
    path('availability/', views.check_availability, name='availability'),
]