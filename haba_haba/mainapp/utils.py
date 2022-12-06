class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        # Здесь можно прописать дополнительную логику

        return context
