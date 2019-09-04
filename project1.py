import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
        
  
    selected_city = ""

    while selected_city not in ['chicago', 'new york city', 'washington']:
            city = input("Select one city from Chicago, New York City and Washington\n").lower()
            if city in ['chicago', 'new york city', 'washington']:
                selected_city = city
                print('You selected: {}'.format(city))
            else:
                print('\n'+"Invalid city name. Please try again.")
    
    
    selected_month = ""

    while selected_month not in ['january','february','march','april','may','june','all']:
            
            month = input("Select month range: All, January, February, March, April, May, June\n").lower()
            if month in ['january','february','march','april','may','june','all']:
                selected_month = month
                print('You selected: {}'.format(month))
            else:
                print('\n'+"Invalid month range. Please try again.")


    selected_day = ""

    while selected_day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:

        day = input("Select day range: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
        if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            selected_day = day
            print('You selected: {}'.format(day))
        else:
            print('\n'+"Invalid day range. Please try again.")

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
    file = CITY_DATA.get(city,"")
    df = pd.read_csv(file)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    months = ['january','february','march','april','may','june']

    if month != 'all':
        df = df[ df['Start Time'].dt.month == (months.index(month) + 1)]    
    if day != 'all':
        df = df[df['Start Time'].dt.weekday_name == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].value_counts().idxmax()
    months = ['January','February','March','April','May','June']
    print('Most common month: {}'.format(months[popular_month - 1]))


    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_dayofweek = df['day_of_week'].value_counts().idxmax()
    print('Most common day of week: {}'.format(popular_dayofweek))


    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('Most common start hour: {}:00 hrs'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    start_stations = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station: {}'.format(start_stations))


    end_stations = df['End Station'].value_counts().idxmax()
    print('Most commonly used end station: {}'.format(end_stations))


    df['combined_stations'] = df['Start Station'] + ' and ' + df['End Station']
    combined_stations = df['combined_stations'].value_counts().idxmax()
    print('Most frequent combination of start station and end station trip: {}'.format(combined_stations))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total = int(round(df['Trip Duration'].sum()/3600))
    print('Total travel time: {} hrs'.format(total))

    
    mean = int(round(df['Trip Duration'].mean()/60))
    print('Mean travel time: {} min'.format(mean))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    unique_user_types = df['User Type'].unique()
    
    for types in unique_user_types:
        usertype_count = len(df[df['User Type'] == types])
        if types is not np.nan:
            print('Counts of {} types: {}'.format(types,usertype_count))

    if 'Gender' and'Birth Year' in df.columns:
        gender = df['Gender'].unique()

        for x in gender:
            gender_count = len(df[df['Gender'] == x])
            if x is not np.nan:
                print('{} count: {}'.format(x,gender_count))


        earliest = df['Birth Year'].min()
        print('Earliest birth year: {}'.format(earliest.astype(int)))

        most_recent = df['Birth Year'].max()
        print('Most recent birth year: {}'.format(most_recent.astype(int)))
        
        most_common = df['Birth Year'].value_counts().idxmax()
        print('Most common birth year: {}'.format(most_common.astype(int)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to view full data? Enter yes or no.\n')
        if raw_data.lower() != 'no':
            print(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
