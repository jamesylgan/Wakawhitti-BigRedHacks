from helpers import Continent, Country, City
import pickle
from requests import get, post

continent_name_to_id = {'ASIA':'AS', 'AFRICA':'AF', 'NORTH AMERICA': 'NA', 'SOUTH AMERICA': 'SA', 'ANTARCTICA': 'AN', 'EUROPE': 'EU', 'AUSTRALIA':'OC'}
continent_dict = None
country_to_continent = None
data = None
NUM_SUGGESTIONS = 5

def getCurrencyId(country_id):
	global data

	if data == None:
		response = get('http://www.freecurrencyconverterapi.com/api/v2/countries')
		try:
			data = response.json()
		except:
			raise InvalidRequest(req + ' is not a valid request.')
		if 'error' in data:
			raise CallError('Error: ' + data['error'])
	if country_id not in data['results'].keys():
		return None
	return data['results'][country_id]['currencyId']

def setup():
	global continent_dict, country_to_continent

	f = open('continent_dict_dump', 'r')
	f2 = open('country_to_continent_dump', 'r')
	continent_dict = pickle.load(f)
	country_to_continent = pickle.load(f2)
	f.close()
	f2.close()
	f3 = open('currency_dict_dump', 'r')
	currency_dict = pickle.load(f3)
	f3.close()
	for cont_key in continent_dict.keys():
		cont = continent_dict[cont_key]
		countries_to_remove = set([])
		for country in cont.country_list:
			currencyId = getCurrencyId(country.country_code.upper())
			if currencyId == None:
				countries_to_remove.add(country)
			country.currencyId = currencyId
			if currencyId == 'USD':
				country.avg_rate = 1.
				country.curr_rate = 1.
				country.delta_percent = 0.
			else:
				if currencyId in currency_dict.keys():
					(country.avg_rate, country.curr_rate) = currency_dict[currencyId]
					country.delta_percent = (country.curr_rate - country.avg_rate) / country.avg_rate * 100.
				else:
					countries_to_remove.add(country)
		for c in countries_to_remove:
			print('removing {0}'.format(c.country_code))
			cont.country_list.remove(c)

	for continent in continent_dict.values():
		continent.country_list = sorted(continent.country_list, key=lambda country: country.delta_percent, reverse=True)

	f4 = open('continent_dict_with_rates_dump', 'w')
	pickle.dump(continent_dict, f4)
	f4.close();

def load():
	global continent_dict, country_to_continent

	f = open('continent_dict_with_rates_dump', 'r')
	f2 = open('country_to_continent_dump', 'r')
	continent_dict = pickle.load(f)
	country_to_continent = pickle.load(f2)
	f.close()
	f2.close()
	for continent in continent_dict.values():
		continent.country_list = sorted(continent.country_list, key=lambda country: country.delta_percent, reverse=True)

def get_recommendation(continent_name):
	global continent_name_to_id, continent_dict, NUM_SUGGESTIONS

	d = {}

	if continent_dict == None:
		load()

	# continent name not specified
	if continent_name == None:
		countries = []
		for ctnt in continent_dict.values():
			countries.extend(ctnt.country_list[:NUM_SUGGESTIONS])
		return sorted(countries, key=lambda country: country.delta_percent, reverse=True)[:NUM_SUGGESTIONS]
	else:
		lst = continent_dict[continent_name_to_id[continent_name.upper()]].country_list
		count = 0
		for country in lst:
			best_city_list = rank_cities(country.country_code)
			city_name_list = []
			for city in best_city_list:
				city_name_list.append(city.name)

			lsd = {'exchange_info' : country.delta_percent, 'cities' : city_name_list}
			d[country.name] = lsd
			if count >= NUM_SUGGESTIONS:
				break
			count += 1
	
		return d

	#     {'USA': { 'exchange_info': 'Monieesss', 'cities': ['New York', 'San Francisco']}}

def rank_cities(country_code):
	global continent_dict, country_to_continent, NUM_SUGGESTIONS
	code = country_code.upper()

	country = None
	for c in continent_dict[country_to_continent[code]].country_list:
		if c.country_code == code:
			country = c
			break
	if country == None:
		print "Invalid country code"
		return

	lst = sorted(country.city_list, key=lambda city: city.population, reverse=True)
	if len(lst) <= NUM_SUGGESTIONS:
		return lst
	return lst[:NUM_SUGGESTIONS]

def get_hotel_data(city_name, check_in, check_out):
	response = get('http://www.priceline.com/api/hotelretail/listing/v3/{0}/{1}/{2}/1/50'.format(city_name, check_in, check_out))
	try:
		data = response.json()
	except:
		raise InvalidRequest(req + ' is not a valid request.')
	if 'error' in data:
		raise CallError('Error: ' + data['error'])
	hotel_list = []
	for hotel_id in data['hotels'].keys():
		hotel = data['hotels'][hotel_id]
		hotel_list.append((hotel['hotelName'], hotel['starRating']))
		print('{0} rating: {1}'.format(hotel['hotelName'], hotel['starRating']))
	return sorted(hotel_list, key=lambda hotel: hotel[1], reverse=True)[:10]
	
if __name__ == '__main__':
	for continent_name in continent_name_to_id:
		print 'country recommendation'
		for country in get_recommendation(continent_name):
			print('{0} avg rate: {1}, curr rate: {2}, delta percent: {3}'.format(country.name, country.avg_rate, country.curr_rate, country.delta_percent))
			print 'city recommendation'
			for city in rank_cities(country.country_code):
				print('city {0} population {1}'.format(city.name, city.population))
