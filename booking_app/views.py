from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking
from .forms import BookingForm
from core.models import Space

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_app/booking_form.html'

    def get_initial(self):
        space = get_object_or_404(Space, id=self.kwargs['space_id'])
        return {
            'space': space,
            'start_time': timezone.now() + timezone.timedelta(hours=1),
            'end_time': timezone.now() + timezone.timedelta(hours=2),
        }

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        form.instance.space = get_object_or_404(Space, id=self.kwargs['space_id'])
        response = super().form_valid(form)
        messages.success(self.request, "Бронювання успішно створено! Очікуйте підтвердження.")
        return response

    def get_success_url(self):
        return reverse_lazy('booking:detail', kwargs={'pk': self.object.pk})

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_app/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user.profile).order_by('-start_time')

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking_app/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.profile)

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_app/booking_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user.profile,
            status__in=['pending', 'confirmed']
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Бронювання успішно оновлено!")
        return response

    def get_success_url(self):
        return reverse_lazy('booking:detail', kwargs={'pk': self.object.pk})

class BookingCancelView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = []
    template_name = 'booking_app/booking_confirm_cancel.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user.profile,
            status__in=['pending', 'confirmed']
        )

    def form_valid(self, form):
        form.instance.status = 'cancelled'
        response = super().form_valid(form)
        messages.success(self.request, "Бронювання скасовано!")
        return response

    def get_success_url(self):
        return reverse_lazy('booking:list')

def check_availability(request):
    space_id = request.GET.get('space_id')
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    try:
        space = Space.objects.get(id=space_id)
        is_available = not Booking.objects.filter(
            space=space,
            start_time__lt=end,
            end_time__gt=start,
            status__in=['confirmed', 'pending']
        ).exists()
        
        return JsonResponse({'available': is_available})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)