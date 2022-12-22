# from django import template
#
# from mainapp.models import Post
#
# register = template.Library()
#
#
# @register.inclusion_tag('mainapp/includes/_news.html', name='news')
# def show_main_categories():
#     news = Post.get_new_post()
#     return {'news': news}