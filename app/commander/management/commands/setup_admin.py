#!/usr/bin/env python

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Command(BaseCommand):
    """
    Creates superusers and changes their password.

    .. warning:: if the user already exists and is not superuser this command
                will promote the instance to superuser.

    Arguments:

        - ``-u`` ``--username``
        - ``-p`` ``--password``
        - ``-e`` ``--email``


    .. code-block:: bash

        manage.py setup_admin -u=admin -p=secretsecret -e=admin@test.com

    """

    help = _('Setup admin user')

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            '-u',
            type=str,
            help=_('Set the admin username'),
            dest='username',
            action='store',
            required=False,
            default=settings.ADMIN_USERNAME,
        )
        parser.add_argument(
            '--password',
            '-p',
            type=str,
            help=_('Set the admin password'),
            dest='password',
            action='store',
            required=True,
        )
        parser.add_argument(
            '--email',
            '-e',
            type=str,
            help=_('Set the admin e-mail'),
            dest='email',
            action='store',
            required=False,
            default='',
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # create admin user if needed
        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(username, email, password)

        else:
            admin = User.objects.get(username=username)
            # promote to staff
            admin.is_staff = True
            admin.is_superuser = True
            # update password
            admin.set_password(password)
            admin.save()
