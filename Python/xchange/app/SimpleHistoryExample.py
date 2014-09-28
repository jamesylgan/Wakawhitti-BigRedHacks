# SimpleHistoryExample.py

import blpapi
import pickle

import ccy
from requests import get, post
from optparse import OptionParser


def parseCmdLine():
    parser = OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="10.8.8.1")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options

def getCurrencyId(country_id):
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

def main():
    options = parseCmdLine()

    # Fill SessionOptions
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print "Connecting to %s:%s" % (options.host, options.port)
    # Create a Session
    session = blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print "Failed to start session."
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print "Failed to open //blp/refdata"
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create and fill the request for the historical data
        request = refDataService.createRequest("HistoricalDataRequest")
        """
        to get exchange rate, use "USD{other currency code} CURNCY" 
        """
        #f = open('cities_dict_dump', 'r')
        #cities_dict = pickle.load(f)
        #keys = cities_dict.keys()
        
        f2 = open('country_to_continent_dump', 'r')
        country_to_continent = pickle.load(f2)
        f2.close()
        keys = country_to_continent.keys()
        invalid_keys = set([])
        
        for k in keys:
            currencyId = getCurrencyId(k.upper())
            if currencyId == None:
                print("no currency id for {0}: {1}".format(k, ccy.country(k)))
                continent = country_to_continent[k]
                invalid_keys.add(k)
            else:
                #print("key: {0}, country: {1}, currency: {2}".format(k, ccy.country(k) , currencyId))
                if currencyId != 'USD':
                    request.getElement("securities").appendValue("USD{0} CURNCY".format(currencyId))
        
        #request.getElement("securities").appendValue("USDGIP CURNCY")
        #request.getElement("securities").appendValue("USDEUR CURNCY")
        #request.getElement("securities").appendValue("USDJPY CURNCY")
        request.getElement("fields").appendValue("PX_LAST")
        request.getElement("fields").appendValue("OPEN")
        request.set("periodicityAdjustment", "ACTUAL")
        request.set("periodicitySelection", "DAILY")#"MONTHLY")
        request.set("startDate", "20110927")
        request.set("endDate", "20140927")
        request.set("maxDataPoints", 9999999)

        currency_dict = {}

        print "Sending Request:", request
        # Send the request
        session.sendRequest(request)

        # Process received events
        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                if str(msg.messageType()) == "HistoricalDataResponse":
                    fieldData = msg.asElement().getElement("securityData").getElement("fieldData");
                    rate_avg = 0.;
                    last_val = 0.;
                    numData = fieldData.numValues()
                    returnList = [[0 for col in range(fieldData.getValue(row).numValues()+1)] for row in range(numData)]
                    for row in range(numData):
                        rowField = fieldData.getValue(row)
                        for col in range(rowField.numValues()+1):
                            colField = rowField.getElement(col)
                            returnList[row][col] = colField.getValue()
                            last_val = returnList[row][col]
                            if col == rowField.numValues():
                                rate_avg += returnList[row][col]
                    if numData == 0:
                        print("no data for {0}".format(msg.asElement().getElement("securityData").getElement("security")))
                        rate_avg = 1.0
                    else:
                        rate_avg /= numData
                        elem = msg.asElement().getElement("securityData").getElement("security")
                        currency_dict[str(elem).split('USD')[1][:3]] = (rate_avg, last_val)
                    #print("avg: {0}".format(str(rate_avg)))
                #print msg

            if ev.eventType() == blpapi.Event.RESPONSE:
                # Response completly received, so we could exit
                break
        f = open('currency_dict_dump', 'w')
        pickle.dump(currency_dict, f)
        f.close()

    finally:
        # Stop the session
        session.stop()

if __name__ == "__main__":
    print "SimpleHistoryExample"
    try:
        main()
    except KeyboardInterrupt:
        print "Ctrl+C pressed. Stopping..."

__copyright__ = """
Copyright 2012. Bloomberg Finance L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
