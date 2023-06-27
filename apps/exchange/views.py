from django.shortcuts import render
from django.views.generic import TemplateView
from apps.reviews.models import Review

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_reviews = Review.objects.order_by('-created_at')[:5]
        context['reviews'] = latest_reviews
        return context


class AmlView(TemplateView):
    template_name = 'aml.html'


class RulesView(TemplateView):
    template_name = 'rules.html'


class NoticeView(TemplateView):
    template_name = 'notice.html'

    
