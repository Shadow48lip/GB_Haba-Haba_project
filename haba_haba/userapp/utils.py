from mainapp.models import Post, Comment, AuthorLike, PostLike, CommentLike

class DataMixin:
    """Примиси для пользовательских разделов сайта"""
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        context['post_count'] = Post.objects.filter(author=self.request.user, is_published=True, is_blocked=False).count()
        context['comment_count'] = Comment.objects.filter(user=self.request.user, is_published=True).count()
        like_author = AuthorLike.objects.filter(author=self.request.user).count()
        like_posts = PostLike.objects.filter(post__author=self.request.user).count()
        like_comment = CommentLike.objects.filter(comment__user=self.request.user).count()
        context['like_receive_count'] = like_author + like_posts + like_comment

        return context
