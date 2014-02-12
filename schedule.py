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
        ("Fri, 14th") : [(15.0, 18.0)],
        ("Sat, 15th") : [(10.0, 19.0)],
        ("Sun, 16th") : [(10.0, 14,0), (19.0, 21.0)],
        ("Fri, 21st") : [(15.0, 20.0)],
        ("Sat, 22nd") : [(10.0, 19.0)],
        ("Sun, 23rd") : [(10.0, 14,0), (19.0, 21.0)]
    }

def coordinator_availability(pattern):
    """
    Input: pattern is a tuple of (interview length, break)
    Using the coordinator availability dictionary above, and 
    a given pattern, split the interview availability into 
    pattern specific block, output is dictionary of form 
    --(date) : [available blocks]--
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

print coordinator_availability((15, 5))
