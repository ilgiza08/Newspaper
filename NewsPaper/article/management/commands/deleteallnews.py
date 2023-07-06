from django.core.management.base import BaseCommand
from article.models import Post


class Command(BaseCommand):
    help = 'Удаление всех новостей категории'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category')

    def handle(self, **kwargs):
        self.stdout.readable()
        self.stdout.write('Вы хотите удалить все новости? yes/no')
        answer = input()
        if answer == 'yes':
            Post.objects.filter(postCategory__categoryName=kwargs['category']).delete()
            self.stdout.write(self.style.SUCCESS('Новости удалены'))
            return
        self.stdout.write(self.style.ERROR('Отказано в доступе'))
