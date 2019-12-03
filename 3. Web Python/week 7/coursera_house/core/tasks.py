from __future__ import absolute_import, unicode_literals
from celery import task
from django.conf import settings
import requests
from django.core.mail import EmailMessage

from .models import Setting

token = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {token}'}

@task()
def smart_home_manager():
	controller_data = requests.get(url , headers=headers).json()['data']
	controllers={element['name']: element['value'] for element in controller_data}
	control_load = {'controllers' : [] }

	if controllers.get('curtains') == 'slightly_open':
		pass
	else:
		
		if controllers.get('outdoor_light') < 50 and not controllers.get('bedroom_light'):
			control_load['controllers'].append({'name' : 'curtains', 'value' : 'open'})

		elif controllers.get('outdoor_light') > 50 or controllers.get('bedroom_light'):
			control_load['controllers'].append({'name' : 'curtains', 'value' : 'close'})


	if controllers.get('leak_detector') or controllers.get('smoke_detector'):
		if controllers.get('cold_water'):
			control_load['controllers'].append({'name' : 'cold_water', 'value' : False})
		if controllers.get('hot_water'):
			control_load['controllers'].append({'name' : 'hot_water', 'value' : False})
		email = EmailMessage(
			'ATTENTION',
			'leak detector: cold water and hot water was closed',
			settings.EMAIL_HOST,
			[settings.EMAIL_RECEPIENT])
		email.send(fail_silently=False)
		
	     

	if not controllers.get('cold_water') or controllers.get('leak_detector'):
		if controllers.get('boiler'):
			control_load['controllers'].append({'name' : 'boiler', 'value' : False})
		if controllers.get('washing_machine') in ['on', 'broken']:
			control_load['controllers'].append({'name' : 'washing_machine', 'value' : 'off'})

	hot_water_target=Setting.objects.get(controller_name='hot_water_target_temperature').value
	bedroom_target=Setting.objects.get(controller_name= 'bedroom_target_temperature').value

	if controllers.get('smoke_detector'):
		if controllers.get('air_conditioner'):
			control_load['controllers'].append({'name' : 'air_conditioner', 'value' : False})
		if controllers.get('bedroom_light'):
			control_load['controllers'].append({'name' : 'bedroom_light', 'value' : False})
		if controllers.get('bathroom_light'):
			control_load['controllers'].append({'name' : 'bathroom_light', 'value' : False})
		if controllers.get('boiler'):
			control_load['controllers'].append({'name' : 'boiler', 'value' : False})
		if controllers.get('washing_machine') in ['on', 'broken']:
			control_load['controllers'].append({'name' : 'washing_machine', 'value' : 'off'})

	condition = { 'boiler' : not controllers.get('boiler') and \
		not controllers.get('smoke_detector') and \
		not controllers.get('leak_detector') and \
		controllers.get('cold_water')
		}  


	
	if (controllers.get('boiler_temperature') < hot_water_target*0.9) and \
	condition['boiler']:
		control_load['controllers'].append({'name' : 'boiler', 'value' : True})
	if controllers.get('boiler_temperature') > hot_water_target*1.1:
		control_load['controllers'].append({'name' : 'boiler', 'value' : False})


	if controllers.get('bedroom_temperature') > bedroom_target*1.1:
			control_load['controllers'].append({'name' : 'air_conditioner', 'value' : True})
	if (controllers.get('bedroom_temperature') < bedroom_target*0.9) and not controllers.get('smoke_detector'):
			control_load['controllers'].append({'name' : 'air_conditioner', 'value' : False})



	if control_load['controllers']:
		load=[]
		for x in control_load['controllers']:
			if x not in load:
				load.append(x)
	control_load['controllers']=load

	requests.post(url, headers=headers, json=control_load)

