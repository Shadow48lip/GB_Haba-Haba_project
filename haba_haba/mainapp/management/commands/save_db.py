import json
from os import path
from django.core.management.base import BaseCommand
from mainapp.models import Tag, Post

JSON_PATH = 'mainapp/fixtures'


def save_json(file_name, data):
    with open(path.join(JSON_PATH, file_name + '.json'), 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, sort_keys=True, default=str)


class Command(BaseCommand):
    help = 'Save Post, Tags'

    def handle(self, *args, **options):
        posts = Post.objects.all()
        data = []
        for post in posts:
            tags = []
            for tag in post.tags.all():
                tags.append(tag.id)
            data.append({'pk': post.id,
                         'cat': post.cat.id,
                         'author': post.author.id,
                         'title': post.title,
                         'slug': post.slug,
                         'content': post.content,
                         'photo': post.photo,
                         'time_create': post.time_create,
                         'time_update': post.time_update,
                         'is_published': post.is_published,
                         'is_blocked': post.is_blocked,
                         'tags': tags
                         })

        save_json('post', data)
