import time
import pandas as pd
import numpy as np

"""Aim: We will learn about bike share use in Chicago, New York City, and Washington by computing a variety of descriptive statistics.
 I will Use Python, Pandas, NumPy, to explore US bikeshare data for three cities (Chicago, New York, and Washington) 
Name : Ahmad Aburrub
Project Name: Explore US Bikeshare Data
    """

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """Request from user to specify a city, month, and day in order to analyze
    Return Output:
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data")
    
    # Get the input for city (chicago, new york, washington). Use a while loop to handle invalid inputs.
    while True:
        city =input("Please enter one of the following cities you want to see data for:\n Chicago, New York,or Washington\n").lower()
        if city in cities:
            break
        else:
            print('Please enter valid city.')
            
    # Get user to filter by month, day, or none.
    while True:
        choice = input("Would you like to filter the data by month, day, or none?\n").lower()
        if choice == 'month':
            month = input("Please enter the month you want to explore. If you do not want a month filter enter 'all'. \nChoices: All, January, February, March, April, May, June\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month.')
        elif choice == 'day':
            day = input("Please enter the day of the week you want to explore. If you do not want to apply a month filter enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()#PB
            month = 'all'
            if day in days:
                break
            else:
                print('Please enter a valid day')
        elif choice == 'none':
            month = 'all'
            day = 'all'
            break
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Arguments:
        city - name of the city to analyze
        month - name of the month to filter by, or "all" to apply no month filter
        day - name of the day of week to filter by, or "all" to apply no day filter
    Return Output:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all': 
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """
    This method for time statistics
    """

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of the week, and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common month
    popular_month = df['month'].mode()[0]
    month_name = pd.Timestamp(f'2023-{popular_month}-01').strftime('%B')  # Get full month name
    print('Most Common Month:', month_name)

    # Display the most common day of the week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week:', popular_day)

    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    period = 'AM' if popular_hour < 12 else 'PM'
    formatted_hour = popular_hour if popular_hour == 12 or popular_hour == 0 else popular_hour % 12
    formatted_hour = 12 if popular_hour == 0 else formatted_hour  # Handle midnight as 12 AM
    print(f'Most Common Start Hour: {formatted_hour} {period}')

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    This menthod displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: \n", popular_start_station)
    
    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: \n", popular_end_station)
    
    # Display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] + " to " +  df['End Station']
    common_combo_station = combo_station.mode()[0]
    print("Most Common Trip from Start to End:\n {}".format(common_combo_station)) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum()
    hours, remainder = divmod(total_duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"The Total Travel Time is {hours} Hours, {minutes} Minutes, and {seconds} Seconds.")

    # Display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minutes, seconds = divmod(average_duration, 60)
    hours, minutes = divmod(minutes, 60) if minutes >= 60 else (0, minutes)

    if hours > 0:
        print(f'The Average Travel Time is {hours} Hours, {minutes} Minutes, and {seconds} Seconds.')
    else:
        print(f'The Average Trip Duration is {minutes} Minutes and {seconds} Seconds.')

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type:\n", user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(' ' * 40)
        print('Counts of Each User Gender:')
        print(gender)
    except:
        print('Counts of Each User Gender:\nSorry, no gender data available for {} City'.format(city.title()))
      
    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min() #Oldest birth year
        recent = df['Birth Year'].max() #Youngest birth Year
        common = df['Birth Year'].mode() #This gives the Common Birth Year 
        print(' ' * 40)
        print('Counts of User Birth Year:')
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    except:
        print('Counts of User Birth Year:\nSorry, no birth year data available for {} City'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_data(df):
    # Ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break
                    
def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))
        
        df = load_data(city, month, day)
        #print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
