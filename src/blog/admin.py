from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Tag)
# admin.site.register(models.Post)


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date_posted", "status")
    list_filter = ("status", "author")
    search_fields = ("title", "content")
    date_hierarchy = "date_posted"
    inlines = [CommentInline]
