import time
import datetime
import requests
import sys
import xml.etree.ElementTree
from optparse import OptionParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

# Get a list of routes from the SF-Muni Nextbus API
# Adapted from Matt Conway's gtfsrdb

# Parse options - database URL and wait time (default 30)
p = OptionParser()
p.add_option('-d', '--database', default=None, dest='dsn',
             help='Database connection string', metavar='DSN')

p.add_option('-w', '--wait', default=30, type='int', metavar='SECS',
             dest='timeout', help='Time to wait between requests (in seconds)')
opts, args = p.parse_args()

# Warning if no database specified
if opts.dsn == None:
    print('No database specified!')
    sys.exit(1)

# Database connection
engine = create_engine(opts.dsn)
session = sessionmaker(bind=engine)()
Base.metadata.create_all(engine)

# Send requests
keep_running = True
while keep_running:

	try:
		# Send request
		request_time = datetime.datetime.now()
		vehiclePositions_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni"
		response = requests.get(vehiclePositions_url)

		# Create XML tree
		vp_tree = xml.etree.ElementTree.fromstring(response.content)
		vehicle_tree = vp_tree.findall('vehicle')

		# Loop through tree pulling out each vehicle
		for vehicle in vehicle_tree:
			# Empty lead vehicle since they don't all have them (for two car trains)
			#leading_vehicle = ''
			#if vehicle.get('leadingVehicleId'):
				#leading_vehicle = vehicle.get('leadingVehicleId')

			# Create row for vehicle
			vehicle_update = VehiclePosition(
				veh_id = vehicle.get('id'),
				route_tag = vehicle.get('routeTag'),
				dir_tag = vehicle.get('dirTag'),
				pos_lat = vehicle.get('lat'),
				pos_lon = vehicle.get('lon'),
				pos_speed = vehicle.get('speedKmHr'),
				last_report = vehicle.get('secsSinceReport'),
				lead_veh = vehicle.get('leadingVehicleId'),
				timestamp = request_time)

			# Add row to session
			session.add(vehicle_update)

		# Commit rows to database
		session.commit()

		print('Added {} vehicle positions at {}'.format(str(len(vehicle_tree)), request_time))

	except:
		print('Exception occurred in iteration')

	time.sleep(opts.timeout)


		