#! /usr/bin/env python
'''
Empower Media Marketing skills assesement import job

Hank Marquuardt 5/8/2015

'''
import os
import sys
import csv
import datetime
import cx_Oracle

'''
inumber,ilength,result,callernumber,callername,callercity,callerstate
SQL> desc emm_calls;
 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 PHONE                                              VARCHAR2(15)
 CALL_LENGTH                                        NUMBER
 RESULT                                             VARCHAR2(15)
 CALLER_PHONE                                       VARCHAR2(15)
 CALLER_NAME                                        VARCHAR2(128)
 CALLER_CITY                                        VARCHAR2(25)
 CALLER_STATE                                       VARCHAR2(2)

'''
callsSql = '''
    insert into emm_calls (phone,call_length,result,caller_phone,caller_name,caller_city,caller_state) values
    (:inumber,:ilength,:result,:callernumber,:callername,:callercity,:callerstate)
'''

''' 
iNumber,Station
SQL> desc emm_stationnumbers;
 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 STATION                                            VARCHAR2(4)
 PHONE                                              VARCHAR2(15)

'''
stationnumbersSql = '''
    insert into emm_stationnumbers (station, phone) values (:Station,:iNumber)
'''

'''
Station,iTime,iLength,Cost
SQL> desc emm_spots;
 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 STATION                                            VARCHAR2(4)
 SPOT_DATE                                          DATE
 SPOT_DURATION                                      NUMBER
 COST                                               NUMBER

'''
spotsSql = '''
    insert into emm_spots (station,spot_date,spot_duration,cost) values (:Station,:iTime,:iLength,:Cost)
'''

'''
Station,Market
SQL> desc emm_stations;
 Name                                      Null?    Type
 ----------------------------------------- -------- ----------------------------
 STATION                                            VARCHAR2(4)
 MARKET                                             VARCHAR2(40)
'''
stationsSql = '''
    insert into emm_stations (station, market) values (:Station,:Market)
'''

db = cx_Oracle.connect('insertConnectStringHere, redacted for your viewing pleasure')
cursor = db.cursor()

with open('calls.csv') as calls:
    fetch = csv.DictReader(calls)
    for row in fetch:
        cursor.execute(callsSql,row)

with open('stationnumbers.csv') as stationnumbers:
    fetch = csv.DictReader(stationnumbers)
    for row in fetch:
        cursor.execute(stationnumbersSql,row)
with open('stations.csv') as stations:
    fetch = csv.DictReader(stations)
    for row in fetch:
        cursor.execute(stationsSql,row)

with open('spots.csv') as spots:
    fetch = csv.DictReader(spots)
    for row in fetch:
        row['iTime'] = datetime.datetime.strptime(row['iTime'],"%x").strftime("%d-%b-%y")
        cursor.execute(spotsSql,row)
db.commit()
db.close()
