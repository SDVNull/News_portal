from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from portal.models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def create_new_post(instance, **kwargs):
    if kwargs['action'] == 'post_add':

        subject = f'Новая публикация в категории {",".join(category.name for category in instance.category.all())}'

        emails = User.objects.filter(
            subscriptions__category__in=instance.category.all()
        ).values_list('email', flat=True)

        text_content = (
            f'Заголовок: {instance.header}\n'
            f'Текст: {instance.preview()}\n\n'
            f'Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Заголовок: {instance.header}\n'
            f'Текст: {instance.preview()}\n\n'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
