from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.apps import AppConfig


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='basic')
        instance.groups.add(default_group)

# def create_groups(sender, **kwargs):
#     # List of groups to create
#     groups = ['operator', 'teacher']

#     for group_name in groups:
#         group, created = Group.objects.get_or_create(name=group_name)
#         if created:
#             print(f'Created group: {group_name}')
    
#     # Assign all admin users to the 'operator' group
#     admin_users = User.objects.filter(is_staff=True, is_superuser=True)
#     operator_group = Group.objects.get(name='operator')
#     for admin_user in admin_users:
#         admin_user.groups.add(operator_group)
#         print(f'Added {admin_user.username} to operator group')

# class CustomAccountsConfig(AppConfig):
#     name = 'customaccounts'

#     def ready(self):
#         post_migrate.connect(create_groups, sender=self)