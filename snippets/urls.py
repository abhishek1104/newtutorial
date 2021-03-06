from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^snippets/$', views.snippets_list , name='snippets_list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippets_Details, name='snippets_Details'),
    url(r'^snippets/details/$',views.snippets_detaillist, name='snippets_detaillist'),
    url(r'^snippets/detailswithcomments/$',views.SnipCmnts, name='SnipCmnts'),
    url(r'^snippets/selectdetail/$' , views.snippet_selectdetail , name='snippet_selectdetail'),
    url(r'^snippets/comment/(?P<comment_id>[0-9]+)/$' ,views.new_comment_detail, name='new_comment_detail'),
]