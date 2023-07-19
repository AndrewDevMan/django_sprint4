from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'category',
        'location',
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)
    list_per_page = 20


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    list_editable = (
        'description',
        'slug',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)
    list_per_page = 10


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 20


admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
