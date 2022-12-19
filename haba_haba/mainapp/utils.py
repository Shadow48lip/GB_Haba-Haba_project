from mainapp.models import Post


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        context['news'] = Post.get_new_post()

        return context
