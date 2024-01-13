# -*- coding: utf-8 -*-

import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsn_backend.settings")
django.setup()

from post.models import Post, Trend

def extract_trends(body):
    trends = []
    for word in body.split():
        if word.startswith('#'):
            trends.append(word[1:])
    return trends

for trend in Trend.objects.all():
    trend.delete()

period = timezone.now() - timedelta(days=7)
trends = []
for post in Post.objects.filter(created_at__gte=period).filter(is_private=False):
    trends.extend(extract_trends(post.body))

for trend in Counter(trends).most_common(10):
    Trend.objects.create(title=trend[0], count=trend[1])