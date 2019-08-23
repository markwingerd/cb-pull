from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Company

class IndexView(generic.ListView):
    template_name = 'company/index.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        return Company.objects.order_by('name')

class DetailView(generic.DetailView):
    model = Company
    template_name = 'company/detail.html'
