from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from .models import BookProduct 
import json
from django.conf import settings
# Create your views here.
BASE_URL = settings.BASE_URL
class ProductListView(TemplateView):
    template_name = 'product/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query:str = kwargs.get('q','')
        try:
            products = BookProduct.objects.filter(title__contains=query)
            context['products'] = json.dumps(products)
            context['query'] = json.dumps(query)

        except:
            raise Http404
        return context

class ProductDetailView(TemplateView):
    template_name = 'single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pid = kwargs.get('product_id',0)
        try:
            #TOFIX: No detecta el objeto pese a existir en la db
            product = BookProduct.objects.get(pk=pid)
            context['product'] = product
            context['BASE_URL'] = BASE_URL
        except:
            raise Http404
        return context