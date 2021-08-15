import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITY_NAMES_LIST = [key.title() for key in CITY_DATA.keys()]
CITY_NAMES = ' ,'.join(CITY_NAMES_LIST)
VALID_TIME_UNITS = ['Month', 'Day', 'Nal']
VALID_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
VALID_DAYS = {'1': 'Mon', '2': 'Tue', '3': 'Wed', '4': 'Thur', '5': 'Fri', '6': 'Sat', '7': 'Sun'}


def get_single_filter(filter_message, filter_type, valid_filter_items):
    """
    Captures a valid input from a terminal for the given filter type and validates the same

    Args:
        (str) filter_message : The message used to prompt the user to choose a filter
        (str) filter_type : The type of filter ( month, day etc)
        (iter) valid_filter_items : valid filter values to validate user input
    Returns:
        (str) filtered_field : The filtered value captured from user
    """
    filter_field = None
    while True:
        filtered_field = input(filter_message)
        if filtered_field.title() not in valid_filter_items:
            print("Sorry , that was an incorrect {} . Try again ".format(filter_type))
            print()
        else:
            break
    print()
    return filtered_field


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = None, None, None
    print('Hello! Let\'s explore some US bikeshare data!')

    city_message = "Select the city for which  you would like to see the data --> {} : ".format(CITY_NAMES)
    time_units_message = "Would you like to filter by Month, Day or Not at All ?" \
                         "Type 'NAL' if no time filters are needed : "
    months_message = "Please enter the complete month name from -> {} : ".format(" ,".join(VALID_MONTHS))
    days_message = "Please enter the day of the week as a number : (1, Monday) , (2, Tuesday) . . : "

    city = get_single_filter(city_message, 'city', CITY_NAMES_LIST)
    time_unit = get_single_filter(time_units_message, 'time_unit', VALID_TIME_UNITS)
    if time_unit.title() == 'Month':
        month = get_single_filter(months_message, 'Month', VALID_MONTHS)
    elif time_unit.title() == 'Day':
        day = get_single_filter(days_message, 'Day', VALID_DAYS)

    print('-'*40)
    return city, month, day


def load_raw_data_for_user(df: pd.DataFrame):
    """
        Displays 5 rows from the input dataframe sequentially based on user choice
    """
    i = 0
    len_df = len(df)
    while True:
        print_raw_data = input("\nWould you like to view original trip data? Type 'yes' or 'no' :\n")
        if print_raw_data.lower() == 'yes' and i < len_df:
            print(df[i: i+5].to_string())
            print()
            i += 5
        else:
            break


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    # add 1 to account for zero based indexing of 'day' : 0-Mon, 1-Tue . .
    df['Day_of_week'] = df['Start Time'].dt.dayofweek + 1

    if month:
        month_num = (VALID_MONTHS.index(month.title()) + 1)
        df = df[(df['Month'] == month_num)]
    if day:
        day_num = int(day)
        df = df[(df['Day_of_week'] == day_num)]
    return df


def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel.
        Args:
            (pd.DataFrame) df : The df on which analysis will be performed
        Returns:
            None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour_of_day'] = df['Start Time'].dt.hour

    # display the most common month, day_of_week and hour_of_day
    most_common_month = df['Month'].mode()
    most_common_day = df['Day_of_week'].mode()
    most_common_hour = df['hour_of_day'].mode()

    # get the most common day and month names for printing from their numeric indices
    val_most_common_month = VALID_MONTHS[most_common_month[0] - 1]
    val_most_common_day = VALID_DAYS[str(most_common_day[0])]
    val_most_common_hour = most_common_hour[0]

    count_common_month = df[(df['Month'] == most_common_month[0])]['Month'].count()
    count_common_day = df[(df['Day_of_week'] == most_common_day[0])]['Day_of_week'].count()
    count_common_hour = df[(df['hour_of_day'] == most_common_hour[0])]['hour_of_day'].count()

    print(" Most common month of travel is : {}  with count : {} ".format(val_most_common_month, count_common_month))
    print(" Most common travel day  of week is : {} with count : {} ".format(val_most_common_day, count_common_day))
    print(" Most common travel start hour of day is : {} with count : {}".format(val_most_common_hour, count_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel.
        Args:
            (pd.DataFrame) df : The df on which analysis will be performed
        Returns:
            None
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Journey_end_points'] = "FROM : [" + df['Start Station'] + "] TO : [" + df['End Station'] + "]"


    # display most commonly used start station
    start_stn_agg_count = df['Start Station'].value_counts(ascending=False).head(1)
    freq_start_stn = start_stn_agg_count.index.tolist()[0]
    freq_start_stn_count = start_stn_agg_count[0]
    print(" Most common start station is : '{}' with count : {}".format(freq_start_stn, freq_start_stn_count))

    # display most commonly used end station
    end_stn_agg_count = df['End Station'].value_counts(ascending=False).head(1)
    freq_end_stn = end_stn_agg_count.index.tolist()[0]
    freq_end_stn_count = end_stn_agg_count[0]
    print(" Most common end station is : '{}' with count : {}".format(freq_end_stn, freq_end_stn_count))

    # display most frequent combination of start station and end station trip
    journey_agg_count = df['Journey_end_points'].value_counts(ascending=False).head(1)
    frequent_journey_stations = journey_agg_count.index.tolist()[0]
    frequent_journey_stn_count = journey_agg_count[0]
    print(" Most frequent combination of starting and ending stations is  : '{}' with count : {}"
          .format(frequent_journey_stations, frequent_journey_stn_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel.
        Args:
            (pd.DataFrame) df : The df on which analysis will be performed
        Returns:
            None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_trip_duration_seconds = df['Trip Duration'].sum()
    avg_trip_duration_seconds = df['Trip Duration'].agg('mean')

    # display total travel time
    print(" Total duration of all trips in hours is : {}".format(round(total_trip_duration_seconds / 3600, 3)))

    # display mean travel time
    print(" Average duration of all trips in minutes is : {}".format(round(avg_trip_duration_seconds / 60, 3)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel.
        Args:
            (pd.DataFrame) df : The df on which analysis will be performed
        Returns:
            None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(" The distribution of different user types is : \n", df['User Type'].value_counts(), '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_ser = df['Gender'].fillna('Not available')
        print(" The distribution of Gender is : \n", gender_ser.value_counts(), '\n')
    else:
        print("No gender data to display ")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(" The most recent date of birth is : ", df['Birth Year'].max())
        print(" The earliest date of birth is : ", df['Birth Year'].min())
        print(" The most common date of birth is : ", df['Birth Year'].mode()[0])
    else:
        print("No birth data to display ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print("Filters -> city : {}, month: {}, day: {}".format(city, month, day and VALID_DAYS[day]))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        load_raw_data_for_user(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
