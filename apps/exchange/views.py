from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class AmlView(TemplateView):
    template_name = 'aml.html'

class RulesView(TemplateView):
    template_name = 'rules.html'