from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author','time_in', 'field_choice', 'header', 'content', 'rating']
    list_filter = ['author', 'time_in', 'field_choice', 'post_category']
    search_fields = ['header', 'content']
    raw_id_fields = ['author']
    date_hierarchy = 'time_in'
    ordering = ['author', 'time_in']

