from django.urls import path, re_path
from django.views.static import serve

# from blog.settings import MEDIA_ROOT, STATIC_ROOT

from .feeds import BlogRssFeed
from .views import IndexView, ArchiveView, TagDetailView, TagView, BlogDetailView,\
    AddCommentView, CategoryDetaiView, MySearchView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/<int:blog_id>/', BlogDetailView.as_view(), name='blog_id'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('tags/', TagView.as_view(), name='tags'),
    re_path(r'^tags/(?P<tag_name>\w+)$', TagDetailView.as_view(), name='tag_name'),
    re_path(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    path(r'search/', MySearchView(),  name='haystack_search'),
    path('rss/', BlogRssFeed(), name='rss'),
    re_path(r'^category/(?P<category_name>\w+)/$', CategoryDetaiView.as_view(), name='category_name'),
    # 添加静态文件的访问处理函数
    # re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # # 静态文件处理
    # re_path(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),
]

# 配置全局404页面
hander404 = 'myblog.views.page_not_found'

# 配置全局505页面
hander505 = 'myblog.views.page_errors'
