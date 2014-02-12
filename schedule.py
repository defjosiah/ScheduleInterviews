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
        ("Fri 14th") : [(15.0, 18.0)],
        ("Sat 15th") : [(10.0, 19.0)],
        ("Sun 16th") : [(10.0, 14,0), (19.0, 21.0)],
        ("Fri 21st") : [(15.0, 20.0)],
        ("Sat 22nd") : [(10.0, 19.0)],
        ("Sun 23rd") : [(10.0, 14,0), (19.0, 21.0)]
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
    name_exlude = {}
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
                name_exlude[row[0]] = exclude
    return name_exlude




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

print parse_csv("test_schedule_1.csv")