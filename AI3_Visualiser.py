from AI3_Functions import *

if __name__ == '__main__':
    
    the_year = 2019
    try:
        the_year = int(sys.argv[1])
    except Exception as e:
        print(f'The usage: python3 {sys.argv[0]} year', end=' ')
        print(f'(no year provided, using the default value {the_year})')
    
    import matplotlib.pyplot as plt
    cm = plt.cm.get_cmap('jet')
    # import seaborn as sns
    # sns.set()
    plt.style.use('seaborn')
    school_data_file = "ACT_School_Locations_2017_-_archived.csv" 
    enrol_data_file  = "Census_Data_for_all_ACT_Schools.csv"
    pop_data_file    = "ACT_Population_Projections_by_Suburb__2015_-_2020_.csv" 
    school_data = get_school_data(school_data_file, dt=dt_school)
    enrolment   = read_enrolment_data(enrol_data_file, dt=dt_census)
    population  = read_population_data(pop_data_file, ages_range=86)
    
    age_group = JUNIOR_SCHOOL_AGES
    school_age_data = enrolment_vs_population(
                           enrolment,
                           school_data,
                           population, 
                           year_level=JUNIOR_SCHOOL_AGES,
                           year=the_year
                           )
    print(school_age_data)
    # retain only those suburbs where someone lives and goes to school
    school_age_data  = [e for e in school_age_data if e[1:] != (0,0)]
    pop_numbers  = [e[1] for e in school_age_data]
    enr_numbers  = [e[2] for e in school_age_data]
    diffs        = [(e[1] - e[2]) for e in school_age_data]
    mind, maxd = (min(diffs), max(diffs)) if diffs else (1,0)
    colours = [d//10 for d in diffs] # break into subgroups of one colour
    sizes = [abs(d)*500/(maxd - mind) for d in diffs] # set point sizes
    
    # plotting
    fig = plt.figure(figsize=(6,6))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    fig.subplots_adjust(hspace=0)
    fig.tight_layout()
    
    # for junior school ages
    g1 = ax1.scatter(pop_numbers, enr_numbers, c=colours, s=sizes, 
                                            alpha=.7, cmap=cm)
    ages = '-'.join([str(y) for y in [min(age_group), max(age_group)]])
    title = f'Population vs Enrolment in {the_year} for {ages} years olds'
    ax1.set_title(title, fontsize=12)
    max_p = max(pop_numbers) if pop_numbers else 100
    max_e = max(enr_numbers) if enr_numbers else 100
    ax1.set_xlim(-200, max_p + 300) # add h-space to avoid clipping
    ax1.set_ylim(-200, max_e + 300) # add v-space to avoid clipping
    # ax1.set_xticks([])
    ax1.set_ylabel('Suburb School Enrolment')
    fig.colorbar(g1, ax=ax1)
    
    # for secondary school ages
    age_group = SECONDARY_SCHOOL_AGES
    school_age_data = enrolment_vs_population(
                           enrolment,
                           school_data,
                           population, 
                           year_level=SECONDARY_SCHOOL_AGES,
                           year=the_year
                           )
    # retain only those suburbs where someone lives and goes to school
    school_age_data  = [e for e in school_age_data if e[1:] != (0,0)]
    pop_numbers  = [e[1] for e in school_age_data]
    enr_numbers  = [e[2] for e in school_age_data]
    diffs        = [(e[1] - e[2]) for e in school_age_data]
    mind, maxd = (min(diffs), max(diffs)) if diffs else (1,0)
    colours = [d//10 for d in diffs] # break into subgroups of one colour
    sizes = [abs(d)*500/(maxd - mind) for d in diffs] # set point sizes
    g2 = ax2.scatter(pop_numbers, enr_numbers, 
                c=colours, s=sizes, alpha=.7, cmap=cm)
    ages = '-'.join([str(y) for y in [min(age_group), max(age_group)]])
    title = f'Population vs Enrolment in {the_year} for {ages} years olds'
    ax2.set_title(title, fontsize=12)
    max_p = max(pop_numbers) if pop_numbers else 100
    max_e = max(enr_numbers) if enr_numbers else 100
    ax2.set_xlim(-200, max_p + 300) # add h-space to avoid clipping
    ax2.set_ylim(-200, max_e + 300) # add v-space to avoid clipping
    ax2.set_ylabel('Suburb School Enrolment')
    ax2.set_xlabel('Suburb Population for School Ages (in thousands)', fontsize=10)
    fig.colorbar(g2, ax=ax2)
        
    plt.show()

