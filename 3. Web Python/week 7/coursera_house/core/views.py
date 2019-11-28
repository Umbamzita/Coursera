import requests
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from django.http import HttpResponse
from .models import Setting
from .form import ControllerForm


token = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {token}'}

def update_bd(controller_name, label, value):
    try:
        contr = Setting.objects.get(controller_name=controller_name)
    except:
        Setting.objects.create(controller_name=controller_name, value=value, label=label)
    else:
        contr.value=value
        contr.save()



class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    



    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        
        try:
            controller_data = requests.get(url , headers=headers).json()
            context['data'] = controller_data
        except:
            return HttpResponse(status=502)
        return context

    def get_initial(self):
        initial = super(ControllerView, self).get_initial()
        initial['bedroom_target_temperature'] = 21
        initial['hot_water_target_temperature'] = 80
        return initial

    def form_valid(self, form):
        update_bd('bedroom_target_temperature', 
            'bedroom target temperature', 
            form.cleaned_data['bedroom_target_temperature'])

        update_bd('hot_water_target_temperature', 
            'hot water target temperature', 
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
            if controller_bedroom_light != form.cleaned_data['bedroom_light']:
                cont_load['controllers'].append(
                    {'name' : 'bedroom_light', 'value' : form.cleaned_data['bedroom_light']}
                    )
            elif controller_bathroom_light != form.cleaned_data['bathroom_light']:
                cont_load['controllers'].append(
                    {'name' : 'bathroom_light', 'value' : form.cleaned_data['bathroom_light']}
                    )
        cc=requests.post(url, headers=headers, json=cont_load).json()
        return super(ControllerView, self).get(form)
