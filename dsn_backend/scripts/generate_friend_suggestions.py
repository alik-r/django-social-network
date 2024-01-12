# -*- coding: utf-8 -*-

import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsn_backend.settings")
django.setup()

from account.models import User

users = User.objects.all()

for user in users:
    user.friend_suggestions.clear()
    for friend in user.friends.all():
        for friend_of_a_friend in friend.friends.all():
            if friend_of_a_friend not in user.friends.all() and friend_of_a_friend != user:
                user.friend_suggestions.add(friend_of_a_friend)