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

def get_vehicle_positions(agency_code):
	base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a="
	vehiclePositions_url = base_url + agency_code

	# Send request
	response = requests.get(vehiclePositions_url)

	# Create XML tree
	tree = xml.etree.ElementTree.fromstring(response.content)
	return(tree)

def parse_vehicle_tree(vp_tree):
	### Just a test for parsing, which works ###
	### When I implement it for real, will won't the for-loop
		# and then create a new sqlalchemy instance of class VehiclePosition
		# and add to database at the end of each loop
	position_dict = {}
	for vehicle in vp_tree.findall('vehicle'):
		vehicle_id = vehicle.get('id')
		vehicle_route = vehicle.get('routeTag')
		direction_tag = vehicle.get('dirTag')
		vp_lat = vehicle.get('lat')
		vp_lon = vehicle.get('lon')
		last_report = vehicle.get('secsSinceReport')
		position_dict[vehicle_id] = {'vid': vehicle_id, 
			'route': vehicle_route,
			'direction': direction_tag,
			'lat': vp_lat,
			'lon': vp_lon,
			'lastReport': last_report}
	return(position_dict)













# Gets all the stops and inbound and outbound stop orders for that route
# Can do for one route or up to 100 routes (SFMTA has 83 total)
# Has things like the 
# As well as paths - don't need this for now
#def get_route_config(agency_code):
	#base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a="
	#routeConfig = base_url + agency_code

#http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni
