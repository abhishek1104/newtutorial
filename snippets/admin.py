from django.contrib import admin
from models import Snippets,SnippetsComments

# Register your models here.
#admin.site.register(Snippets)

class ChoiceInline(admin.TabularInline): #Better than using admin.StackedInline
    model=SnippetsComments
    extra=1 #Apart from existing comments to show!


class SnippetsAdmin(admin.ModelAdmin):
    list_display=('title','language','recently_created',) #By default, Django displays the str() of each object
    list_filter = ['created']
    search_fields = ['title','language']
    #fields=['code','lineos','title']

    fieldsets =[
    (None,{'fields':['title']}),
    ('Additional Info',{'fields':['code','lineos','language','style'],'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline] #here write the inline class without within inverted commas.


class SnippetsCommentsAdmin(admin.ModelAdmin):
    list_display=('comments',)
    search_fields = ['comments','snippet__title']
    fieldsets=[
    (None,{'fields':['snippet','comments']}),
    ('Additional Information',{'fields':['published'],'classes': ['collapse']}),
    ]


admin.site.register(SnippetsComments,SnippetsCommentsAdmin)
admin.site.register(Snippets,SnippetsAdmin)