from django.shortcuts import render
from django import forms
import recommendation as rec
# from logic import get_recommendations, get_trips

# Create your views here.

def suggestions(request):
	continent = request.POST['region']
	departure_date = request.POST['departure_date']
	return_date = request.POST['return_date']
	countries = rec.get_recommendation(continent)
	params = { 'countries': countries,
			  'departure_date': departure_date,
			  'return_date': return_date }
	print params
	return render(request, 'suggestions.html', params)
	# params = { 'countries': {'USA': { 'exchange_info': 'Monieesss', 'cities': ['New York', 'San Francisco']}},
	# 		  'departure_date': 'now!',
	# 		  'return_date': 'tomorrow!' }
	# return render(request, 'suggestions.html', params)

def results(request):
	country = request.POST['country']
	city = request.POST['city']
	departure_date = request.POST['departure_date']
	return_date = request.POST['return_date']
	# trips = get_trips(country, cities, departure_date, return_date)
	return render(request, 'results.html', { 'trips': ['I love candy!', 'do you?'] })

def home(request):
	return render(request, 'frontpage.html')

# {'USA': { 'exchange_info': 'Monieesss', 'cities': ['New York', 'San Francisco']}}