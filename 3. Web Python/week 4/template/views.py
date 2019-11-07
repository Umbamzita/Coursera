from django.shortcuts import render,  HttpResponse


# Create your views here.

def echo(request):
    par = { 
    'get' : request.GET, 
    'post' : request.POST, 
    'meta' : request.META 
    }
   
    
    return render(request, 'echo.html', context = par)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
