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
        ordering = ('name',)


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
        ordering = ('name',)


class Post(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    content = models.TextField(blank=True, verbose_name='Текст')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Презентационная картинка', blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, db_index=True, verbose_name='Публикация')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирована')
    # related_name указывает обратный вызов из таблицы Tags. tag.posts.all
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', related_name='posts')
    total_views = models.IntegerField(default=0, verbose_name='Просмотры')
    is_deleted = models.BooleanField(verbose_name='удален', db_index=True, default=False)

    def __str__(self):
        return self.title

    # Для формирования динамического url к записи. В шаблонах {{ p.get_absolute_url }}
    def get_absolute_url(self):
        return reverse('main:post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    # переопределяем метод, удаляющий пост (скрываем)
    def delete(self):
        self.is_deleted = True
        self.is_published = False
        self.save()

    @staticmethod
    def get_new_post():
        return Post.objects.select_related(
            'author', 'cat'
        ).filter(is_published=True, is_blocked=False)[:5]  # .order_by('-time_create')

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ('-time_create', 'title')


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
        return Comment.objects.select_related(
            'user', 'post'
        ).filter(post=post, is_published=True).count()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('time_create', 'user')


class AuthorLike(models.Model):
    user = models.ForeignKey(
        HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_author_set'
    )
    author = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Автор', related_name='author_set')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.author}'

    @staticmethod
    def get_count(author):
        return AuthorLike.objects.select_related(
            'user', 'author'
        ).filter(author=author).count()

    class Meta:
        verbose_name = 'Лайк автору'
        verbose_name_plural = 'Лайки автору'
        ordering = ('time_create',)


class PostLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.post}'

    @staticmethod
    def get_count(post):
        return PostLike.objects.select_related(
            'post', 'user'
        ).filter(post=post).count()

    @staticmethod
    def post_liked(post, user):
        obj = PostLike.objects.select_related(
            'post', 'user'
        ).filter(post=post, user=user).first()

        if obj:
            return 'bi-heart-fill'
        else:
            return 'bi-heart'

    @staticmethod
    def set_like(post, user):
        obj = PostLike.objects.select_related(
            'post', 'user'
        ).filter(post=post, user=user).first()

        if obj:
            obj.delete()
            return 0
        else:
            PostLike.objects.create(post=post, user=user)
            return 1

    class Meta:
        verbose_name = 'Лайк к статье'
        verbose_name_plural = 'Лайки к статье'
        ordering = ('time_create',)


class CommentLike(models.Model):
    user = models.ForeignKey(HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.user} / {self.comment}'

    @staticmethod
    def get_count(comment):
        return CommentLike.objects.select_related(
            'comment', 'user'
        ).filter(comment=comment).count()

    @staticmethod
    def comment_liked(comment, user):
        obj = CommentLike.objects.filter(comment=comment, user=user).first()

        if obj:
            return 'bi-heart-fill'
        else:
            return 'bi-heart'

    @staticmethod
    def set_like(comment, user):
        obj = CommentLike.objects.select_related(
            'comment', 'user'
        ).filter(comment=comment, user=user).first()

        if obj:
            obj.delete()
            return 0
        else:
            CommentLike.objects.create(comment=comment, user=user)
            return 1

    class Meta:
        verbose_name = 'Лайк к комментарию'
        verbose_name_plural = 'Лайки к комментарию'
        ordering = ('time_create',)


class UserComplaints(models.Model):
    user = models.ForeignKey(
        HabaUser, on_delete=models.CASCADE, verbose_name='Заявитель', related_name='user_complaint_set'
    )
    bad_user = models.ForeignKey(
        HabaUser, on_delete=models.CASCADE, verbose_name='Виновный', related_name='bad_user_set'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    moderator = models.ForeignKey(
        HabaUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Модератор',
        related_name='moderator_complaint_set'
    )
    time_moderated = models.DateTimeField(null=True, blank=True, verbose_name='Отмодерировано')

    def __str__(self):
        return f'{self.user} / {self.bad_user} / {self.post}'

    @staticmethod
    def set_сomplaint(post, user, comment):

        if comment is None:  # Жалоба на статью
            obj = UserComplaints.objects.select_related(
                'post', 'user'
            ).filter(post=post, user=user, comment=comment).first()

            if obj:
                if obj.user == user:
                    if obj.moderator is None:
                        obj.delete()
                        return 0
                else:
                    UserComplaints.objects.create(user=user, bad_user=post.author, post=post)
                    return 1
            else:
                UserComplaints.objects.create(user=user, bad_user=post.author, post=post)
                return 1

        else:
            obj = UserComplaints.objects.select_related(
                'post', 'user', 'comment'
            ).filter(post=post, user=user, comment=comment).first()

            if obj:
                if obj.moderator is None:
                    obj.delete()
                    return 0
            else:
                UserComplaints.objects.create(user=user, bad_user=comment.user, post=post, comment=comment)
                return 1

    @staticmethod
    def get_сomplaint(post, user, comment):
        obj = UserComplaints.objects.select_related(
            'post', 'user', 'comment'
        ).filter(post=post, user=user, comment=comment).first()

        if obj:
            return 'bi bi-exclamation-circle-fill'
        else:
            return 'bi bi-exclamation-circle'

    @staticmethod
    def get_post_сomplaint(post, user):
        obj = UserComplaints.objects.select_related(
            'post', 'user'
        ).filter(post=post, user=user, comment=None).first()

        if obj:
            return 'bi bi-exclamation-circle-fill'
        else:
            return 'bi bi-exclamation-circle'

    @staticmethod
    def get_new_complaints():
        return UserComplaints.objects.select_related(
            'post', 'user', 'comment'
        ).filter(moderator=None).count()

    class Meta:
        verbose_name = 'Жалоба пользователя'
        verbose_name_plural = 'Жалобы пользователя'
        ordering = ('time_create',)


class BlockedUser(models.Model):
    user = models.ForeignKey(
        HabaUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_block_set'
    )
    moderator = models.ForeignKey(
        HabaUser, on_delete=models.CASCADE, verbose_name='Модератор', related_name='moderator_block_set'
    )
    complaint = models.ForeignKey(UserComplaints, on_delete=models.CASCADE, verbose_name='Жалоба пользователя')
    lock_date = models.DateField(null=True, blank=True, verbose_name='Заблокирован до')
    reason_for_blocking = models.CharField(max_length=255, verbose_name='Причина блокировки')

    def __str__(self):
        return f'{self.user} / {self.moderator} / {self.complaint}'

    class Meta:
        verbose_name = 'Заблокированный пользователь'
        verbose_name_plural = 'Заблокированные пользователи'
        ordering = ('lock_date',)
