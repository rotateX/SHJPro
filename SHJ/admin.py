from django.contrib import admin
from SHJ.models import Content, Category, Tag, Comment
# Register your models here.


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_age', 'pub_time', 'views', 'comment_num')
    list_per_page = 5
    search_fields = ['title']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'content', 'email', 'update_time')


admin.site.register(Content, ContentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)


