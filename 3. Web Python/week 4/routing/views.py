from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

@require_GET
def simple_route(request):
    if request.method == 'GET':
        return HttpResponse()
 
    
def slug_route(request, slug):
    return HttpResponse(slug)
    

def sum_route(request, a, b):
    a = int(a)
    b = int(b)
    
    return HttpResponse(a + b)

@require_GET    
def  sum_get_method(request):
    try:
        
        return HttpResponse(int(request.GET.get('a'))+int(request.GET.get('b')))
    except:
        return HttpResponseBadRequest()
        

@require_POST          
def sum_post_method(request):
    try:
    
        a = int(request.POST.get('a'))
        b = int(request.POST.get('b'))
        
    except:
        return HttpResponseBadRequest()
        
    return HttpResponse(a+b)
    