import time
from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=1000)
    singer = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    # date = models.DateTimeField('date published')

    # def was_published_recently(self):
    #     return self.pub_date >= time.now() - datetime.timedelta(days=1)

    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    # was_published_recently.short_description = 'Published recently?'

