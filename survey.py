# FUNCTIONS TO POPULATE DATA (RANDOMLY BUT REASONABLY)
import random
import pandas as pd

def randomize(n, start, end, probs = []):
    '''
    this function was used to populate age evenly
    and age_gap disproportionately (smaller age gap usually preferred).

    this function finds selects a random number from a range and repeats the trials n times.
    user can also define the probability array to define the weight of each number within the range.
    '''
    if not probs:
        return [random.randint(start, end) for _ in range(n)]
    
    else:
        return random.choices(range(start, end+1), weights = probs, k = n)
    
def populate_gender_pref(gender):
    preferences = list()
    for g in gender:
        if g == [1,0,0]:
            preferences.append([0,1,0])
        else:
            preferences.append([1,0,0])
        
    return preferences

def populate_interest(n, num_interest):
    ''' randomly populate interest arrays with varying scores -> uniform odds for liking/disliking each interest genre '''
    return [[random.randint(1,5) for i in range(num_interest)] for j in range(n)]

def populate_by_percentage(n):
    ''' randomly populate an array of scores ranging from 0% to 100% -> uniform odds for select each discrete percentage point (i.e. 1%, 2%, etc.)
    this is used for seriousness factor and can be also used for similarity preference field'''
    return [random.randint(0,100)/100 for i in range(n)]

def populate_similarity(n):
    ''' randomly populate an array of scores ranging from 0% to 100% but more weight is placed towards the higher percentages
    The rationale is that people are more likely to prefer similar partners in real life '''
    # this function increases the likelihood that people prefer more similar partners
    leftover = 100
    index = -1
    
    similarity = [0 for _ in range(101)]
    
    while leftover > 0:
        percent = random.randint(1, 3)
        
        # amount to allocate is more than leftover
        if percent > leftover:
            percent = leftover
        
        leftover -= percent
        similarity[index] = percent
        index -= 1
    
    return [x/100 for x in random.choices(range(0,101), weights = similarity, k = n)]

def populate_traits(n, choose, num_traits):
    ''' randomly populate traits array for every user. each user must select 10 out of 30 traits
    each trait has an equal chance of being selected. '''
    choices = choose # choose x from total number of traits
    
    traits = list()
    
    for i in range(n):
        trait = [0 for _ in range(num_traits)]
        
        while sum(trait) != choices:
            trait[random.randint(0, num_traits-1)] = 1
        
        traits.append(trait)

    return traits

def populate_ranking(n, num_ranking_choices):
    ''' users have 10 points to distribute across 3 factors:
        1. matching by interest
        2. matching by traits compatibility
        3. matching by seriousness compatibility
        
        users must use up the 10 points, each point correspond to a 10% weightage in that factor,
        all of the weights sum up to 100% or 1.
    '''
    total = 10 #distribute
    
    rankings = list()
    
    for i in range(n):
        leftover = total
        
        ranking = [0 for _ in range(num_ranking_choices)]
        
        while leftover > 0:
            ranking[random.randint(0, num_ranking_choices-1)] += 0.1
            leftover -= 1
        
        rankings.append(ranking)
    
    return rankings

def populate_budget(n):
    ''' randomly populate an array of budgets ranging from $0 to $100 but more weight is placed towards the lower end ranging $20 - $50
    as these are the common comfortable price range for most people '''
    
    values = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # $0 to $100
    weights = [0.02, 0.1, 0.2, 0.2, 0.2, 0.15, 0.07, 0.03, 0.01, 0.01, 0.01]

    return random.choices(values, weights = weights, k = n)
    
def populate_duration(n):
    ''' randomly populate an array of duration ranging from 1 to 12 hours but more weight is placed towards the lower end ranging 2 - 6 hours
    as these are the common comfortable dating duration for most people
    
    each person must have a minimum and a maximum duration desired, so these must be randomly populated in order'''
    
    values = range(1,13) # 1 to 12 hour durations
    weights = [0.15, 0.20, 0.15, 0.15, 0.15, 0.1, 0.05, 0.03, 0.02, 0.0, 0.0, 0.0]

    min_duration = [0 for _ in range(n)]
    max_duration = [0 for _ in range(n)]

    for i in range(n):
        min_value = random.choices(values, weights = weights)[0] # 1 choice only
        max_value = random.choices(values, weights= weights)[0] # 1 choice only

        if min_value > max_value:
            min_value, max_value = max_value, min_value # swap if max is smaller than min
        
        min_duration[i] = min_value
        max_duration[i] = max_value

    return min_duration, max_duration

def populate_distance(n):
    ''' randomly populate an array of distance ranging from 5 km to 50 km, this is uniformly distributed for all users'''

    return [random.randint(5, 51) for x in range(n)]

