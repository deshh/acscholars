from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create default groups and assign them to admin users'

    def handle(self, *args, **kwargs):
        # Define the groups you want to create
        groups = ['operator', 'teacher']

        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Successfully created group: {group_name}')
            else:
                self.stdout.write(f'Group {group_name} already exists')

        # Assign all admin users to the 'operator' group
        admin_users = get_user_model().objects.filter(is_staff=True, is_superuser=True)
        operator_group = Group.objects.get(name='operator')
        for admin_user in admin_users:
            admin_user.groups.add(operator_group)
            self.stdout.write(f'Added {admin_user.username} to operator group')
