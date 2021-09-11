"""
The following is a customised version of ANUs Intro to Data Science course.
"""

###   ###   ----------------------------------------------------------------
# Import statements
import sys
import csv
import numpy as np


###   ###   ----------------------------------------------------------------
# Constants
MONTHS_NAMES = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
MONTHS = dict(zip(MONTHS_NAMES, range(1,13)))
YEAR_NAMES = ['Kindergarten', 'Year 1', 'Year 2', 'Year 3', 'Year 4',
            'Year 5', 'Year 6', 'Year 7', 'Year 8', 'Year 9', 'Year 10', 'Year 11', 'Year 12', 'Older']
SCHOOL_YEARS = dict(zip(YEAR_NAMES, range(0,14)))
SCHOOL_YEARS['Preschool'] = 0
PRESCHOOL_AGES = [4]
KINDERGARTEN_AGES = [5]
PRIMARY_SCHOOL_AGES = list(range(6,12))
JUNIOR_SCHOOL_AGES = PRESCHOOL_AGES + KINDERGARTEN_AGES + PRIMARY_SCHOOL_AGES
SECONDARY_SCHOOL_AGES = list(range(12,18))

###   ###   ----------------------------------------------------------------
# Numpy Data Types
dt_school = np.dtype([
                ('name','<U50'),
                ('address','<U30'),
                ('suburb','<U30'),
                ])
dt_census = np.dtype([
                ('date', '<M8[D]'), 
                ('name','<U50'),
                ('year_level','<i8'),
                ('enrolment','<i8'),
                ])

###   ###   ----------------------------------------------------------------
def get_school_data(fname, dt=dt_school):
    """
    Reads the school location data file fname, extracts values for
    school names, addresses and suburbs, packs them into 3-tuple of str
    and returns a list of those. Alternatively, returns an NumPy
    array with dtype=dt_school
    """
    try:
        output = []
        with open('ACT_School_Locations_2017_-_archived.csv') as fopen:  
            csv_reader = csv.reader(fopen) 
            next(csv_reader)                        # skip the header
            for row in csv_reader: 
                name, address, suburb = row[:3]     # slice first 3 records
                output.append((name, address, suburb)) # append the constructed 3-tuple
        return output
    except IOError as ioe:
        print(f'{ioe}: File not found or unreadable', file=sys.stderr)
    except Exception as ie:
        print(f'{ie}: Data file is ill-formatted', file=sys.stderr)


########################################################################################################################
#                                   PART 1 - DATA PREPARATION & CLEANING
#                                                Tasks 1 - 6.        
########################################################################################################################

###   ###   ----------------------------------------------------------------
###  TASK 1A    
###  FORMAT DATE VARIABLE
#      Format date from long format character string to
#      either YYYY-MM-DD or YYYY formats
def format_date(s, short_format=True):
    """
    Converts a string date representation formatted as
    'Date Month_Name Year' into a string YYYY-MM-DD 
    (if short_format = False), or a string YYYY (if short_format = True)
    Note for testing: 
    format_date('21 February 2018', False)) should return '2018-02-21'
    format_date('20 February 2019')) should return '2019'
    """
    s = s.split() # Splits the date into 3
    if short_format == False: # If a long format is called.
        if len(str(MONTHS[s[1]])) < 1:
            s[1] = str(MONTHS[s[1]])
        else:
            s[1] = str(0) + str(MONTHS[s[1]])
        return s[2] + '-' + s[1] + '-' + s[0] # Adds dashes
    else:
        return s[2]

###   ###   ----------------------------------------------------------------
###  TASK 1B
###  FORMAT SCHOOL NAME VARIABLE
#      Clean school name, removing unnecessary text and
#      applying consistency
def clean_school_name(sname):
    """
    Normalise school names - which can be present as either
    '"Woden School, The"' or as 'The Woden School'; the double quote removal
    is necessary if the data is read with Numpy's genfromtxt and a field
    in a record is embedded in them.
    For Testing:
    clean_school_name('The Woden School') should return 'Woden School'
    clean_school_name('Canberra College, The') should return 'Canberra College'
    """
    sname = sname.replace('The ', '') # Removes 'The ' in the school name.
    sname = sname.replace(', The', '') # Removes ', The' in the school name. 
    return sname

###   ###   ----------------------------------------------------------------
###  TASK 1C 
###  FORMAT YEAR LEVEL VARIABLE
#      Convert year level variable to integer value
def convert_level(year_level):
    """
    Maps year level to int; the value is the same as the year
    level for 1..12, for preschool and kindergarten it's 0, for
    older and mature (or just older) it's 13
    For testing:
    convert_level('Year 11') should be 11
    convert_level('Kindergarten') shouuld be 0
    convert_level('Preschool' should be 0
    convert_level('Older') shouuld be 13
    """
    return SCHOOL_YEARS[year_level] # Returns year level as int.

###   ###   ----------------------------------------------------------------
###  APPLY DEFINED FUNCTIONS
#      Uses previously defined functions to clean input file
#      Applys: - format_date
#              - clean_school_name
#              - convert_level functions
def convert_census_record(fields, 
        functions=[format_date, clean_school_name, convert_level, int]):
    '''
    If the three functions are implemented correctly, this function
    must return the (required part of) school census record. 
    For example,
        ["20 February 2019","Amaroo School","Year 10","196"]
    will be converted into 
        ['2019', 'Amaroo School', 10, 196]
    '''
    return [ x[0](x[1]) for x in zip(functions, fields) ]

