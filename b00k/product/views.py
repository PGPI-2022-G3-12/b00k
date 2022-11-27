from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from . import models
import json
# Create your views here.

class ProductListView(TemplateView):
    template_name = 'product/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query:str = kwargs.get('q','')
        try:
            products = models.BookProduct.objects.filter(title__contains=query)
            context['products'] = json.dumps(products)

        except:
            raise Http404
        return context

class ProductDetailView(TemplateView):
    template = 'product/single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pid = kwargs.get('product_id',0)
        try:
            product = models.BookProduct.objects.get(pk=pid)
            context['product'] = json.dumps(product)
        except:
            raise Http404
        return context