from django.db import models
from django.urls import reverse, reverse_lazy
# from django.utils.text import slugify
from pytils.translit import slugify

from userapp.models import HabaUser
import datetime


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Категория", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Тэг", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name', ]


class Post(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE,
                            verbose_name='Категория')
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    content = models.TextField(blank=True, verbose_name='Текст')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Презентационная картинка', blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирована')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', related_name='tags')

    def __str__(self):
        return self.title

    # Для формирования динамического url к записи. В шаблонах {{ p.get_absolute_url }}
    def get_absolute_url(self):
        return reverse('main:post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    @staticmethod
    def get_new_post():
        return Post.objects.filter(is_published=True, is_blocked=False).order_by('-time_create')[:5]

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-time_create', 'title']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name="Комментарий")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')

    def __str__(self):
        return f'{self.user} / {self.post}'

    @staticmethod
    def get_count(post):
        return Comment.objects.filter(post=post, is_published=True).count()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create', 'user']


class AuthorLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_author_set')
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='author_set')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.author}'

    @staticmethod
    def get_count(author):
        return AuthorLike.objects.filter(author=author).count()

    class Meta:
        verbose_name = 'Лайк автору'
        verbose_name_plural = 'Лайки автору'
        ordering = ['time_create']


class PostLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.post}'

    @staticmethod
    def get_count(post):
        return PostLike.objects.filter(post=post).count()

    @staticmethod
    def post_liked(post, user):
        obj = PostLike.objects.filter(post=post, user=user).first()
        if obj:
            return 'bi-heart-fill'
        else:
            return 'bi-heart'

    @staticmethod
    def set_like(post, user):
        obj = PostLike.objects.filter(post=post, user=user).first()
        if obj:
            obj.delete()
            return 0
        else:
            PostLike.objects.create(post=post, user=user)
            return 1

    class Meta:
        verbose_name = 'Лайк к статье'
        verbose_name_plural = 'Лайки к статье'
        ordering = ['time_create']


class CommentLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.comment}'

    @staticmethod
    def get_count(comment):
        return CommentLike.objects.filter(comment=comment).count()

    @staticmethod
    def comment_liked(comment, user):
        obj = CommentLike.objects.filter(comment=comment, user=user).first()
        if obj:
            return 'bi-heart-fill'
        else:
            return 'bi-heart'

    @staticmethod
    def set_like(comment, user):
        obj = CommentLike.objects.filter(comment=comment, user=user).first()
        if obj:
            obj.delete()
            return 0
        else:
            CommentLike.objects.create(comment=comment, user=user)
            return 1

    class Meta:
        verbose_name = 'Лайк к комментарию'
        verbose_name_plural = 'Лайки к комментарию'
        ordering = ['time_create']


class UserComplaints(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Заявитель',
                             related_name='user_complaint_set')
    bad_user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Виновный',
                                 related_name='bad_user_set')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    moderator = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Модератор',
                                  related_name='moderator_complaint_set')
    moderated_time = models.DateTimeField(default=datetime.date(2000, 1, 1), verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.bad_user} / {self.post}'

    class Meta:
        verbose_name = 'Жалоба пользователя'
        verbose_name_plural = 'Жалобы пользователя'
        ordering = ['time_create']


class BlockedUser(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_block_set')
    moderator = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Модератор',
                                  related_name='moderator_block_set')
    complaint = models.ForeignKey(UserComplaints, on_delete=models.CASCADE, verbose_name='Жалоба пользователя')
    lock_date = models.DateField(verbose_name='Заблокирован до')
    reason_for_blocking = models.CharField(max_length=255, verbose_name='Причина блокировки')

    def __str__(self):
        return f'{self.user} / {self.moderator} / {self.complaint}'

    class Meta:
        verbose_name = 'Заблокированный пользователь'
        verbose_name_plural = 'Заблокированные пользователи'
        ordering = ['lock_date']
