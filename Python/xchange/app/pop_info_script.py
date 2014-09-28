import ccy
import pickle

f = open('worldcitiespop_init.txt', 'r')
f2 = open('worldcitiespop.txt', 'w')

line = f.readline()
items = line.split(',')
f2.write("{0},{1},{2}\n".format(items[0], items[1], items[4]))

country_codes = {}
all_cities = set([])

for line in f:
	items = line.split(',')
	city = "{0},{1}".format(items[0], items[1])
	if items[4] != '' and city not in all_cities:
		if items[0] not in country_codes.keys():
			country_codes[items[0]] = set([])
		cities = country_codes[items[0]]
		country_name = items[0] # change this to ccy.country(items[0]) to get actual name
		f2.write("{0},{1},{2}\n".format(items[0], items[1], items[4]))
		cities.add(city)
		all_cities.add(city)

f.close()
f2.close()

print(str(len(all_cities)))
print(str(len(country_codes['ae'])))

f3 = open('cities_dict_dump', 'w')
f4 = open('cities_all_dump', 'w')
pickle.dump(country_codes, f3)
pickle.dump(all_cities, f4)
f3.close()
f4.close()
