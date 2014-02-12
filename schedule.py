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
    Input: Excel CSV file
    Parse input into list of available times
    Return: dictionary mapping
    (name) : {(date) : excluded_times (start, end)}

    CSV Format (Google spreadsheet): 
    Name date1                     date2        date3
    a    start1 end1 start2 end2   
    b
    c 
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
    Input: pattern is a tuple of (interview length, break)
    in minutes
    Using the coordinator availability dictionary above, and 
    a given pattern, split the interview availability into 
    pattern specific block, output is dictionary of form 
    --(date) : [available blocks]-- blocks are start times in 
    (hour.decimal_minutes) format
    """

    int_length = pattern[0]
    break_length = pattern[1]
    block_avail = {}

    for date in coord_avail:
        times = []
        for strt_end in coord_avail[date]:
            start = strt_end[0]*60
            end = strt_end[1]*60
            while(start < end):
                times.append(start/60)
                start += int_length + break_length
        block_avail[date] = times
    return block_avail



def compare_close(a, b, error):
    return abs(a-b) < error

def is_between(start_end, time):
    return time >= start_end[0] and time <= start_end[1] 

def is_in(available, excluded_times):
    test = []
    for time in excluded_times:
        test.append( is_between(time, available) )
    return any(test)

def available_times(name_exclude, block_avail):
    """
    return: (name) : {(dates) : times}
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
    Match by available_times
    Return dict: (Date) : {time: person}
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

    for person in sorted(name_sort, key=lambda x:x[1] ):
        found = False
        for time_date in sorted(most_popular, key=lambda x: x[2]):
            if(close_enough_in_date(time_date[1], name_available[person[0]][time_date[0]])):
                matching_dict[time_date[0]][time_date[1]] = person[0]
                most_popular.remove(time_date)
                found = True
                break
        if found == False:
            not_matched.append(person[0])

    pretty_print_interviews(matching_dict)
    return matching_dict, not_matched

def close_enough_in_date(time, time_list):
    for x in time_list:
        if(compare_close(time, x, 0.001)):
            return True
    return False

def get_most_popular(name_available, block_avail):

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
    print "Interview Times"
    for date in sorted(matching_dict, key=lambda x: x):
        print date + ":"
        for time in sorted(matching_dict[date], key=lambda x: x):
            print "\t {0} -- {1}".format(float_mil_to_actual(time), 
                                            matching_dict[date][time])

def float_mil_to_actual(time):
    if(time > 12.0):
        final_time = int(time - 12.0)
    else:
        final_time = int(time)
    decimal = time % 1
    actual = int(round(decimal * 60))
    if(actual == 0):
        actual = "00"
    return "{0}:{1}".format(final_time, actual)

def main():
    name_exclude = parse_csv("test_schedule_1.csv")
    block_avail = coordinator_availability((15, 5))
    name_available = available_times(name_exclude, block_avail)
    final = sort_and_match(name_available, block_avail)
    print final[0]
    print final[1]

if __name__ == "__main__":
    main()

