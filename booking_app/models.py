from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import Space, UserProfile

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    )
    
    user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Користувач"
    )
    space = models.ForeignKey(
        Space, 
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Простір"
    )
    start_time = models.DateTimeField("Початок бронювання")
    end_time = models.DateTimeField("Кінець бронювання")
    status = models.CharField(
        "Статус", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)
    participants = models.PositiveIntegerField("Кількість учасників", default=1)
    notes = models.TextField("Додаткові нотатки", blank=True)

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"
        ordering = ['-start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name="check_start_time_before_end_time"
            )
        ]

    def __str__(self):
        return f"{self.space.name} - {self.user.user.username} ({self.start_time:%d.%m.%Y %H:%M})"
    
    def clean(self):
        # Перевірка часу
        if self.start_time >= self.end_time:
            raise ValidationError("Час завершення має бути після часу початку")
        
        # Перевірка місткості
        if self.participants > self.space.capacity:
            raise ValidationError(f"Максимальна місткість: {self.space.capacity}")
        
        # Забороняємо бронювання в минулому
        if self.start_time < timezone.now():
            raise ValidationError("Не можна бронювати в минулому часі")
        
        # Перевірка доступності (крім скасованих та завершених)
        overlapping = Booking.objects.filter(
            space=self.space,
            status__in=['pending', 'confirmed'],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if overlapping.exists():
            raise ValidationError("Обраний період вже зайнятий")

    def save(self, *args, **kwargs):
        self.full_clean()  # Виклик повної валідації
        super().save(*args, **kwargs)