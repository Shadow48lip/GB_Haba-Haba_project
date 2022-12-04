from django.contrib import admin
from .models import Category, Tag, Post, PostLike, CommentLike, AuthorLike, \
    BlockedUser, UserComplaints, Comment
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

    prepopulated_fields = {'slug': ('title',)}
    # Подключаем виджет к админке
    summernote_fields = ('content',)


class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('id', 'post', 'user', 'time_create', 'time_update')
    list_display_links = ('id', 'post', 'user')
    list_filter = ('is_published', 'time_create')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(AuthorLike)
admin.site.register(BlockedUser)
admin.site.register(UserComplaints)
