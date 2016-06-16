from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0],item[0]) for item in LEXERS])
STYLE_CHOICES =  sorted([(item,item) for item in get_all_styles()])


class Snippets(models.Model):
    created =  models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True,default='')
    code = models.TextField()
    lineos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,default='python',max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly',max_length=100)


    def recently_created(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    recently_created.admin_order_field='created'
    recently_created.boolean=True
    recently_created.short_description = 'Created Recently?'


    class Meta:
        ordering = ('-created',)

    def __str__ (self):
        return self.code




class SnippetsComments(models.Model):
    snippet = models.ForeignKey(Snippets,related_name='comments') # 'app_name.model_class_name'
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField()


    class Meta:
        db_table = 'comment'


    def __str__(self):
        return self.comments



