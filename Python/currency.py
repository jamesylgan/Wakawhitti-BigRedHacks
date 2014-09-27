import requests
import ccy

# from bs4 import BeautifulSoup

# http://www.ozforex.com.au/forex-tools/historical-rate-tools/monthly-average-rates

# How many ___ you get for 1 USD
# might be better to switch from currency code to country name
# need function to find currency code given a country
currency_list = {'AED' : 3.67, 'ARS' : 3.44, 'AUD' : 1.35, 'BGN' : 1.60,
	'BND' : 1.52, 'CAD' : 1.26, 'CHF' : 1.28, 'CLP' : 561.04, 'CNY' : 7.31,
	'CZK' : 24.16, 'DKK' : 6.24, 'EGP' : 5.59, 'EUR' : 0.84, 'FJD' : 1.86,
	'GBP' : 0.61, 'HKD' : 7.77, 'HUF' : 217.35, 'IDR' : 9369.02, 'ILS' : 4.09,
	'INR' : 41.39, 'ISK' : 94.79, 'JPY' : 110.30, 'KRW' : 1030.96, 'KWD' : .29,
	'LKR' : 84.79, 'MAD' : 8.93, 'MGA' : 1999.32, 'MXN' : 10.14, 'MYR' : 3.25,
	'NOK' : 6.73, 'NZD' : 1.63, 'OMR' : .38, 'PEN' : 3.10, 'PGK' : 2.80,
	'PHP' : 47.99, 'PKR' : 85.87, 'PLN' : 3.34, 'RUB' : 29.49, 'SAR' : 3.75,
	'SBD' : 5.83, 'SCR' : 8.84, 'SEK' : 7.41, 'SGD' : 1.55, "THB" : 33.26,
	'TOP' : 2.01, 'TRY' : 1.61, 'TWD' : 32.19, 'TZS' : 1268.51, 'USD' : 1.00,
	'VEF' : 4.70, 'VND' : 17448.41, 'VUV' : 115.96, 'WST' : 3.15, 'XOF' : 524.16,
	'XPF' : 101.56, 'ZAR' : 6.32}

def convert(a, b, c):
	a = a.upper()
	b = b.upper()
	url = ('http://rate-exchange.appspot.com/currency?from=%s&to=%s&q=1') % (a, b)
	r = requests.get(url)
	return r.json()['v']

def exchange_rate(a):
	return convert('USD',a,1)

# basically unneeded
def get_dataz(html_string):
	ret = []
	while html_string.find("<td>") != -1:
		first_td = html_string.find("<td>")
		next_td = html_string.find("</td>", first_td+1)
		if (html_string[first_td+4:next_td-1]).find(".") != -1:
			ret.append(float(html_string[first_td+4:next_td-1]))
			html_string = html_string[next_td+5:]
		else:
			html_string = html_string[next_td+5:]
	return ret

def get_average(lst):
	ave = 0
	for i in lst:
		ave += i
	return ave / len(lst)

# need to test
def exchange_ratio(curr):
 	cpis = consumer_price_index()
	try:
		return exchange_rate(curr) / currency_list[curr]
	except:
		return "Sorry, currency not supported"

# returns a dictionary of the CPI of a bunch of countries
def consumer_price_index():
	html = requests.get("http://www.numbeo.com/cost-of-living/rankings_by_country.jsp").text
	html = html.replace(" ","")
 	html = html.replace("\n","")
	d = {}
	html = html[html.find("cityOrCountryInIndicesTable"):]
	while html.find("cityOrCountryInIndicesTable") != -1:
		html = html[html.find("cityOrCountryInIndicesTable"):]
		country = html[29:html.find("</td>")]
		cpidex = html.find("right")
		cpiend = html.find("</td>",cpidex)
		cpi = html[cpidex+6:cpiend]
		d[country] = cpi
		html = html[html.find("cityOrCountryInIndicesTable",1):]
	return d

def cpi_ratio(country):
	cpis = consumer_price_index()
	try:
		return float(cpis['UnitedStates']) / float(cpis[country])
	except:
		return "Sorry, country not supported"


def cc_of_country(country):
	url = "http://www.freecurrencyconverterapi.com/api/v2/countries"
	json = requests.get("http://www.freecurrencyconverterapi.com/api/v2/countries").text
	c_index = json.find(country)
	curr_dex = json.rfind("currencyId",0,c_index)
	return json[curr_dex+13:curr_dex+16]

# Jisun had that cool list of country codes, we can use ccy with that to get
# currency code and country name, yay
# other than that preyy much done. huzzah!
def strength_of_dollar(country):
	print cpi_ratio(country)
	print currency_list[cc_of_country(country)]
	return cpi_ratio(country) * currency_list[cc_of_country(country)]

def sod_col(here, there, country):
	pass

# works great if we get cities
def cost_of_living_difference(here, there):
	url = 'http://www.expatistan.com/cost-of-living/comparison/' + here + '/' + there
	html = requests.get(url).text
	html = html[html.find("total"):]
	if html.find("cheaper") < html.find("expensiver") and html.find("cheaper") > 0:
		difference = html[html.find("cheaper")+9:html.find("</span>")-1]
		return 1.0 / float("." + difference)
	else:
		difference = html[html.find("expensiver")+12:html.find("</span>")-1]
		return float("." + difference)


if __name__ == '__main__':
	# print convert("USD","EUR",1)
	# print exchange_rate("EUR")
	# print ratio("EUR")
	# s = "<tr><td>01/1990</td><td>0.781105</td></tr><tr><td>02/1990</td><td>0.759321</td></tr>"
	# print get_dataz(s)

	# html = requests.get("http://www.numbeo.com/cost-of-living/rankings_by_country.jsp").text
	# html = html.replace(" ","")
 # 	html = html.replace("\n","")
 	# cpis = consumer_price_index()
 	# print cpis["UnitedStates"]

# 	print cost_of_living_difference("ithaca", "mumbai")

	# print cc_of_country("Afghanistan")

	print strength_of_dollar("Somalia")

 	# print cpi_ratio("India")
 	# print exchange_ratio("INR")

	# html = """<tr width="100%">
 #    <td class="cityOrCountryInIndicesTable">Norway</td>
 #    <td align=right>145.16</td>
 #    <td align=right>61.54</td>
 #    <td align=right>104.97</td>
 #    <td align=right>137.08</td>
 #    <td align=right>166.66</td>
 #    <td align=right>89.81</td>
 # 	</tr>"""
 	# html = html.replace(" ","")
 	# html = html.replace("\n","")
 	# c = consumer_price_index(html)
 	# print c


	# html = requests.get("http://www.ozforex.com.au/forex-tools/historical-rate-tools/monthly-average-rates").text
	# html = html.replace(" ", "")
	# html = html.replace("<strong>", "")
	# html = html.replace("</strong>", "")
	# html = html.replace("\n","")
	# print get_average(get_dataz(html))