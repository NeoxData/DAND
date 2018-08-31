import time
import pandas as pd
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def month_choice():
    #function used to get, check and transform data according to the needs
    month_dd= input('Which month are you interested? Jan, Feb, Mar, Apr, May, Jun\n')
    month_d=month_dd.title()
    while True:
       if month_d not in ['Jan','Feb', 'Mar', 'Apr','May','Jun']:
           print('Oups you did not write the correct short name of month. Please try again\n')
           month_d= input('Which month are you interested? Jan, Feb, Mar, Apr, May, Jun\n')
       else:
           break
    
    month_number={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6}
    month_choosen=month_number[month_d]
    return month_choosen


def day_choice():
    #function used to get, check and transform data according to the needs
    day_dd= input('Which day are you interested? Mo,Tu,We,Th,Fr,Sa,Su\n')
    day_d=day_dd.title()
    while True:
       if day_d not in ['Th','Fr', 'Sa', 'Su','Mo','Tu','We']:
           print('Oups you did not write the correct short name of days. Please try again\n')
           day_d= input('Which day are you interested? Mo,Tu,We,Th,Fr,Sa,Su\n')
       else:
           break
  
    day_number={'Mo':0,'Tu':1,'We':2,'Th':3,'Fr':4,'Sa':5,'Su':6}
    day_choosen=day_number[day_d]
    return day_choosen 
 
def display_data(city_data):
    #function to display raw data from selected city, month and day
    n=5
    i=0
    info = input('Would you like to see raw data? Enter Y or N\n')
    while True:
       if info.lower() not in ['y', 'n']:
           print('Oups you did not write the correct answer. Please try again\n')
           info= input('Would you like to see some raw data? Enter Y or N\n')       
       elif info.lower() == 'y': 
           print(city_data.iloc[i:n,:])
           n=n+5
           i=i+5
           info = input('Would you like to continue seeing raw data? Enter Y or N\n')         
       else:
            break

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #input of user selection for the data analysis. There is a check in case of invalid input
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city= input('Would you like to see data from Chicago(CCG), New York (NY) or Washington (WSG)? Please use only short name like NY\n')
    city=city.title()
    while True:
       if city not in ['Ccg','Ny', 'Wsg']:
        print('Oups you did not write the correct short name of the cities. Please try again\n')
        city= input('Would you like to see data from Chicago(CCG), New York (NY) or Washington (WSG)? Please use only short name like NY\n')
       else:
           break

     # get user input for day of week (all, monday, tuesday, ... sunday)
     # get user input for month (all, january, february, ... , june)

    filter_choice= input ('Would you like to filter the data by month, day or both or not at all. Please type all for no time filter\n')
    while True:
       if filter_choice.title() not in ['Month','Day', 'Both', 'All']:
            print('Oups you did not write the correct selection. Please try again\n')
            filter_choice= input ('Would you like to filter the data by month, day or both or not at all. Please type all for the latter\n')
       else:
           break

    if filter_choice == 'month':
        month_decided=month_choice()
        day_decided='all'
    elif filter_choice =='day':
        day_decided=day_choice()
        month_decided='all'
    elif filter_choice == 'both':
        day_decided=day_choice()
        month_decided=month_choice()
    else :
        month_decided = 'all'
        day_decided= 'all'

    print('-'*40)
    
    return city, month_decided, day_decided


def load_data(city, month1, day1):
    #change month variable to month1 (same for day) to avoid any misunderstanding in the code further down
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city=='NY':
        city_name = 'new york city'
    elif city=='CCG':
        city_name='chicago'
    else:
        city_name='washington'
    
    df= pd.read_csv(CITY_DATA[city_name])
    
    #change format of Start time column in order to select month, weekday and hour in new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour
    
    #dataframe build depending on user criteria
    if (month1!='all' and day1 =='all'):
        return df[df['month'] == month1]
    elif (day1!='all' and month1 =='all'):
        return df[df['weekday'] == day1]
    elif (month1!='all' and day1!='all'):
        df1= df[df['month'] == month1]
        df2=df1[df1['weekday'] == day1]
        return df2
    else:
        return df  
          

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month= df['month'].mode()[0]
    print('The most common month is ', popular_month)

    # display the most common day of week
    popular_day=df['weekday'].mode()[0]
    print('The most popular day of the week is:', popular_day)

    # display the most common start hour
    popular_hour=df['start_hour'].mode()[0]
    print('The most popular start hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation=df['Start Station'].mode()[0]
    print('The most popular start station is:\n', popular_startstation)

    # display most commonly used end station
    popular_endstation=df['End Station'].mode()[0]
    print('The most popular end station is:\n', popular_endstation)

    # display most frequent combination of start station and end station trip
    subset = df[['Start Station','End Station']]
    station_tuples = [tuple(x) for x in subset.values]
    counts = Counter(x for x in station_tuples)
    popular_combstation=counts.most_common()[0]
    
   #Reference for the combination part:
   #https://codereview.stackexchange.com/questions/118914/word-frequency-counter
   #https://stackoverflow.com/questions/9758450/pandas-convert-dataframe-to-array-of-tuples

    print('The most popular combination of station is:\n', popular_combstation)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time(travel time =tt)
    Totaltt= df['Trip Duration'].sum()
    print('The total travel time is: ', Totaltt)
    # display mean travel time
    Meantt= df['Trip Duration'].mean()
    print('The mean travel time is: ', Meantt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print ('User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print ('Gender:\n', gender)
    else:
        print('No gender stats to display')
    
        

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth = df['Birth Year'].mode()[0]
        r_birth= df['Birth Year'].min()
        e_birth= df['Birth Year'].max()
        print ('Most popular year of birth\n', birth)
        print('Most recent year of birth\n', r_birth)
        print('Earliest year of birth\n', e_birth)
    else:
        print('No birth year stats to display')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #display raw data (5 lines by 5) as an option according to the city, month and day selected previoulsy
    display_data(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
