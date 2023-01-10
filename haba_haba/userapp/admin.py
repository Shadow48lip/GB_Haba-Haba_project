from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import HabaUser


class HabaUserAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    save_on_top = True
    save_as = True
    fields = (
        'username',
        'slug',
        'email',
        'first_name',
        'last_name',
        'gender',
        'age',
        'about',
        'groups',
        'user_permissions',
        'is_active',
        'date_joined',
        'is_blocked',
        'lock_date',
        'is_staff',
    )

    readonly_fields = (
        'slug',
        'date_joined',
        'is_blocked',
        'lock_date',
    )

    summernote_fields = ('about',)

    list_display = (
        'id',
        'username',
        'slug',
        'email',
        'creation_time',
        'is_active',
        'is_blocked',
        'is_staff',
    )

    list_display_links = (
        'id',
        'username',
    )

    search_fields = (
        'username',
    )
    list_editable = (
        'is_active',
        'is_blocked',
    )
    list_filter = (
        'is_active',
        'is_blocked',
        'creation_time',
    )
    # prepopulated_fields = {
    #     'slug': ('username',)
    # }


admin.site.register(HabaUser, HabaUserAdmin)
