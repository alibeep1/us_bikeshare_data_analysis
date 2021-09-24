import time
import datetime as dt
import pandas as pd
import numpy as np
# list that acts as my 'repository' for months and days
CITY_DATA = { 'chicago': 'chicago.csv', 'washington': 'washington.csv',
              'new york city': 'new_york_city.csv'
               }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hey there! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Please choose a city: Chicago, Washington, New York City\n').lower()
            if city in CITY_DATA.keys():
                break
        except ValueError:
            print('Didn\'t get that, please choose a country by entering its name\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            print()
            month = input('Please choose a month by typing it, or just type "all" to not apply a month filter: ').lower()
            if month in months or month =='all':
                break
        except ValueError:
            print('Did not get that, please select a proper month between Jan and June')



    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            print()
            day = input('For what day would you like to filter the data (type "all" for no filters)\n').lower()
            if day in days or day == 'all':
                break
        except:
            print('Kindly, select an appropriate weekday\n')

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

    # extracting the month's name; not as an integer
    df['month'] = df['Start Time'].dt.month_name()

    # extracting the day's name; not as an integer
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        """

        # use the index of the months list to get the corresponding int
        # months = ['january', 'february', 'march', 'april', 'may', 'june']
        # month = months.index(month) + 1

        ----------------------------------------------------

        I replaced the above method by since I am storing the months in my dataframe as month names (strings) not as integers anymore

        I will use the name of the month as the index as opposed to its integer value
        """

        # filter by month to create the new dataframe

        df = df[df['month'] == month.title()]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for {} ...\n'.format(city.title()))
    start_time = time.time()

    common_month = df['month'].mode()[0]
    # TO DO: display the most common month
    print('The most busy month is {}\n'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most busy day is {}\n'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = dt.timedelta(hours = int(df['Start Time'].dt.hour.mode()[0]))

    print('Seems like the rush hour occurs at {}\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip for {}...\n'.format(city.title()))
    start_time = time.time()

    # TO DO: display most commonly used start station
    busiest_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is ', busiest_start_station)

    # TO DO: display most commonly used end station
    busiest_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ', busiest_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    busiest_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print('The most frequently occurring combo of start/end destinations are: ', ' PLUS '.join(busiest_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Durations for {}...\n'.format(city.title()))
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time = dt.timedelta(seconds = int(df['Trip Duration'].sum()))
    print('Total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = dt.timedelta(seconds = int(df['Trip Duration'].mean()))
    print('Mean travel time: ', mean_travel_time,' (HH:MM:SS)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for {}...\n'.format(city.title()))
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts().count()
    print('Types of user accounts: ', user_types_count)
    print()
    # TO DO: Display counts of gender
    # since the Gender and Birth Year columns do not exist in the washington dataframe, we must check their existence!

    if 'Birth Year' in df.columns and 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Gender count:\n', gender_count)
        print()
    else:
        print('the column {} does not exist for {}!'.format('Gender', city.title()))

    # TO DO: Display earliest, most recent, and most common year of birth

    # I handle the errors that appear due to the absence of the birth year and gender columns in washington.csv, which was causing an undefined error using try and except and the if-else statements!
    try:
        earliest_birthdate = df['Birth Year'].min()
        latest_birthdate = df['Birth Year'].max()
        most_popular_birthdate = df['Birth Year'].mode()[0]
        today = dt.date.today().year
        print('The earliest birthday, the eldest person, was born on ', earliest_birthdate, ' making them over {} years old!'.format(today - earliest_birthdate))
        print('The latest birthday occurs on ', latest_birthdate, ' making them just {} years old!'.format(today - latest_birthdate))
        print('The most popular birthday is ', most_popular_birthdate, ' making them {} years old'.format(today - most_popular_birthdate))

    except:
        print('the column {} does not exist for {}!'.format('Birth Year', city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):

    counter = 1
    while True:
        raw_input = input('Would you like to see 5 data rows?\n').lower()
        if raw_input == 'yes':
            print(df[counter:counter+5])
            counter = counter + 5

        else:

            break

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)
        time.sleep(1)
        time_stats(df, city)
        time.sleep(2)
        station_stats(df, city)
        time.sleep(2)
        trip_duration_stats(df, city)
        time.sleep(2)
        user_stats(df, city)
        time.sleep(2)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
