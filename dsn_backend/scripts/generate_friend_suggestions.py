# -*- coding: utf-8 -*-

import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsn_backend.settings")
django.setup()

from account.models import User
from django.db.models import Q

users = User.objects.all()

for user in users:
    user.friend_suggestions.clear()
    user_friends = user.friends.all()
    friend_of_friend_qs = User.objects.filter(friends__in=user_friends).exclude(id=user.id).exclude(friends=user)
    user.friend_suggestions.add(*friend_of_friend_qs)
