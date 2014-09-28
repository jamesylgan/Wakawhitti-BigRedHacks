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
	return render(request, 'suggestions.html', params)

def results(request):
	country = request.POST['country']
	city = request.POST['city']
	departure_date = request.POST['departure_date']
	return_date = request.POST['return_date']
	hotels = rec.get_hotel_data(city, departure_date.replace("-",""), return_date.replace("-",""))
	return render(request, 'results.html', { 'trips': hotels })

def home(request):
	return render(request, 'frontpage.html')

# {'USA': { 'exchange_info': 'Monieesss', 'cities': ['New York', 'San Francisco']}}


def yaydates(date_in, date_out):
	return date_out + date_in

# def get_hotels(city, date_in, date_out):
#  	url = 'http://www.priceline.com/api/hotelretail/listing/v3/' + city + '/' + date_in + '/' + date_out + '/1/10'
#  	# url = 'http://www.priceline.com/svcs/ac/index/hotels/' + city
#  	j = requests.get(url).text
#  	dec = json.loads(j)
#  	hotel_ids = dec['hmiSorted']

 	