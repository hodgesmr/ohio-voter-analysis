#!/usr/bin/env python
import csv
import os
import subprocess
import sys
import urllib
import zipfile


def filter_into_city(filename):
    city = raw_input('Enter city [default=None]: ')

    if city:
        city = city.upper()
        output_dir =  os.path.dirname(os.path.realpath(filename))
        output_file_name = output_dir + '/' + city + '.csv'

        with open(output_file_name, 'w') as output_file:
            # Fill the header
            r_val = subprocess.call(['head', '-n', '1', filename], stdout=output_file)
            if r_val > 0:
                print 'There was an error reading the downloaded data.'
                sys.exit(1)

            # Filter in the data
            city_column = 12
            pattern = '^([^,]*,){' + str(city_column) + '}' + city + ','
            r_val = subprocess.call(['grep', '-E', pattern, filename], stdout=output_file)
            if r_val > 0:
                print city + ' was not found in the data set.'
                sys.exit(1)

        return output_file

    else:
        return filename


def download_data():
    counties = [
            'ADAMS',
            'ALLEN',
            'ASHLAND',
            'ASHTABULA',
            'ATHENS',
            'AUGLAIZE',
            'BELMONT',
            'BROWN',
            'BUTLER',
            'CARROLL',
            'CHAMPAIGN',
            'CLARK',
            'CLERMONT',
            'CLINTON',
            'COLUMBIANA',
            'COSHOCTON',
            'CRAWFORD',
            'CUYAHOGA',
            'DARKE',
            'DEFIANCE',
            'DELAWARE',
            'ERIE',
            'FAIRFIELD',
            'FAYETTE',
            'FRANKLIN',
            'FULTON',
            'GALLIA',
            'GEAUGA',
            'GREENE',
            'GUERNSEY',
            'HAMILTON',
            'HANCOCK',
            'HARDIN',
            'HARRISON',
            'HENRY',
            'HIGHLAND',
            'HOCKING',
            'HOLMES',
            'HURON',
            'JACKSON',
            'JEFFERSON',
            'KNOX',
            'LAKE',
            'LAWRENCE',
            'LICKING',
            'LOGAN',
            'LORAIN',
            'LUCAS',
            'MADISON',
            'MAHONING',
            'MARION',
            'MEDINA',
            'MEIGS',
            'MERCER',
            'MIAMI',
            'MONROE',
            'MONTGOMERY',
            'MORGAN',
            'MORROW',
            'MUSKINGUM',
            'NOBLE',
            'OTTAWA',
            'PAULDING',
            'PERRY',
            'PICKAWAY',
            'PIKE',
            'PORTAGE',
            'PREBLE',
            'PUTNAM',
            'RICHLAND',
            'ROSS',
            'SANDUSKY',
            'SCIOTO',
            'SENECA',
            'SHELBY',
            'STARK',
            'SUMMIT',
            'TRUMBULL',
            'TUSCARAWAS',
            'UNION',
            'VANWERT',
            'VINTON',
            'WARREN',
            'WASHINGTON',
            'WAYNE',
            'WILLIAMS',
            'WOOD',
            'WYANDOT',
    ]

    for i in range(0, len(counties)):
        print str(i+1) + ' - ' + counties[i]

    try:
        prompt = 'Select county [1-' + str(len(counties)) + ']: '
        county = int(raw_input(prompt)) - 1
        if county not in range(0, len(counties)):
            raise ValueError
    except ValueError:
        print 'You must specify a known county'
        sys.exit(1)

    url = 'ftp://sosftp.sos.state.oh.us/free/Voter/' + counties[county] + '.zip'
    my_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = my_dir + '/data/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = output_dir + counties[county] + '.zip'

    print 'Downloading data...'

    urllib.urlretrieve(url, output_file)

    with zipfile.ZipFile(output_file, 'r') as z:
        z.extractall(output_dir)

    os.remove(output_file)

    old_filename = output_dir + counties[county] + '.TXT'
    new_filename = output_dir + counties[county] + '.csv'
    os.rename(old_filename, new_filename)

    return new_filename


def parse_parties(filename):
    pass


if __name__ == '__main__':
    downloaded_data = download_data()
    filtered_data = filter_into_city(downloaded_data)
    parse_parties(filtered_data)

