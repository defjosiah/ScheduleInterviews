import csv

#Josiah Grace
#O-Week 2014 Scheduling


"""
Interview Scheduler

    (Optional) 
        Access the Google Docs API in order to download the CSV
        files from the duncaroos@gmail folder.

    a. Transform from CSV into acceptable interview format
    b. Accept different interview blocks for coordinators 
    (e.g. 15 minutes w/ 5 minute breaks)
    c. Turn candidate preferences into acceptable interview
    times

    (Optional)
        Turn back into Google Doc spreadsheet

"""

# (date) : [(start, end),(start, end)]
# TODO: remove hard-coded form of coord_avail
coord_avail = { 
        ('Fri  14th') : [(15.0, 18.0)],
        ('Sat  15th') : [(10.0, 19.0)],
        ('Sun  16th') : [(10.0, 14,0), (19.0, 21.0)],
        ('Fri  21st') : [(15.0, 20.0)],
        ('Sat  22nd') : [(10.0, 19.0)],
        ('Sun  23rd') : [(10.0, 14,0), (19.0, 21.0)]
    }

def parse_csv(filename):
    """
    Input: .csv filename string
    Parse input into list of available times
    Return: dictionary mapping
        (name) : {(date) : excluded_times (start, end)}
    ______________________________________________________
    CSV Format (Google spreadsheet): 
        Name date1                     date2        date3
        a    start1 end1 start2 end2   ...          ...
        b
        c 
    ______________________________________________________
    """
    name_exclude = {}
    dates = []
    with open(filename, 'rb') as csvfile:
        schedule_reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(schedule_reader):
            if(i == 0):
                dates = row[1::]
            else:
                exclude = {}
                for j, date in enumerate(dates):
                    no_work = row[j+1].split()
                    temp = []
                    for k in range(0, len(no_work), 2):
                        temp.append((float(no_work[k]), float(no_work[k+1])))
                    exclude[date] = temp
                name_exclude[row[0]] = exclude
    return name_exclude

def coordinator_availability(pattern):
    """
    Input: 
        pattern - tuple of (interview length, break) in min
        coord_avail - global dict mapping dates to availability (hours)
        (date) : [(start, end), (start,end)]
    
    Returns: block_avail - split the interview availability into 
    pattern specific block, output is dictionary of form:
    (date) : [start1, start2, start3]
    where each list entry is the start time of an interview in 
    (hour.decimal_minute) format
    """
    interview_length = pattern[0]   #interview length
    break_length = pattern[1]
    block_avail = {}

    for date in coord_avail:
        times = []
        for strt_end in coord_avail[date]:
            start = strt_end[0]*60
            end = strt_end[1]*60
            while(start < end):
                times.append(start/60)
                start += interview_length + break_length
        block_avail[date] = times
    return block_avail

def available_times(name_exclude, block_avail):
    """
    Input:
        name_exclude - dictionary consisting of
            (name) : {(date) : excluded_times (start, end)}
        block_avail - dictionary consisting of 
                (date) : [start1, start2, start3]
    Returns: 
        name_available - (name) : {(dates) : times}

    Reduces excluded times and available startimes interviews 
    into a single dictionary mapping names to available interview
    start times per input date. 
    """ 
    name_available = {}
    for person in name_exclude:
        available_interviews = {}
        for date in name_exclude[person]:
            available_interviews[date] = []
            for available in block_avail[date]:
                if( not is_in(available, name_exclude[person][date]) ):
                    available_interviews[date].append(available)
        name_available[person] = available_interviews
    return name_available

def sort_and_match(name_available, block_avail):
    """
    Input: 
        name_available - (name) : {(dates) : times}
        mapping names to available interview start times
        block_avail - (date) : [start1, start2, start3]
        mapping dates to all possible interview start times

    Return: 
        matching_dict - (date) : {(time): name}
        not_matched - [name1, name2, name3]

    Reduces availabe interview start times per person to actual 
    interview mappings per person by attempting to match the most
    difficult inputs (smallest number of available interview times)
    to interview times by least to most popular. 
    ** variation on longest task first scheduling - Decreasing Time **

    """
    most_popular = get_most_popular(name_available, block_avail)

    matching_dict = {}
    not_matched = []
    for date in block_avail:
        matching_dict[date] = {}

    #create list using least number of 
    #available dates
    #match hardest first
    name_sort = []
    for person in name_available:
        count = 0
        for date in name_available[person]:
            count += len(name_available[person][date])
        name_sort.append((person, count))

    for person in sorted(name_sort, key=lambda x:x[1]):
        found = False
        for time_date in sorted(most_popular, key=lambda x: x[2]):
            if(close_enough_in_date(time_date[1], 
                name_available[person[0]][time_date[0]])):

                matching_dict[time_date[0]][time_date[1]] = person[0]
                most_popular.remove(time_date)
                found = True
                break

        if found == False:
            not_matched.append(person[0])

    return matching_dict, not_matched

