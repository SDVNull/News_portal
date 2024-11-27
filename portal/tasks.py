from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from config import settings
from portal.models import Post, Subscription


@shared_task
def send_emails(id):
    new_post = Post.objects.get(id=id)
    subject = f'Новая публикация в категории {",".join(category.name for category in new_post.category.all())}'

    emails = User.objects.filter(
        subscriptions__category__in=new_post.category.all()
    ).values_list('email', flat=True)

    text_content = (
        f'Заголовок: {new_post.header}\n'
        f'Текст: {new_post.preview()}\n\n'
        f'Ссылка: http://127.0.0.1:8000{new_post.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок: {new_post.header}\n'
        f'Текст: {new_post.preview()}\n\n'
        f'<a href="http://127.0.0.1:8000{new_post.get_absolute_url()}">'
        f'Ссылка</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_emails_weekly():
    posts = Post.objects.filter(time_in__gte=(timezone.now() - timedelta(days=7)))

    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string('weekly_post.html',
                                    {'link': settings.SITE_URL,
                                     'posts': posts})
    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
