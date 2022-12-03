from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class HabaUser(AbstractUser):
    MALE = 'М'
    FEMALE = 'Ж'
    HIDDEN = 'НД'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (HIDDEN, 'НД')
    )

    email = models.EmailField(null=False, unique=True, db_index=True, verbose_name='Электронная почта')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    age = models.PositiveSmallIntegerField(default=0, null=False)
    lock_date = models.DateField(verbose_name='Заблокирован до', default=datetime.date(1970, 1, 1))
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    about = models.TextField(verbose_name="О себе", blank=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['creation_time', 'username']