###   ###   ----------------------------------------------------------------
###  TASK 1D
###  RETURN YEAR
#      Returns integer year value from date string (YYYY)
def parse_year(dt):
    """
    Extract the year value from the date-time string used in
    the (ACT) population data, formatted as mm/dd/yyyy hh:mm:ss [AP]M
    Returns it as int
    For testing:
    parse_year('06/30/2015 12:00:00 AM') should be 2015
    parse_year('06/30/2020 11:59:59 PM') should be 2020
    """
    return dt.split('/')[2].split()[0] # Splits by / into 3 sections, then splits the 3rd section, and returns the first value of the 3rd section.
print(parse_year('06/30/2020 12:00:00 AM'))

###   ###   ----------------------------------------------------------------
###  TASK 2
###  ENROLMENT DATASET CONSTRUCTION
#      Reads in and cleans enrolment datafile, returning enrolment dataset
#      with four variables
#      Applys: - format_date
#              - clean_school_name
#              - convert_level
def read_enrolment_data(fname, dt=dt_census):
    """
    Reads a school enrolment census data file, extracts values for
    census date, (school) name, year-level and enrolment number, packs
    them into 4-tuple -- str (data formatted as YYYY-MM-DD, which is
    different from the format in the data file!), str, int, int -- and
    returns a list of those.
    """
    i = 0
    enrolment = []
    data = csv.reader(open(fname, newline=''), delimiter=',')
    for row in data:
        i += 1
        if i != 1: # Skips the column headers.
            if row[3] == "Older & Mature" or row[3] == "Mature": # Includes older & mature, and mature ages as older.
                row[3] = "Older"
            enrolment.append((format_date(row[0], False), clean_school_name(row[1]), convert_level(row[3]), row[4]))# Appends required tuple to a list 
                                                                                                                    # Cannot use convert_census_record as it always uses short date format
                                                                                                                    
    return enrolment 


###   ###   ----------------------------------------------------------------
###  TASK 3
#    ATTACH SCHOOLS TO SUBURBS
#      Match schools to suburbs
def get_suburb_schools(school_data, suburb):
    """
    As the function name says -- takes a sequence of all
    school data (returned by get_school_data) and retains those
    with matching suburb
    For testing: As these examples get more complex you'll want to
    familiarise yourself with the AI3_Tests.py file that contains
    several test cases that will be checked. For future questions, inspect
    those test cases. Ask your teacher if you're unsure what this means.
    """
    return schools

###   ###   ----------------------------------------------------------------
###  TASK 4
###  INPUT SUBURB LEVEL POPULATION
#      Population projections, by single year of age and
#      sex, need to be aggregated into suburb totals
def read_population_data(fname, ages_range=86):
    """
    Read population data file formatted as follows:
         datatime, suburb, female 0..85+ range, male 0..85+ range
    The data structure used is a dictionary:
         key: 2-tuple (suburb, year)
         value: list of 2-tuples (female, male) for age ranges 0..86
    """
    return pop_data

###   ###   ----------------------------------------------------------------
###  TASK 5    (1 Mark)
###  CREATE SUBURB POPULATION SET
#      Iterate through pop_data dictionary
#      creating a set up population estimates
#      for each suburb
def all_suburbs(pop_data):
    """
    Extracts suburbs from pop_data and returns them as a set
    """
    return suburbs

###   ###   ----------------------------------------------------------------
###  TASK 6    (2 Marks)
###  TOTAL SCHOOL ENROLMENT
#      Calculate school enrolment across
#      all year levels for required year
#      Average enrolments are calculated
def get_yearly_enrolment(enrolment, year, levels=[]):
    """
    Takes enrolment data (returned by the read_enrolment_data function)
    and returns a dictionary with keys being school names, and values being
    the enrolment numbers for the year of census totalled over year levels
    given by levels; if the census year has multiple data (eg, for
    February and August), a mean value of enrolment numbers for that year is
    used.
    """
    return output

########################################################################################################################
#                                   Part 2 - Data Manipulation
#                                           Task 7.
########################################################################################################################

###   ###   ----------------------------------------------------------------
###  TASK 7
#    COMBINE ENROLMENT AND POPULATION DATASETS
def enrolment_vs_population(enrolment,
                            schools,
                            population, 
                            year_level, 
                            year, delta=5):
    """Returns a list of 3-tuples -- (suburb, population, enrolment) --
    for year of census and year_level of schools (assuming that the 
    student age is year_level + delta)
    
    Parameters
    ----------
    enrolment : list of 4-tuples (year, name, year_level, enrolment)
                elements of which are (int, str, int, int)
                (alternatively, a 1-dim structured np.array with the fields
                'year', 'name', 'year_level', 'enrolment'; the 'year' field can 
                be either int or numpy.datetime64 value)
    schools : a list of 3-tuples, (str,str,str), or alternatively a
              1-d structured numpy array with dtype fields (st,str,str)
              a list (np.array) of all schools with (names, address, suburb)
    population : a dict keyed by (str,int) being ()'suburb', year), and values
                 being lists of 2-tuples, each tuple being (female,male) 
                 population numbers, and the list index being the age of 
                 population group (the last element being the age "maximal+", 
                 85+ in the provided data set)
    year_level : a list of int, 
                 representing the school year levels
    year : int, 
           the year of census data
    delta : int, optional (default=5) 
            relates the school year level and the standard student age
    
    Returns
    -------
    output : a list of 3-tuples (str, int, float) 
              the last component, enrolment, is float because it is a mean 
              value over possibly more that one (usually, two)
              census date for enrolment in a given year
    """
    return output
