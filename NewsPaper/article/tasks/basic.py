from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from article.models import User
import datetime

def notify_add_news(instance):
    subject = f'{instance.title}',
    subscribers_list = []
    post_categories = instance.postCategory.all()
    for category in post_categories:
        for email in category.subscribers.all():
            subscribers_list.append(email.email)     
        
        html = render_to_string(
            template_name = 'mail/new_post.html',
            context={
                'category': category,
                'post': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body = '',
            from_email='il.ilgiza@yandex.ru', 
            to=[subscribers_list,],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()


def get_new_post_list(subscriptions):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    new_post_list = []
    for sub in subscriptions:
           new_posts = sub.post_set.filter(time__range=(start_date, end_date))
           new_post_list.append(new_posts)
    return new_post_list


def notify_weekly():
    users=User.objects.all()
    for user in users:
        subscriptions = user.category_set.all()
        new_post_list = get_new_post_list(subscriptions)
        
        print(f'NEW POST LIST {new_post_list}')
        
        html = render_to_string(
            template_name = 'mail/weekly_mailing.html',
            context={
                'posts': new_post_list,
            },
        )

        msg = EmailMultiAlternatives(
            subject='Новые статьи в любимых категориях',
            body = '',
            from_email='il.ilgiza@yandex.ru', 
            to=[user.email,],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        

        