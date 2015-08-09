#!/usr/bin/env python
import csv
import os
import subprocess
import sys
import urllib
import zipfile


def filter_into_city(filename):
    city = raw_input('\nEnter city [default=None]: ')
    print "Filtering data..."

    if city:
        city = city.upper()
        output_dir = os.path.dirname(os.path.realpath(filename))
        output_file_name = output_dir + '/' + city + '.csv'

        with open(output_file_name, 'w') as output_file:
            # Fill the header
            r_val = subprocess.call(
                ['head', '-n', '1', filename],
                stdout=output_file,
            )
            if r_val > 0:
                print 'There was an error reading the downloaded data.'
                sys.exit(1)

            # Filter in the data
            city_column = 12
            pattern = '^([^,]*,){' + str(city_column) + '}' + city + ','
            r_val = subprocess.call(
                ['grep', '-E', pattern, filename],
                stdout=output_file,
            )
            if r_val > 0:
                print city + ' was not found in the data set.'
                sys.exit(1)

        return output_file_name

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

    url = 'ftp://sosftp.sos.state.oh.us/free/Voter/{}.zip'.format(
        counties[county],
    )
    my_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = my_dir + '/data/' + counties[county] + '_COUNTY/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = output_dir + counties[county] + '.zip'

    print '\nDownloading data...'

    urllib.urlretrieve(url, output_file)

    with zipfile.ZipFile(output_file, 'r') as z:
        z.extractall(output_dir)

    os.remove(output_file)

    old_filename = output_dir + counties[county] + '.TXT'
    new_filename = output_dir + counties[county] + '_COUNTY.csv'
    os.rename(old_filename, new_filename)

    return new_filename


def parse_parties(filename):
    print "Inferring party affiliations..."

    party_column = 9
    first_election_column = 45

    democrats = []
    republicans = []
    independents = []

    with open(filename, 'rb') as input_file:
        reader = csv.reader(input_file)

        header = next(reader)

        for row in reader:
            party = None

            if len(row) > party_column:
                if row[party_column] == 'D' or row[party_column] == 'R':
                    party = row[party_column]
                else:
                    column = first_election_column
                    while column < len(row):
                        if row[column] == 'D' or row[column] == 'R':
                            party = row[column]
                        column += 1

            if party == 'D':
                democrats.append(row)
            elif party == 'R':
                republicans.append(row)
            else:
                independents.append(row)

    filename_pieces = filename.split('.')

    democrats_output = '{}_DEMOCRATS.{}'.format(
        filename_pieces[0],
        filename_pieces[1],
    )
    republicans_output = '{}_REPUBLICANS.{}'.format(
        filename_pieces[0],
        filename_pieces[1],
    )
    independents_output = '{}_INDEPENDENTS.{}'.format(
        filename_pieces[0],
        filename_pieces[1],
    )

    with open(democrats_output, 'wb') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for row in democrats:
            writer.writerow(row)

    print '\nFound ' + str(len(democrats)) + ' Democrats.'
    print 'Data output to ' + democrats_output

    with open(republicans_output, 'wb') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for row in republicans:
            writer.writerow(row)

    print '\nFound ' + str(len(republicans)) + ' Republicans.'
    print 'Data output to ' + republicans_output

    with open(independents_output, 'wb') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        for row in independents:
            writer.writerow(row)

    print '\nFound ' + str(len(independents)) + ' Independents.'
    print 'Data output to ' + independents_output

if __name__ == '__main__':
    downloaded_data = download_data()
    filtered_data = filter_into_city(downloaded_data)
    parse_parties(filtered_data)
