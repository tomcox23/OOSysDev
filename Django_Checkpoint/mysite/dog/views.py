from django.shortcuts import render
from django.conf import settings
from django.db import models

User= settings.AUTH_USER_MODEL

# Create your views here.
from django.http import HttpResponse
from dog.models import Breed
from dog.filters import BreedFilter

def dog_query_view(request):

	breed_list = Breed.objects.all()
	breed_filter = BreedFilter(request.GET, queryset=breed_list)

	return render(request, 'dog/index.html', {'filter': breed_filter})