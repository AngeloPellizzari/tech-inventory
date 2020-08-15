from astropy.table import Table
import urllib
import datetime
import pandas as pd
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)

# importing the data from the google sheets
# Sign out sheet
# imports the csv from a published google sheet, turns it into a readable csv, then separates rows by splitting
link_out = urllib.request.urlopen(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbrggo3hYpkCDFscC8gcUpSlQginobNmvjrayiSAUMMnXW63RGvzyfOgflhb829mW"
    "UPUE3RoQ1hBc-/pub?output=csv")
file_out = str(link_out.read())  # reading the file data from the csv
data_out = file_out.split('\\r\\')  # list of all data now separated by \\r\\
# print(data_out)
# defining a list for the rows and appending lists of rows into the list while eliminating the header row
n_out = len(data_out) - 1  # number of items in the list of total data
rows_out = []  # starting the list of sign out rows
for n in range(n_out):
    rows_out = rows_out + [data_out[n + 1]]  # adding the rows of data as a list of rows

# turning the rows into lists of their elements
n_out_rows = len(rows_out)  # number of rows in the list of rows
data_out_li = []  # setting the list of data out
for n in range(n_out_rows):
    data_1 = rows_out[n].split(',')  # splitting each row up into its individual elements by comma delimited data
    data_out_li.append(
        data_1)  # appending the split up lists to the data list so it is a list of lists of separated data

# Sign in sheet
link_in = urllib.request.urlopen(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQKYN3wLmkAiUZKnApPA975GNx0tLQTNBadSw1QQorpuc_agtV7FO-FAfOrWi6vxas"
    "5tlyEfD5_K0Or/pub?output=csv")
file_in = str(link_in.read())
data_in = file_in.split('\\r\\')
# print(data_in)
# defining a list for the rows and appending lists of rows into the list while eliminating the header row
n_in = len(data_in)
rows_in = []
for n in range(n_in - 1):
    rows_in = rows_in + [data_in[n + 1]]

# turning the rows into lists of their elements
n_in_rows = len(rows_in)
data_in_li = []
for n in range(n_in_rows):
    data_2 = rows_in[n].split(',')
    data_in_li.append(data_2)

"""
# Creating a function to check if the tech has been signed back in with the following parameters
# 1) The date/time of return MUST occur chronologically later than the sign out
# 2) The name of the instructor matches that of the one that signed it out
# 3) The name of the tech matches that of the tech signed out
# 4) The number of tech returned matches that of the tech signed out
"""


def checker():
    out = data_out_li  # importing the sign out data
    tin = data_in_li  # importing the sign in data
    end = len(tin) - 1  # defining the endpoint for the counter function so that all of the data is gone over
    li_inds = list(range(0, len(out)))  # defining the list of indices for the items signed out
    li_name = []  # defining an empty list of names from non-returned tech
    li_tech = []  # defining an empty list of non-returned tech
    li_amnt = []  # defining an empty list of amounts for the non-returned tech
    li_dt_out = []  # defining an empty list of datetimes of signout
    li_dt_return = []  # defining an empty list of expected datetimes of return

    # iterating over the data
    for m in range(len(out)):
        ind = 0
        out_n = out[m]  # current line from sign in
        # defining the data for the sign in
        timestamp_out = out_n[0]
        name_out = out_n[1]
        tech_out = out_n[2]
        amnt_out = out_n[3].replace("'", "")
        timestamp_split = str(timestamp_out).split(' ')
        timestamp_t = timestamp_split[1]
        timestamp_d = timestamp_split[0]
        time_list_out = timestamp_t.split(':')
        date_list_out = timestamp_d.split('/')
        datetime_out = datetime.datetime(int(date_list_out[2]), int(date_list_out[0].replace("n", '')),
                                         int(date_list_out[1]), int(time_list_out[0]), int(time_list_out[1]),
                                         int(time_list_out[2]))

        while ind <= end:
            # defining the data for sign out
            # print(ind)
            tin_ind = tin[ind]  # current line from sign out
            timestamp_in = tin_ind[0]
            name_in = tin_ind[1]
            tech_in = tin_ind[2]
            amnt_in = tin_ind[3].replace("'", "")
            timestamp_split_in = str(timestamp_in).split(' ')
            timestamp_t_in = timestamp_split_in[1]
            timestamp_d_in = timestamp_split_in[0]
            time_list_in = timestamp_t_in.split(':')
            date_list_in = timestamp_d_in.split('/')
            datetime_in = datetime.datetime(int(date_list_in[2]), int(date_list_in[0].replace("n", '')),
                                            int(date_list_in[1]), int(time_list_in[0]), int(time_list_in[1]),
                                            int(time_list_in[2]))
            # checking to match parameters
            if datetime_out <= datetime_in and name_out == name_in and tech_out == tech_in and amnt_in == amnt_out:
                li_inds.remove(m)
                # print(li_inds)
                break
            else:
                ind += 1

    # given the indices of where things are not yet returned
    # returning an altered list from sign out
    if len(li_inds) > 0:
        for i in li_inds:
            out_index = out[int(i)]
            time_out = out_index[0].replace("n", "")
            name = out_index[1]
            tech = out_index[2]
            amnt = out_index[3]
            expected_return_time = out_index[4]
            expected_return_date = out_index[5].replace("'", "")
            expected_return = expected_return_date + ' ' + expected_return_time
            li_dt_out.append(time_out)
            li_name.append(name)
            li_tech.append(tech)
            li_amnt.append(amnt)
            li_dt_return.append(expected_return)
        return Table([li_dt_out, li_name, li_tech, li_amnt],
                     names=('TIME OF SIGNOUT', 'NAME', 'TECH', 'AMOUNT'))
    else:
        return "No tech currently out!"


print(checker()[1:])
