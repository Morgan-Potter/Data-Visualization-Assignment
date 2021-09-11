import pytest

import numpy as np
from io import StringIO
from AI3_Functions import *

@pytest.mark.parametrize("name", [
    'Garran Primary,Gilmore Crescent,Garran,Government,Primary School,"(-35.344681, 149.103287)"',
    'School of Hard Knocks,Neverland,Discworld,Ministry of Magic,High School,'
    ])
def test_get_school_data(name):    
    data = get_school_data(name)
    if type(data) is list:
        expected = [('Garran Primary', 'Gilmore Crescent', 'Garran'), ('School of Hard Knocks', 'Neverland', 'Discworld')]
    elif type(data) is np.ndarray:
        for adatum, edatum in zip:
            assert adatum['name'] == edatum[0]
            assert adatum['address'] == edatum[1]
            assert adatum['suburb'] == edatum[2]



def test_format_date():
    assert(str(format_date('21 February 2018', False)) == '2018-02-21')
    assert(str(format_date('20 February 2019')) == '2019')


@pytest.mark.parametrize('test_input,expected',
                      [('The Woden School', 'Woden School'),
                       ('Canberra College, The', 'Canberra College')])
def test_clean_school_name(test_input, expected):
    assert clean_school_name(test_input) == expected


@pytest.mark.parametrize('test_input,expected',
                      [('Year 11', 11),
                       ('Kindergarten', 0),
                       ('Preschool', 0),
                       ('Older', 13)])
def test_convert_level(test_input, expected):
    assert convert_level(test_input) == expected


@pytest.mark.parametrize('test_input,expected',
      [(["20 February 2019","Amaroo School","Year 10","196"],
       ['2019', 'Amaroo School', 10, 196])])
def test_convert_census_record(test_input, expected):
    assert convert_census_record(test_input) == expected
    
@pytest.mark.parametrize('test_input,expected',
                      [('06/30/2015 12:00:00 AM', 2015),
                       ('06/30/2020 11:59:59 PM', 2020)])
def test_parse_year(test_input, expected):
    assert parse_year(test_input) == expected


def test_read_enrolment_data():
    """docstring for test_read_enrolment_data"""
    pass


def test_get_yearly_enrolment():
    schools = [
        ('2009-01-01', 'Ainslie School',  1,  46),
        ('2015-01-01', 'Ainslie School',  1,  52),
        ('2011-01-01', 'Amaroo School',  6, 116),
        ('2011-01-01', 'Aranda Primary School',  3,  57),
        ('2013-01-01', 'Bonython Primary School',  3,  47),
        ('2014-01-01', 'Mount Stromlo High School', 10, 176),
        ('2011-01-01', 'Yarralumla Primary School',  2,  31)
    ]
    # schools = np.asarray(schools, dtype=dt_census)
    res = get_yearly_enrolment(schools, 2011, [2,3])
    assert res['Aranda Primary School'] == 57.0
    assert res['Yarralumla Primary School'] == 31.0
    assert res['Mount Stromlo High School'] == 0


def test_get_suburb_schools():
    schools = [
         ('Gold Creek School', 'Kelleway Street', 'Nicholls'),
         ('Lyneham Primary', 'Hall Street', 'Lyneham'),
         ("O'Connor Cooperative School", 'MacPherson Street', "O'Connor"),
         ('Garran Preschool', 'Robson Street', 'Garran'),
         ('Garran Primary', 'Gilmore Crescent', 'Garran'),
         ('Holy Trinity Primary', 'Theodore Street', 'Curtin'),
         ("St's Peter & Paul", 'Wisdom Street', 'Garran')
    ]
    # schools = np.asarray(schools, dtype=dt_school)
    res = get_suburb_schools(schools, 'Garran')
    expected = [('Garran Preschool', 'Robson Street', 'Garran'),
                ('Garran Primary', 'Gilmore Crescent', 'Garran'),
                ("St's Peter & Paul", 'Wisdom Street', 'Garran')]
    # expected = np.asarray(expected, dtype=dt_school)
    assert len(res) == len(expected)
    for r,e in zip(res,expected):
        assert r == e


def test_all_suburbs():
    fname = 'ACT_Population_Projections_by_Suburb__2015_-_2020_.csv'
    population = read_population_data(fname)
    suburbs = all_suburbs(population)
    assert len(suburbs) == 110
    assert 'Yarralumla' in suburbs
    assert 'Kensington' not in suburbs


def test_read_population_data():
    """docstring for test_read_population_data"""
    pass
    

def test_enrolment_vs_population():
    """docstring for test_enrolment_vs_population"""
    pass

