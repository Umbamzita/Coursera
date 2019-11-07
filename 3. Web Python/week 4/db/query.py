from datetime import datetime
 
from django.db.models import Avg, Q, Count
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    u1 = User.objects.create(first_name = 'u1', last_name = 'u1')
    u1.save()
    u2 = User.objects.create(first_name = 'u2', last_name = 'u2')
    u2.save()
    u3 = User.objects.create(first_name = 'u3', last_name = 'u3')
    u3.save()
    blog1 = Blog.objects.create(title = 'blog1', author = u1)
    blog1.save()
    blog2 = Blog.objects.create(title = 'blog2', author = u1)
    blog2.save() 
    blog1.subscribers.add(u1,u2)
    blog2.subscribers.add(u2)
    
    t1 = Topic.objects.create(title = 'topic1', blog = blog1, author = u1)
    t1.save()
    t2 = Topic.objects.create(title = 'topic2_content', blog = blog1, author = u3, created = '2017-01-01')
    t2.save()
    t1.likes.add(u1,u2,u3)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(first_name__in=['u1', 'u2']).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    u=User.objects.get(first_name='u2')
    u.subscriptions.clear()


def get_topic_created_grated():
    return Topic.objects.filter(created__gte='2018-01-01')


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.order_by('-id')[:2]


def get_topic_count():
    return Blog.objects.all().annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(count=Count('topic')).aggregate(avg=Avg('count'))

    

def get_blog_that_have_more_than_one_topic():
    return Blog.objects.all().annotate(topics=Count('topic')).filter(topics__gt='1')


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__isnull=True).order_by('pk')


def get_topic_that_like_all_users():
    return Topic.objects.filter(likes=User.objects.all())


def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__isnull=True)
