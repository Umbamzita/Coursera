import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Item, Review
from django.forms.models import model_to_dict






class ItemForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)

class ReviewForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)
    



@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):

    def post(self, request):
        
        form = ItemForm(request.POST)

        if form.is_valid():
            data=form.cleaned_data
            m=Item.objects.create(**data)
            id=m.id
            return JsonResponse({'id' : id}, status=201, safe=False)
        return JsonResponse({}, status=400, safe=False, json_dumps_params={'ensure_ascii': False})
        
            

@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    

    def post(self, request, item_id):
        try:
            item=Item.objects.get(id=item_id)

        except:
            return JsonResponse('товара с таким id не существует', status=404, safe=False, json_dumps_params={'ensure_ascii': False})

        form = ReviewForm(request.POST)
        if form.is_valid():
            
            message=form.cleaned_data['text']
            num=form.cleaned_data['grade']
            m=Review.objects.create(text=message, grade=num, item=Item.objects.get(id=item_id))
            return JsonResponse({'id':m.id}, status=201, safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse('запрос не прошел валидацию', status=400, safe=False, json_dumps_params={'ensure_ascii': False})    


@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):

    def get(self, request, item_id):
        try:
            data = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({}, status=404)

        item_good=model_to_dict(data)
        
        review_good=Review.objects.filter(item_id=item_id).order_by('-id').values('id','text','grade')[:5]

        item_good['reviews']=list(review_good)
        return JsonResponse(item_good, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
