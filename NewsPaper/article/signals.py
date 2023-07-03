from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post

@receiver(m2m_changed, sender = Post.postCategory.through)
def notify_add_news(sender, instance, action, **kwargs):
    subject = f'{instance.title}',

    subscribers_list = []
    post_categories = instance.postCategory.all()
    for catigory in post_categories:
        for email in catigory.subscribers.all():
            subscribers_list.append(email.email)
        print(subscribers_list)

    send_mail( 
            subject=subject,
            message=f'Здравствуй. Новая статья в твоём любимом разделе! {instance.url}', 
            from_email='il.ilgiza@yandex.ru', 
            recipient_list= subscribers_list,
        )