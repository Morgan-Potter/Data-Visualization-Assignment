"""
The following is a customised version of ANUs Intro to Data Science course.

Completed by Morgan Potter.
"""

# Questions:
# In task 2, are the tuples meant to include: the full date, including the month, or just the year. 
# In task 6, what exactly is meant to be the output? From the descriptions I have gathered it is meant to output a dictionay, the keys being the school name and the values being the average enrolment of all months in one year, totalled across the school levels chosen. 

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
                output.append((name, address, suburb)) # append the constructed 3-tuple (I believe adding clean_school_name to name would make the output more accurate)
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
        if len(str(MONTHS[s[1]])) < 1:        #   Checks to see if a 0 is needed at the start of the int month.
            s[1] = str(MONTHS[s[1]])          #   Changes the month to int. 
        else:
            s[1] = str(0) + str(MONTHS[s[1]]) #   Changes the month to int and adds a 0 to the start
        return s[2] + '-' + s[1] + '-' + s[0] #   Adds dashes
    else:
        return s[2] # Returns the year.

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
    sname = sname.replace('The ', '')  # Removes 'The ' in the school name.
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
    return int(dt.split('/')[2].split()[0]) # Splits by / into 3 sections, then splits the 3rd section, and returns the first value of the 3rd section as an int. 

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
    # Creates required variables
    enrolment = []                                                                     
    data = csv.reader(open(fname), delimiter=',')
    next(data) # Skips the column headers

    for row in data:

        # Skips the column headers.
        if row[3] == "Older & Mature" or row[3] == "Mature": # Includes older & mature, and mature ages as older.
            row[3] = "Older"

        # Appends required tuple to a list
        enrolment.append((format_date(row[0], False), clean_school_name(row[1]), convert_level(row[3]), float(row[4])))  

    return enrolment 

    # MY ATTEMPT AT AVERAGING ALL RE-OCCURING ENROLMENT DATA (I read output in task 7 wrong)

    # schools = set()
    # levels = set()
    # year_total = 0
    # occurences = 0
    # counter = 0
    
    # data = list(csv.reader(open(fname), delimiter=','))
    #  # Skips the column headers.

    # for row in data:
    #     counter += 1
    #     if counter > 1:
    #         if row[3] == "Older & Mature" or row[3] == "Mature": # Includes older & mature, and mature ages as older.
    #             row[3] = "Older"
    #         schools.add(row[1])
    #         levels.add(row[3])

    # counter = 0
    # print(len(schools) * len(levels))
    # for school in schools:
    #     for year_level in levels:
    #         for year in range(2009, 2019):
    #             for row in data:
    #                 counter += 1
    #                 if counter > 1:
    #                     if year == int(format_date(row[0])) and year_level == row[3] and school == row[1]:
    #                         year_total += int(row[4])
    #                         occurences += 1
    #              if occurences > 0:
    #                 mean_enrolment = year_total / occurences
    #                 enrolment.append((format_date(row[0], False), school, year_level, mean_enrolment))# Appends required tuple to a list 
    #              year_total = 0
    #              occurences = 0
    #              counter = 0          


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
    # Creates required variables
    schools = []
    
    # Loops over what is returned from get_school_data
    for tuples in school_data:
        if tuples[2] == suburb: # If the school is in the provided suburb
            schools.append(tuples) # Append the tuple to a list
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
    # Creates required variables
    pop_data = {}
    data = csv.reader(open(fname), delimiter=',')

    next(data) # Skips the colunm headers

    for row in data:

        # Adds keys to the dictionary, and sets the values to an empty list.
        pop_data[(row[1].strip(), parse_year(row[0]))] = []

        # Iterates over all ages in the age range (data starts at position 2)
        for age in range(2, ages_range + 2):
            pop_data[(row[1].strip(), parse_year(row[0]))].append((row[age], row[age + ages_range])) # Appends the female and male ages to the previously created empty list values.

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
    # Creates required variables
    suburbs = set()

    # Loops over every key in the population data and adds every suburb (key[0]).
    for key in pop_data:
        suburbs.add(key[0])
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
    # Creates required variables
    months = 0
    year_total = 0 
    output = {}

    # Adds all schools to the output dictionary
    for tuples in enrolment:
        output[tuples[1]] = 0
    
    # Loops over enrolment with every possible combination of school and year level.
    for school in output:
        for year_level in levels:
            for tuples in enrolment:
                if int(tuples[0].split('-')[0]) == year and tuples[2] == year_level and tuples[1] == school: # If it is the correct year, year level, and school.
                    # Adds to the variables needed for averaging
                    months += 1
                    year_total += tuples[3]
            if months != 0: # If there was data obtained from the year level
                output[school] += (year_total / months) # Append the average of that year levels data to the school
            # Resets the required variables
            months = 0
            year_total = 0
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
    # THIS ASSUMES YEAR LEVEL IS GRADE AND ONLY USES SUBURBS FROM POPULATION (accurate to the example)

    # Creates required variables
    pop_value = 0
    output = []
    suburb_enrolment = 0
    enrolment = get_yearly_enrolment(enrolment, year, year_level) # Provides function student age instead of student year level.
    suburbs = all_suburbs(population)

    # The main loop - loops over every suburb
    for suburb in suburbs:

        # Adds all needed enrolment data for each suburb together.
        for school in enrolment:
            for tuple in get_suburb_schools(schools, suburb):
                if school == tuple[0]:                           # Checks if the school is in the current suburb.
                    suburb_enrolment += enrolment[school]        # Adds enrolment numbers for each school in one suburb together.

        # Adds all needed population data for each suburb together.
        for key in population:                                                                             # Loops over all keys in the population dictionary
            if year == key[1] and suburb == key[0]:                                                        # If the year is the same as the supplied and if it is the current suburb -
                for pop_year in range(len(population[key])):                                               # Loops over the population data years.
                    if pop_year - delta in year_level:                                                     # If the current school year level (should be age level) is a provided age level -
                        pop_value += int(population[key][pop_year][0]) + int(population[key][pop_year][1]) # Add the female and male population data to the suburb total.

        output.append((suburb, pop_value, suburb_enrolment)) # Appends the created values to output
        # Resets required variables
        pop_value = 0
        suburb_enrolment = 0

    return output

    # THIS ASSUMES YEAR LEVEL IS AGE AND USES SUBURB DATA FROM POPULATION AND SCHOOLS (may be more accurate than example)

    # Converts the student ages in year_level to student grade in grade_levels
    # grade_level = []
    # for level in year_level:
    #     grade_level.append(level - delta)

    # Adds every suburb from schools / get_school_data, and population / get_population_data into a list.
    # suburbs = all_suburbs(population)
    # for tuple in schools:
    #     suburbs.add(tuple[2])

    # Creates required variables
    # pop_value = 0
    # output = []
    # enrolment_num = 0
    # enrolment = get_yearly_enrolment(enrolment, year, grade_level)
    # suburbs = all_suburbs(population)

    # for suburb in suburbs:

    #     for key in enrolment:
    #         for school in get_suburb_schools(schools, suburb):
    #             if key == school[0]:
    #                 enrolment_num += enrolment[key]

    #     for key in population:
    #         if year == key[1] and suburb == key[0]:
    #             for pop_year in range(len(population[key])):
    #                 if pop_year in year_level:
    #                     pop_value += int(population[key][pop_year][0]) + int(population[key][pop_year][1])

    #     output.append((suburb, pop_value, enrolment_num))
    #     pop_value = 0
    #     enrolment_num = 0

    # return output
