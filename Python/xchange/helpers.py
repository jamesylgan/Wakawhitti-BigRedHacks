import ccy
import pickle

class Continent:
	def __init__(self, name):
		self.name = name
		self.country_list = []

class Country:
	def __init__(self, continent, country_code):
		self.continent = continent
		self.country_code = country_code
		self.name = ccy.country(country_code)
		self.currencyId = None
		self.city_list = []
		self.avg_rate = 0.
		self.curr_rate = 0.
		self.delta_percent = 0.

class City:
	def __init__(self, continent, country_code, name, population):
		self.continent = continent
		self.country_code = country_code
		self.country_name = ccy.country(country_code)
		self.name = name
		self.population = population

def get_countries():
	# country name, continent name
	f = open('country_continent.csv', 'r')
	f.readline()
	country_to_continent = {}
	continent_dict = {}

	for line in f:
		items = line.strip().split(',')
		if items[1] not in continent_dict.keys():
			continent_dict[items[1]] = Continent(items[1])
		# key: continent ID, value: Continent
		#continent_dict[items[1]].country_list.append(Country(items[1], items[0]))
		# used to be value: dictionary of (country ID, [cities list, delta%, current exchange rate])
		#continent_dict[items[1]][items[0]] = [None,None,None]
		country_to_continent[items[0]] = items[1]
	return (continent_dict, country_to_continent)

def populate_cities(continent_dict, country_to_continent):
	f = open('worldcitiespop_init.txt', 'r')
	#f2 = open('worldcitiespop.txt', 'w')

	f.readline()
	country_code_to_cities_dict = {}
	all_cities = set([])

	for line in f:
		items = line.strip().upper().split(',')
		country_code = items[0]
		if country_code not in country_to_continent.keys():
			continue;
		continent = country_to_continent[country_code]
		city_name = items[1]
		population = items[4]
		if population != '' and city_name not in all_cities:
			if country_code not in country_code_to_cities_dict.keys():
				country_code_to_cities_dict[country_code] = []
			cities = country_code_to_cities_dict[country_code]
			#f2.write("{0},{1},{2}\n".format(items[0], items[1], items[4]))
			city = City(continent, country_code, city_name, population)
			cities.append(city)
			all_cities.add(city_name)
	f.close()
	#f2.close()

	for k in country_code_to_cities_dict.keys():
		continent = country_to_continent[k]
		# country only gets added if it has a city
		country = Country(continent, k)
		country.city_list = list(country_code_to_cities_dict[k])
		continent_dict[continent].country_list.append(country)

	#print(str(len(all_cities)))
	#print(str(len(country_code_to_cities_dict['AE'])))

(continent_dict, country_to_continent) = get_countries()
populate_cities(continent_dict, country_to_continent)

"""
f3 = open('continent_dict_dump', 'w')
f4 = open('country_to_continent_dump', 'w')
pickle.dump(continent_dict, f3)
pickle.dump(country_to_continent, f4)
f3.close()
f4.close()
"""
"""
c = continent_dict['AF']
print c.name
for ctry in c.country_list:
	#print("country {0} has cities:".format(ctry.country_code))
	for city in ctry.city_list:
		print ("country {2} city {0} population {1}".format(city.name, city.population, city.country_name))
"""