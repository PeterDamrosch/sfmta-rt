import datetime
import requests
import sys
import xml.etree.ElementTree
from optparse import OptionParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

# Get a list of routes from the Nextbus API
# Adapted from Matt Conway's gtfsrdb

# Parse the database option
p = OptionParser()
p.add_option('-d', '--database', default=None, dest='dsn',
             help='Database connection string', metavar='DSN')

opts, args = p.parse_args()

if opts.dsn == None:
    print('No database specified!')
    sys.exit(1)

# Connect to the database, create session, create table
engine = create_engine(opts.dsn)
session = sessionmaker(bind=engine)()
Base.metadata.create_all(engine)

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

request_time = datetime.datetime.now()
def get_vehicle_positions(agency_code):
	request_time = datetime.datetime.now()
	base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a="
	vehiclePositions_url = base_url + agency_code

	# Send request
	response = requests.get(vehiclePositions_url)

	# Create XML tree
	tree = xml.etree.ElementTree.fromstring(response.content)
	return(tree)

def parse_vehicle_tree_dict(vp_tree):
	### Just a test for parsing, which works ###
	### When I implement it for real, will want the for-loop
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

def add_to_database(vp_tree):
	for vehicle in vp_tree.findall('vehicle'):
		# Empty lead vehicle since they don't all have them (for two car trains)
		leading_vehicle = ''
		if vehicle.get('leadingVehicleId'):
			leading_vehicle = vehicle.get('leadingVehicleId')

		# Create row for vehicle
		vehicle_update = VehiclePosition(
			veh_id = vehicle.get('id'),
			route_tag = vehicle.get('routeTag'),
			dir_tag = vehicle.get('dirTag'),
			pos_lat = vehicle.get('lat'),
			pos_lon = vehicle.get('lon'),
			pos_speed = vehicle.get('speedKmHr'),
			last_report = vehicle.get('secsSinceReport'),
			lead_veh = leading_vehicle,
			timestamp = request_time)

		# Add row to session
		session.add(vehicle_update)

	# Commit rows to database
	session.commit()

		


	



















# Gets all the stops and inbound and outbound stop orders for that route
# Can do for one route or up to 100 routes (SFMTA has 83 total)
# Has things like the 
# As well as paths - don't need this for now
#def get_route_config(agency_code):
	#base_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a="
	#routeConfig = base_url + agency_code

#http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni
