from django.shortcuts import render,HttpResponse,get_object_or_404,redirect

from django.utils import timezone
import datetime
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippets,SnippetsComments
from .serializers import SnippetSerializer
from django.db import connection, transaction
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippets_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippets.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializers.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JSONResponse(serializers.data, status=201)
        return JSONResponse(serializers.errors, status=400)


@csrf_exempt
def snippets_Details(request,pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippets = Snippets.objects.get(pk=pk)
    except Snippets.DoesNotExist:
        return HttpResponse(status=404) #status=404 means Not Found

    if request.method=="GET":
        serializers=SnippetSerializer(snippets)
        return JSONResponse(serializers.data)


    elif request.method=="PUT":
        data=JSONParser().parse(request)
        serializers= SnippetSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            return JSONResponse(serializers.data)

        return JSONResponse(serializers.errors,response=400) #status=400 means Bad Request

    elif request.method == "DELETE":
        snippets.delete()
        return HttpResponse(status=204) #status=204 means No Content Found



def snippets_detaillist(request):
    overall=Snippets.objects.filter(created__gte=timezone.now()-datetime.timedelta(days=1)).order_by('-created')
    return render(request,"snippets/snippets.html",{'overall':overall})




def SnipCmnts(request):
    cursor = connection.cursor()
    cursor.execute("""SELECT ss.id AS snippets_id,
    ss.created,ss.title,ss.lineos,c.id AS comment_id,c.`comments` AS comment_text,
    c.`created` AS comment_created,c.`published` AS comment_published
     FROM `snippets_snippets` ss
    JOIN `comment` c ON ss.`id`=c.`snippet_id`""")
    customdata=cursor.fetchall()
    return render(request,"snippets/with_comments.html",{'customdata':customdata})

@login_required
def snippet_selectdetail(request):
    
    """
    snip=get_object_or_404(Snippets,pk=snippet_id)

    try:
        selected_comments=snip.comments.get(pk=request.POST['snippetscomments']) 
        #entities fetching in snippetscomments model
    except :
        return render(request,'snippets/details.html',{'snip':snip,'error_message':'No Comment Selected!'})

    else:
        #return HttpResponse("Valid entry inserted !")
        return render(request,'snippets/details.html',{'snip':snip,})
    """

    title = 'Welcome'
    if request.method == "POST":

        #print request.POST
        myform = CommentForm(request.POST)

        if myform.is_valid():
            instance = myform.save(commit=False)
            instance.comments=myform.cleaned_data.get("comments")
            instance.published=timezone.now()

            instance.save()
            print instance.comments
            print instance.published
            title='Thank You'
            return redirect('snippet_main:new_comment_detail',comment_id=instance.pk)


    else:
        myform=CommentForm()

    return render(request, 'snippets/details.html',{'form':myform,'title':title} )

def new_comment_detail(request,comment_id):
    cursor=connection.cursor()
    qry="""SELECT c.id AS comment_id,ss.title AS snippet_title,
    ss.CODE AS snippet_code,c.comments AS comment_data,c.published  FROM `comment` c
    JOIN snippets_snippets ss ON c.snippet_id=ss.id
    WHERE c.id={0}""".format(comment_id,)
    cursor.execute(qry)
    comment_data=cursor.fetchall()
    return render(request,"snippets/new_comment.html",{'comment_data':comment_data})


            







