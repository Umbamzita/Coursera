import requests
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from django.http import HttpResponse
from .models import Setting
from .form import ControllerForm
from django import forms


token = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {token}'}

def update_bd(controller_name, value):
    try:
        contr = Setting.objects.get(controller_name=controller_name)
    except Setting.DoesNotExist:
        Setting.objects.create(controller_name=controller_name, value=value)
    else:
        contr.value=value
        contr.save()


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not context.get('data'):
            return self.render_to_response(context, status=502)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        try:
            controller_data=requests.get(url, headers=headers).json()['data']
            controllers={element['name']: element['value'] for element in controller_data}
            context['data'] = controllers
        except:
            context['data'] = {}
        return context

    def get_initial(self):
        try:
            initial = super(ControllerView, self).get_initial()
            initial['hot_water_target_temperature'] = Setting.objects.get(controller_name='hot_water_target_temperature').value
            initial['bedroom_target_temperature'] = Setting.objects.get(controller_name= 'bedroom_target_temperature').value
        except:
            initial['bedroom_target_temperature'] = 21
            initial['hot_water_target_temperature'] = 80
        return initial

    def form_valid(self, form):
        update_bd('bedroom_target_temperature', 
            form.cleaned_data['bedroom_target_temperature'])

        update_bd('hot_water_target_temperature', 
            form.cleaned_data['hot_water_target_temperature'])

        controller_data = requests.get(url , headers=headers).json()['data']

        for element in controller_data:
            if element['name'] == 'bathroom_light':
                controller_bathroom_light = element['value']
            elif element['name'] == 'bedroom_light':
                controller_bedroom_light = element['value']
            elif element['name'] == 'smoke_detector':
                controller_smoke_detector = element['value']

        cont_load = {'controllers' : [] }

        if not controller_smoke_detector:
            if  form.cleaned_data['bedroom_light'] != controller_bedroom_light :
                cont_load['controllers'].append(
                    {'name' : 'bedroom_light', 'value' : form.cleaned_data['bedroom_light']}
                    )
            if form.cleaned_data['bathroom_light'] != controller_bathroom_light :
                cont_load['controllers'].append(
                    {'name' : 'bathroom_light', 'value' : form.cleaned_data['bathroom_light']}
                    )
        else:
            cont_load['controllers'].append(
                    {'name' : 'bedroom_light', 'value' : False})
            cont_load['controllers'].append(
                    {'name' : 'bathroom_light', 'value' : False})
            
            

        requests.post(url, headers=headers, json=cont_load)
        return super(ControllerView, self).get(form)
