from django.contrib import admin
from django.db.models.functions import Substr

from .models import Post, Author, Category, Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'time_in', 'field_choice', 'header', 'content', 'rating']
    list_filter = ['author', 'time_in', 'field_choice', 'category']
    search_fields = ['header', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'time_in'
    ordering = ['author', 'time_in']

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Subscription)


