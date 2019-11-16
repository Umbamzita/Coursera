import json
from jsonschema import validate 
from jsonschema.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.forms.models import model_to_dict

from .models import Item, Review
import base64

from django.contrib.auth import authenticate
#from django.conf import settings

REVIEW_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 64,
            },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
            },
        'price': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000000
        }
    },
    'required': ['title', 'description', 'price'],
}

REVIEW_SCHEMA_REVIEW = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
            },
        'grade': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 10
        }
    },
    'required': ['text', 'grade'],
}


@method_decorator(csrf_exempt, name="dispatch")
class AddItemView(View):

    def post(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode("utf-8").split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_staff:
                        request.user = user
                        try:
                            document = json.loads(request.body.decode('utf-8'))
                            validate(document, REVIEW_SCHEMA)
                            m = Item.objects.create(**document)
                            m.save()
                            return JsonResponse({"id" : m.id}, status=201)
                        except json.JSONDecodeError:
                            return JsonResponse({"error": "JsonDecoder"}, status=400)
                        except ValidationError as exc:
                            return JsonResponse({"error": exc.message}, status=400)
                    elif user is not None:
                        return JsonResponse({}, status=403)
                    else:
                        return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=401)            
                    

@method_decorator(csrf_exempt, name="dispatch")
class PostReviewView(View):
    
    def post(self, request, item_id):
        try:
            document = json.loads(request.body.decode('utf-8'))
            validate(document, REVIEW_SCHEMA_REVIEW)
            product = Item.objects.get(id = item_id)
            m = Review.objects.create(grade = document['grade'],\
                text = document['text'], item = product)
            m.save()
            return JsonResponse({'id' : m.id}, status=201)
        except ValidationError as exc:
            return JsonResponse({"error": exc.message}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JsonDecoder"}, status=400)
        except:
            return JsonResponse({"error": "product not found"}, status=404) 




@method_decorator(csrf_exempt, name="dispatch")
class GetItemView(View):

    def get(self, request, item_id):
        try:
            data = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse({}, status=404)

        item_good=model_to_dict(data)
        
        review_good=Review.objects.filter(item_id=item_id).order_by("-id").values("id","text","grade")[:5]

        item_good["reviews"]=list(review_good)
        return JsonResponse(item_good, status=200, safe=False, json_dumps_params={"ensure_ascii": False})
