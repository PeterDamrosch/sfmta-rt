import datetime
import requests
import xml.etree.ElementTree

# Get a list of routes from the Nextbus API

def get_route_list(agency_code):
	# Build URL
	base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a="
	routeList_url = base_url + agency_code

	# Send request
	response = requests.get(routeList_url)

	# Create XML tree
	tree = xml.etree.ElementTree.fromstring(response.content)

	# Add tags (aka ids) and titles (full route names) to a dictionary
	route_dict = {}
	for route in tree.findall('route'):
		tag = route.get('tag')
		title = route.get('title')
		route_dict[tag] = title

	# Return results
	return(route_dict)








# Gets all the stops and inbound and outbound stop orders for that route
# Can do for one route or up to 100 routes (SFMTA has 83 total)
# As well as paths - don't need this for now
#def get_route_config(agency_code):
	#base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a="
	#routeConfig = base_url + agency_code

#http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni
