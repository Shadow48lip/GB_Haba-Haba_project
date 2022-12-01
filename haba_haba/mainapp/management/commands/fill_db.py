import json
import shutil
from random import randint, choice
from django.db.models import Count
from django.core.management.base import BaseCommand
from mainapp.models import Category, Tag, Post, AuthorLike, PostLike, Comment, CommentLike
from userapp.models import HabaUser

JSON_PATH = 'mainapp/fixtures'
PHOTOS_PATH = 'mainapp/fixtures/photos'
DST_PATH = './media/photos'


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Наполняем базу данных'

    # Перемещаем картинки к постам в папку media. Папки photos не должно быть
    def handle(self, *args, **options):
        try:
            shutil.copytree(PHOTOS_PATH, DST_PATH)
        except:
            print(f'Удалите папку "photos" в "media". Либо переместите содержимое {PHOTOS_PATH} "photos" в "media"')
            return

            # Загружаем категории. Перед загрузкой таблица очищается
        categories = load_from_json('mainapp/fixtures/category.json')
        Category.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = Category(**cat)
            new_category.save()

        # Загружаем тэги. Перед загрузкой таблица очищается
        tags = load_from_json('mainapp/fixtures/tag.json')
        Tag.objects.all().delete()
        for tag in tags:
            tag_fields = tag.get('fields')
            tag_fields['id'] = tag.get('pk')
            new_tag = Tag(**tag_fields)
            new_tag.save()

        # Загружаем пользователей. Перед загрузкой удаляем ID с 50 и выше
        users = load_from_json('mainapp/fixtures/user.json')
        HabaUser.objects.filter(pk__gt=49).delete()
        for user in users:
            user_fields = user.get('fields')
            user_fields['id'] = user.get('pk')
            new_user = HabaUser(**user_fields)
            new_user.save()

        # Загружаем статьи. Перед загрузкой таблица очищается
        posts = load_from_json('mainapp/fixtures/post.json')
        Post.objects.all().delete()
        for post in posts:
            new_post = Post()
            new_post.id = post['pk']
            new_post.title = post['title']
            new_post.content = post['content']
            new_post.author = HabaUser.objects.get(id=post['author'])
            new_post.cat = Category.objects.get(id=post['cat'])
            new_post.is_blocked = post['is_blocked']
            new_post.is_published = post['is_published']
            new_post.photo = post['photo']
            new_post.slug = post['slug']
            new_post.time_create = post['time_create']
            new_post.time_update = post['time_update']
            new_post.save()
            for tag in post['tags']:
                new_post.tags.add(Tag.objects.get(id=tag))
            new_post.save()

        # Ставим выборочно лайки к статьям. Перед загрузкой таблица очищается
        posts = Post.objects.all()
        users = HabaUser.objects.all()
        PostLike.objects.all().delete()
        for post in posts:
            get_like_count = randint(0, 12)
            for l in range(get_like_count):
                current_user = choice(users).pk
                pl = PostLike.objects.filter(user__id=current_user, post=post)
                if pl.count() == 0:
                    new_pl = PostLike()
                    new_pl.post = post
                    new_pl.user = HabaUser.objects.get(id=current_user)
                    new_pl.save()

        # Ставим выборочно лайки авторам. Перед загрузкой таблица очищается
        AuthorLike.objects.all().delete()
        users = HabaUser.objects.all()
        authors = Post.objects.values('author').annotate(total=Count('id'))  # группируем статьи по авторам
        for au in authors:
            get_count = randint(0, 8)
            for al in range(get_count):
                user = choice(users)
                if user == au['author']:  # самому себе лайки не ставим
                    continue
                get_user_like = AuthorLike.objects.filter(author__id=au['author'], user__id=user.id)
                # Один автор один может получить только один лайк от определенного пользователя
                if get_user_like.count() == 0:
                    new_al = AuthorLike()
                    new_al.user = HabaUser.objects.get(id=user.id)
                    new_al.author = HabaUser.objects.get(id=au['author'])
                    new_al.save()

        # Добавим комментарии. Немного, чтобы были
        comment_list = ['Отличная статья. Очень понравилась', 'Статья ничего так, но не хватает подробностей',
                        'Совершенно не понравилось. Ни очем статья',
                        'Автор молодец. Статья помогла разобраться в вопросе',
                        'Как гласит категорический императив Канта, тема не раскрыта',
                        'То, что автор хотел сказать в статье, написано 100500 раз',
                        'В статье подробно раскрыта тема разработки. Помогло', 'Да! Хорошо написано',
                        'Просто понравилось и все', 'Реклама казино']

        Comment.objects.all().delete()
        posts = Post.objects.all()
        users = HabaUser.objects.all()
        for post in posts:
            get_count = randint(0, 10)
            for al in range(get_count):
                user = choice(users)
                new_comment = Comment()
                new_comment.post = post
                new_comment.user = HabaUser.objects.get(id=user.id)
                new_comment.text = choice(comment_list)
                new_comment.is_published = True
                new_comment.save()


        # Ставим лайки к комментариям. Перед загрузкой таблица очищается
        comments = Comment.objects.all()
        users = HabaUser.objects.all()
        CommentLike.objects.all().delete()
        for comment in comments:
            get_like_count = randint(0, 5)
            for l in range(get_like_count):
                current_user = choice(users).pk
                cl = CommentLike.objects.filter(comment=comment, user__id=current_user)
                if cl.count() == 0:
                    new_cl = CommentLike()
                    new_cl.comment = comment
                    new_cl.user = HabaUser.objects.get(id=current_user)
                    new_cl.save()