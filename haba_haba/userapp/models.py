from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

from django.urls import reverse
from django.utils.text import slugify


class HabaUser(AbstractUser):
    MALE = 'М'
    FEMALE = 'Ж'
    HIDDEN = 'НД'

    GENDER_CHOICES = (
        (HIDDEN, 'Не выбран'),
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    email = models.EmailField(null=False, unique=True, db_index=True, verbose_name='Электронная почта')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    age = models.PositiveSmallIntegerField(default=0, null=False, verbose_name='Возраст')
    lock_date = models.DateField(verbose_name='Заблокирован до', default=datetime.date(1970, 1, 1))
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    about = models.TextField(verbose_name="О себе", blank=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, default=HIDDEN, max_length=10)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user:user_profile', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['creation_time', 'username']