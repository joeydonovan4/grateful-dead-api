#!/usr/bin/python
from datetime import datetime
from collections import namedtuple, OrderedDict
import json
import os
import sys

PATH = "setlists/"
USA = "USA"

def main():
    with open('dates.txt', 'r') as dates:
        data = OrderedDict()
        data['date'] = ''
        data['day'] = ''
        data['venue'] = ''
        data['city'] = ''
        data['state'] = ''
        data['country'] = ''

        setlist_ordered = OrderedDict()
        setlist_ordered['setOne'] = []
        setlist_ordered['setTwo'] = []
        setlist_ordered['encore'] = []
        data['setlist'] = setlist_ordered

        current_year = ''
        for line in dates:
            if not line.strip():
                continue

            if len(line) == 5:
                current_year = line.strip()
            else:
                split = [x.strip() for x in line.split('-', 1)]
                date_tuple = parse_date(split[0], current_year)
                #if data['date'] != '' and date_tuple.date <= data['date']:
                #    print('bad date: {}'.format(date_tuple.date))
                #    sys.exit()
                data['day'] = date_tuple.weekday
                data['date'] = date_tuple.date
                parse_location(split[1], data)
            
                filename = generate_filename(data['date'])
                create_json(data, filename, current_year)

def generate_filename(date):
    parsed = datetime.strptime(date, "%B %d, %Y")
    filename_format = parsed.strftime("%m.%d.%y")
    filename = filename_format + '.json'
    return filename

Date = namedtuple('Date', 'weekday date')

def parse_date(date, year):
    date = date + '/' + year
    parsed = datetime.strptime(date, "%m/%d/%Y")
    day_of_week = parsed.strftime('%A')
    date = parsed.strftime('%B %-d, %Y')

    formatted = Date(day_of_week, date)
    return formatted

def parse_location(l, d):
    if l == '""':
        return
    split = [x.strip() for x in l.split(',')]
    d['venue'] = split[0]
   
    state = ''
    #handle Washington, DC
    if len(split) > 3:
        d['city'] = split[1] + ", " + split[2]
        state = split[3]
    else:
        d['city'] = split[1]
        state = split[2]

    set_state_and_country(state, d) 

def set_state_and_country(loc, d):
    if len(loc) > 2:
        d['state'] = 'N/A'
        d['country'] = loc
    elif len(loc) == 2:
        d['state'] = loc
        d['country'] = USA
    else:
        print('Bad state input: {}'.format(loc))
        sys.exit()

def create_json(d, filename, year):
    year = year[len('19'):]
    directory = PATH + year
    if not os.path.exists(directory):
        os.makedirs(directory)

    full_path = directory + '/' + filename 
    with open(full_path, 'w') as outfile:
        print('writing to {}'.format(full_path))
        json.dump(d, outfile)

