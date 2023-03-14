from django.contrib.syndication.views import Feed
from django.urls import reverse
from myblog.models import Blog


class BlogRssFeed(Feed):
    """
    Create a rss source.
    """
    title = 'rainstone的博客小屋'
    link = '/rss/'

    def items(self):
        return Blog.objects.all()

    def item_title(self, item):
        return item.title

    def item_content(self, item):
        return item.content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blog_id', args=[item.id])
