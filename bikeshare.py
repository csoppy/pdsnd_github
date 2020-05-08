import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
allstr = ['all']



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    If user gives unexpected input, repeat the options.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    city = input('Which city are you interested in: Chicago, New York City or Washington?\n').lower()
    while city not in (CITY_DATA):
        city = input('Please choose from this list: Chicago, New York City or Washington.\n').lower()
    print('The city you chose is: ' + city.title())

    # get user input for month (all, january, february, ... , june)
    month = input('Which month(s) are you interested in: all, January, February, March, April, May or June?\n').lower()
    while month not in (months) and month not in (allstr):
        month = input('Please choose from this list: all, January, February, March, April, May or June.\n').lower()
    print('The month you chose is: ' + month.title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day(s) are you interested in: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n').lower()
    while day not in (days) and day not in (allstr):
        day = input('Please choose from this list: all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.\n').lower()
    print('The day you chose is: ' + day.title())

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """
    Displays statistics on the most frequent times of travel:
     - the most common month
     - the most common week
     - the most common start hour 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is:", calendar.month_name[most_common_month])

    # display the most common day of week
    most_common_week = df['day_of_week'].value_counts().idxmax()
    print("The most common week is:", most_common_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:", most_used_start_station)

    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is:", most_used_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip is:\n', most_frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time= df['Trip Duration'].sum()
    print('Total travel time is:', total_travel_time)

    # display mean travel time
    mean_travel_time= df['Trip Duration'].mean()
    print('Mean travel time is:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', counts_of_user_types, '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print('Counts of genders:\n', counts_of_gender, '\n')
    else:
        print('The Washington database doesn\'t have gender data.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth is:', earliest_yob)
    else:
        print('The Washington database doesn\'t have birth year data.')

    if 'Birth Year' in df.columns:
        most_recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is:', most_recent_yob)

    if 'Birth Year' in df.columns:
        most_common_yob = df['Birth Year'].mode()[0]
        print('The most common year of birth is:', most_common_yob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def show_raw_data(df):
    i = 0
    answer = input('Would you like to see the raw data? (yes/no) ')
    if answer.lower() == "yes":
        while True:
            print(df.iloc[i:i+5, :])
            i += 5
            more = input('Would you like to see 5 more lines of data? (yes/no) ')
            if more.lower() != 'yes':
                break
        print("Okay, I'll stop showing you raw data now.")



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? (yes/no)\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
