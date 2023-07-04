from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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


        