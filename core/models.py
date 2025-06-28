from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Space(models.Model):
    SPACE_TYPES = (
        ('room', 'Кімната'),
        ('desk', 'Робоче місце'),
        ('hall', 'Конференц-зал'),
    )
    name = models.CharField("Назва", max_length=100)
    slug = models.SlugField("URL-адреса", unique=True)
    description = models.TextField("Опис")
    type = models.CharField("Тип", max_length=20, choices=SPACE_TYPES)
    capacity = models.PositiveIntegerField("Вмістимість")
    is_active = models.BooleanField("Доступний", default=True)
    image = models.ImageField("Зображення", upload_to='spaces/', blank=True, null=True)

    class Meta:
        verbose_name = "Простір"
        verbose_name_plural = "Простори"
        ordering = ['name']

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField("Телефон", max_length=20, blank=True)
    notifications_enabled = models.BooleanField("Сповіщення", default=True)
    is_manager = models.BooleanField("Менеджер", default=False)

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return self.user.username

# Сигнали для автоматичного створення профілю
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()