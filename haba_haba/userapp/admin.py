from django.contrib import admin
from .models import HabaUser


class HabaUserAdmin(admin.ModelAdmin):
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
    prepopulated_fields = {
        'slug': ('username',)
    }


admin.site.register(HabaUser, HabaUserAdmin)