def write_to_csv(outfile, matching_dict, block_avail):
    csv_out = []
    header_row = ["times"]
    sorted_dates = sorted(block_avail.keys(), key=lambda x: x[5::]) 
    #clever way to sort by date!
    for key in sorted_dates:
        header_row.append(key)
    csv_out.append(header_row)

    set_accum = []
    for date in block_avail:
        set_accum += block_avail[date]
    set_accum = sorted(list(set(set_accum))) #remove duplicates

    for time in set_accum:
        date_time = [float_mil_to_actual(time)] 
        date_time += ["--"]*(len(header_row[1::])) #len of header -1
        csv_out.append(date_time)

    for date in matching_dict:
        for time in matching_dict[date]:
            time_pos = set_accum.index(time) + 1
            date_pos = sorted_dates.index(date) + 1
            csv_out[time_pos][date_pos] = matching_dict[date][time]

    with open(outfile, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_out)
    return

#########################################################
############# Helper Functions ##########################
#########################################################

def get_most_popular(name_available, block_avail):
    """
    Input: 
        name_available - (name) : {(dates) : times}
        mapping names to available interview start times
        block_avail - (date) : [start1, start2, start3]
        mapping dates to all possible interview start times

    Return: 
        List of tuples with (date, time, popularity count)

    Reduce name_available and block_avail into a list of 
    tuples with counts for how often each time occured in 
    input availabilities. Used for sorting by popularity 
    in sort and match.
    """
    popular = {}
    for date in block_avail:
        popular[date] = {}
    for date in popular:
        for entry in block_avail[date]:
            popular[date][entry] = 0 

    for name in name_available:
        for date in name_available[name]:
            for entry in name_available[name][date]:
                popular[date][entry] += 1
    
    return_list = []
    for date in popular:
        for entry in popular[date]:
            return_list.append( (date, entry, popular[date][entry]) )

    return return_list

def pretty_print_interviews(matching_dict):
    """
    Print in form: 
    ______________________________________________________
        Interview Times
            (Date):
                 (time1) -- (name1)
                 (time2) -- (name2)
    ______________________________________________________
    """
    print "Interview Times"
    for date in sorted(matching_dict, key=lambda x: x):
        print date + ":"
        for time in sorted(matching_dict[date], key=lambda x: x):
            print "\t {0} -- {1}".format(float_mil_to_actual(time), 
                                            matching_dict[date][time])

def float_mil_to_actual(time):
    """
    Change float format (date.decimal_minute)
    to acceptable time string. Rounded to nearest
    standard time.
    e.g. 10.33 -> "10:20"
    """
    if(time > 12.0):
        final_time = int(time - 12.0)
    else:
        final_time = int(time)
    decimal = time % 1
    actual = int(round(decimal * 60))
    if(actual == 0):
        actual = "00"
    return "{0}:{1}".format(final_time, actual)

def close_enough_in_date(time, time_list):
    """
    Check if an input time is in a list of 
    times within 0.01 error, prevents float comparison
    issues. 
    """
    for x in time_list:
        if(compare_close(time, x, 0.001)):
            return True
    return False

def compare_close(a, b, error):
    return abs(a-b) < error

def is_between(start_end, time):
    return time >= start_end[0] and time <= start_end[1] 

def is_in(available, excluded_times):
    """
    Check of an input time is in a list of (start, end)
    excluded times. 
    """
    test = []
    for time in excluded_times:
        test.append( is_between(time, available) )
    return any(test)

#########################################################
############# End Helper Functions ######################
#########################################################

def main():
    name_exclude = parse_csv("test_schedule_1.csv")
    block_avail = coordinator_availability((15, 5))
    name_available = available_times(name_exclude, block_avail)
    matching_dict, not_matched = sort_and_match(name_available, block_avail)
    write_to_csv("out.csv", matching_dict, block_avail)

if __name__ == "__main__":
    main()

