#!/usr/bin/python
# Will Dolan
# -*- coding: utf-8 -*-

import time
import psycopg2
import sys
import json


con = None

# array to hold num logs for each month. order goes sept,oc,nov,dec,jan
# ex. month_logs[1] == 20 means there were 20 logs in oct
month_logs = [0] * 5

# define the function blocks
def sept():
    month_logs[0] += 1

def oc():
    month_logs[1] += 1

def nov():
    month_logs[2] += 1

def dec():
    month_logs[3] += 1

def jan():
    month_logs[4] += 1
def other():
    pass


# map the inputs to the function blocks
options = {1 : jan,
           9 : sept,
           10 : oc,
           11 : nov,
           12 : dec,
           2: other,
           3: other,
           4: other,
           5: other,
           6: other,
           7: other,
           8: other
}

try:
    con_string = "host='130.64.17.0' dbname='JMN' user='dolanwill' password='password7'"
 
    # dev: print the connection string we will use to connect
    # print "Connecting to database\n ->%s" % (con_string)
 
    # get a connection, if a connect cannot be made an exception will be raised here
    con = psycopg2.connect(con_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = con.cursor()
    # dev print "Connected!\n"
    cursor.execute("SELECT * FROM users")
    user_list = cursor.fetchall()

    numUsers = 0
    for user in user_list:
        cur_month = (user_list[numUsers][7]).month
        options[cur_month]()
        numUsers+=1

    print "Usage log report: "
    print "sept count: " + str(month_logs[0])
    print "oct count: " + str(month_logs[1])
    print "nov count: " + str(month_logs[2])
    print "dec count: " + str(month_logs[3])
    print "jan count: " + str(month_logs[4])

    s = str(month_logs)
    print s
    print "[sept, oct, nov, dec, jan]"

    # now write the user signups to a .txt file
    filename = 'user_signup_monthly.txt'
    f = open(filename, 'w')
    f.truncate()
    # write the stats to the file
    f.write(s)
    f.close()

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()