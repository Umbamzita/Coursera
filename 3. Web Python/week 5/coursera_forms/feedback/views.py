import json
from django.shortcuts import render
from django.http import JsonResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from django.views import View
from django.views.generic.edit import CreateView
from marshmallow import ValidationError as MarshmallowError
from .forms import DummyForm
from .schemas import REVIEW_SCHEMA, ReviewSchema
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import FeedBack


#login=hello password=world
class FeedBackCreateView(LoginRequiredMixin,CreateView):
	model = FeedBack
	fields = ['text', 'grade', 'subject']
	success_url = '/feedback/add'

	
@method_decorator(csrf_exempt, name='dispatch')
class SchemaView(View):

	
	def post(self,request):
		try:
			document = json.loads(request.body)
			validate(document, REVIEW_SCHEMA)
			return JsonResponse(document, status=201)
		except ValidationError as exc:
			return JsonResponse({'error': exc.message}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)

		
@method_decorator(csrf_exempt, name='dispatch')
class MarshView(View):

	
	def post(self,request):
		try:
			document=json.loads(request.body)
			schema = ReviewSchema()
			data = schema.loads(document)
			return JsonResponse(data, status=201)
		except MarshmallowError as exr:
			return JsonResponse({'error': exr.messages}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)