from django.contrib import admin
from myblog.models import Blog, Category, Comment, Counts, Tag

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'show_tag', 'content', 'click_nums', 'create_time', 'modify_time')
    list_display_links = ('title',)
    list_filter = ('title', 'category')

    def show_tag(self, obj):
        return [i.name for i in obj.tag.all()]
    show_tag.short_description = '博客标签'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')
    list_display_links = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'create_time', 'blog')


@admin.register(Counts)
class CountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_nums', 'category_nums', 'tag_nums', 'visit_nums')
