from django.shortcuts import render,HttpResponse

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Snippets
from .serializers import SnippetSerializer

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