def populate_calendar(n):
    ''' randomly populate calendar matrix for every participant for the current week (7 days x 14 time slots)
        distribution assumption: people are busier during weekdays workhours
        people are free-er during weekends throughout
    '''
    # Each index represent 1 hour time slices (in 24-hour time format)
    # (0) 0800 - 0900 (1) 0900 - 1000 (2) 1000 - 1100 (3) 1100 - 1200 (4) 1200 - 1300
    # (5) 1300 - 1400 (6) 1400 - 1500 (7) 1500 - 1600 (8) 1600 - 1700 (9) 1700 - 1800
    # (10) 1800 - 1900 (11) 1900 - 2000 (12) 2000 - 2100 (13) 2100 - 2200

    calendar = [None for _ in range(n)]

    weekday_prob = [0.2, 0.2, 0.2, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.5, 0.6, 0.7, 0.7, 0.4]
    weekend_prob = [0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 0.7, 0.5]

    for index_p, p in enumerate(range(n)): # each participant
        week = [None for _ in range(7)]

        for index_d, d in enumerate(range(7)): # each day of the week
            day = [None for _ in range(14)]
            if index_d <= 4: # weekday
                for index_t, t in enumerate(range(14)): # for each time slice
                    odds = weekday_prob[index_t] # odds for current time slice
                    day[index_t] = random.choices([0,1], weights = [1-odds, odds])[0]

            else: # weekend
                for index_t, t in enumerate(range(14)): # for each time slice
                    odds = weekend_prob[index_t] # odds for current time slice
                    day[index_t] = random.choices([0,1], weights = [1-odds, odds])[0]
        
            week[index_d] = day
        
        calendar[index_p] = week
    
    return calendar


# RANDOM TRIAL: defining the variables

# REMINDER -> the matching problem is a NP-HARD problem with basically exponential complexity
# increase N at your own risk!
# largest I have tried (with NO GPU): 50

######################################### PROBLEM SIZE #########################################
n = 62 # number of participants
################################################################################################

def populate_data(n):

    num_ranking_choices = 3 # interest, traits, seriousness -> rank in order of preference
    num_interest = 8 # Adventure, Wellness, Sightseeing, Animals and Nature, Art and Culture, Food, Fitness, Recreational
    num_traits = 30 # TRAITS:
                    # Ambitious, Authentic, Caring, Cheerful, Committed
                    # Confident, Creative, Easy-going, Energetic, Funny
                    # Generous, Honest, Humble, Independent, Intelligent
                    # Kind, Loyal, Mature, Open-minded, Optimistic
                    # Outgoing, Patient, Practical, Respectful, Responsible
                    # Romantic, Social, Supportive, Thoughtful, Trustworthy.
    num_traits_to_choose = 10

    genders = [[1,0,0], [0,1,0]] # male | female | others
    gender_pref = [[1,0,0], [0,1,0], [0,0,1],
                   [1,1,0], [0,1,1], [1,0,1],
                   [1,1,1]] # no preference or [0,0,0] is not allowed

    gender_prob = [0.5, 0.5] # male | female | others

    # POPULATING THE DATA
    age = randomize(n, 19, 26) # ages of each participant
    gap = randomize(n, 0, 4, [0.1, 0.2, 0.4, 0.2, 0.1]) # maximum age gap for each participant
    gender = random.choices(genders, weights = gender_prob, k=n)
    preferences = populate_gender_pref(gender)
    interests = populate_interest(n, num_interest)
    seriousness = populate_by_percentage(n)
    similarity_pref = populate_similarity(n)
    rankings = populate_ranking(n, num_ranking_choices)
    traits = populate_traits(n, num_traits_to_choose, num_traits)
    traits_pref = populate_traits(n, num_traits_to_choose, num_traits)
    budget = populate_budget(n)
    min_duration, max_duration = populate_duration(n)
    max_distance = populate_distance(n)
    calendar = populate_calendar(n)
    
    return pd.DataFrame({'age': age,
                        'gap': gap,
                        'gender': gender,
                        'preferences': preferences,
                        'interests': interests,
                        'seriousness': seriousness,
                        'similarity_pref': similarity_pref,
                        'rankings': rankings,
                        'traits': traits,
                        'traits_pref': traits_pref,
                        'budget': budget,
                        'min_duration': min_duration,
                        'max_duration':max_duration,
                        'max_distance':max_distance,
                        'calendar': calendar})

print("POPULATING DATA...")
df = populate_data(n)

print(df)

df.to_csv("BC2410-student-survey.csv")

print("DATA GENERATED.")