# The setup
This was not web work, but rather an ETL & SQL exercise, the instructions are provided in *instructions.md* and the files described therein are included in the repository.   There is a single, almost insignificant script here as well *import_submit.py* that loads the .csv files into tables.   The rest here is in the SQL, which is enumerated below.

# Response
Attached is import_submit.py -- not much to it really.   Comments contain table structure of files. connect string has been redacted.   I used Oracle as the data store -- this makes some things easier.   For example, it was a nice touch, the SQL injection in the data set, though Oracle's bind variables sanitize such nonsense, use your imagination for the use of a quote or sanitize function on the data if using a different datastore.

With respect to the data itself, the exercise was silent on what to do with bad data ... for example, there was an invalid 3 character state code for Mr. Stallman (another nice touch!), so I fixed it to a bogus 2 character ZZ before import.  Again, in a real script we'd do some state validation against the countries that would be valid respondents and then have reject table with the garbage ... that's little too much work to do for this exercise.   Same thing with some of the names, there are a couple records with call center notes appended, those would need to be cleaned ... they could be targeted by tokenizing the name field and making anything over 3 or 4 to be suspects for further review/processing, again a production exercise for a later date if needed.   In this case I simply increased the size of the name field in the db table and pulled it in as is, since this data wasn't required for the analysis portion of the exercise that was the end.

Perhaps the biggest punt I did with the exercise was the "we're going to keep adding to these files", that's fine, but without a discussion about record collision and duplicate definition this is difficult to definitively address.   Almost all of the data is compound key, my initial thoughts would be to add a hash field to each record, as well as a date created and date modified ... the hash could be used for collision detection and the create/modify stamps used for deletion/rollback of bad data (duplicates) that sneak in in some other way.    I also modified the header row in the files to avoid not having reserved word collision in the SQL ... let me use the nifty row->hash function, obviously I couldn't do that without some additional manipulation if the files would consistently come in that way.   Anyway, I hope that's enough to convince you I can think, without writing a lot of extra code here.

So with that as the backdrop, here's what we have.  I've inserted the interpretation after each bullet of the original exercise:

> Write a program that imports the data attached into the Database Management System of your choice so that you can deliver a table or view with the following information:
Market, Station, Number of Spots that ran on the station, The cost of those spots, and the Number of successful calls those ads generated.

```sql
select v.market,v.station,v.phone,                                                                                                                    
    (select count(*) from emm_spots where nvl(station,'HALO') = v.station) as num_spots,                                                              
    (select sum(cost) from emm_spots where nvl(station,'HALO') = v.station) as dol_posts,                                                             
    (select count(*) from emm_calls where phone = v.phone and result in ('sale','lead') ) as success_calls                                            
from                                                                                                                                                  
(select nvl(t.station,'HALO') as station,nvl(t.market,'UNKNOWN') as market,c.* from                                                                   
    emm_calls c left outer join emm_stationnumbers n on c.phone = n.phone                                                                             
    left join emm_stations t on n.station = t.station                                                                                                 
) v                                                                                                                                                   
group by v.market,v.station,v.phone                                                                                                                   
order by market         
```
I've created an inline view joining the stations to the calls and then queried that view to create the dataset described.        Below is the resulting dataset:
```
MARKET                                   STAT PHONE            NUM_SPOTS  DOL_POSTS SUCCESS_CALLS
---------------------------------------- ---- --------------- ---------- ---------- -------------
ATLANTA                                  KBZQ 8008519961               4    2721.19             2
ATLANTA, GA                              KEUU 8008621846               1     546.88             0
CHICAGO                                  KEHX 8005311707               1      168.1             1
CHICAGO                                  KQQW 8009256650              10    5901.15             1
CINCINNATI                               WELO 8002780879               1     957.72             2
CINCINNATI                               WUQL 8001074445               5    2044.87             0
CLEVELAND-AKRON (CANTON)                 WSKI 8007590252               1     319.11             1
COLUMBUS                                 WWTY 8007277863               2    1055.06             2
DALLAS-FT. WORTH                         KEAJ 8008335685               1     287.52             1
DENVER                                   KMST 8002786469               4    2573.02             4
DETROIT                                  WLMW 8009196917               3    1560.77             1
DETROIT                                  WYNA 8004868772               1     792.26             0
FLINT-SAGINAW-BAY CITY                   KPBD 8004605818               1     994.07             1
FT. WAYNE                                KITT 8008342387               1     215.19             2
GRAND RAPIDS-KALAMAZOO-B.CREEK           WGZF 8009540625               1     252.31             4
GREENVILLE-SPART-ASHEVLL-ANDER           KNWQ 8001862915               1      912.4             2
HOUSTON                                  WZTH 8006404614               1     111.54             1
INDIANAPOLIS                             KJVC 8001003659               4    2235.68             2
KANSAS CITY                              KANP 8002455590               4     2298.4             1
LANSING                                  WXZW 8004564735               1     689.02             3
LEXINGTON                                KRRZ 8005414537               6    1697.89             1
LOS ANGELES                              WUMC 8009880918               4    2809.14             1
LOS ANGELES, CA                          KORY 8003514321               1     198.88             0
LOS ANGELES, CA                          WAKP 8008097570               5    2754.65             1
LOUISVILLE                               KHVU 8008643993               5    3415.54             1
MIAMI-FT. LAUDERDALE                     WCEW 8001449565               1     727.94             0
MILWAUKEE                                KXAI 8001961621               5    2836.97             2
MINNEAPOLIS                              WDQT 8007929658               4    2657.09             3
MINNEAPOLIS-ST. PAUL                     WBCG 8006816377               1     180.67             1
NASHVILLE                                KPWC 8009285013               0                        0
OMAHA                                    KAZB 8008567471               1     789.32             1
PHOENIX (PRESCOTT)                       KYAL 8008788539               1      867.4             2
PORTLAND, OR                             KPTB 8005823913               4    2021.88             2
SACRAMENTO                               KRTU 8002647957               1      891.6             1
SACRAMENTO-STOCKTON-MODESTO              WAMA 8003856258               1     256.34             2
SAN DIEGO                                KDLO 8003661331               2     559.79             2
SAN DIEGO, CA                            KRKW 8007748108               1     135.07             1
SAN FRANCISCO, CA                        WEFK 8001852156               1     311.72             1
SEATTLE                                  WSLQ 8001258480               3    2105.52             1
SEATTLE-TACOMA                           KICL 8002324927               1     303.16             0
SOUTH BEND-ELKHART                       WNBG 8004455001               1     869.27             1
ST. LOUIS                                KWTQ 8008865631               3    1092.37             2
TAMPA-ST PETERSBURG (SARASOTA)           WLID 8002071805               1     829.46             1
UNKNOWN                                  HALO 8003668168               0                        1
UNKNOWN                                  HALO 8006810950               0                        0
```
> Assume that these files will have new data appended to them, so make sure your program can be run on a schedule to keep the database updated. Assume that data will only be appended to these files, never deleted.

Addressed in opening narrative.

> Any calls that occurred on phone numbers not associated with our media spend should have a market of “UNKNOWN” and a station of “HALO.”
A successful call is only a call with a result of ‘lead’ or ‘sale'
 
Accomodated in view logic

> Answer the following about the data:
> How many successful phone calls were made?
```sql
select count(*) from emm_calls where result in ('sale','lead')

  COUNT(*)
----------
        59
```

> What was the total amount spent on the advertisements?
```sql
select sum(cost) from emm_spots;

 SUM(COST)
----------
  54947.93
```
> What market has the highest cost per call?

Not sure if  this is a trick question or not ... nor did I really check if this impacted the answer, but the data does contain what to my mind would be duplicate market data .. for example, Los Angeles and Los Angeles, CA ... to me that would be one market and need to be reconciled, but perhaps the ad business is different, so I just did a straight query.

```sql
  1  select t.market,
  2      (select sum(cost) from
  3          (select a.market,b.* from emm_stations a, emm_spots b where a.station=b.station) where market = t.market)  as budget,
  4      (select count(*) from
  5          (select i.market,k.* from emm_stations i, emm_stationnumbers j, emm_calls k where
  6              i.station = j.station and j.phone = k.phone) where market=t.market) as calls_rcvd,
  7      ((select sum(cost) from
  8          (select a.market,b.* from emm_stations a, emm_spots b where a.station=b.station) where market = t.market)/
  9      (select count(*) from
 10          (select i.market,k.* from emm_stations i, emm_stationnumbers j, emm_calls k where
 11              i.station = j.station and j.phone = k.phone) where market=t.market)) as cost_per_call
 12      from
 13      emm_stations t
 14      group by t.market
 15*     order by cost_per_call desc

MARKET                                       BUDGET CALLS_RCVD COST_PER_CALL
---------------------------------------- ---------- ---------- -------------
KANSAS CITY                                 2298.40          2       1149.20
```

> What market has the lowest cost per spot?
```sql
  1  select market, count(*) as spots,sum(cost) as amount, sum(cost)/count(*) as cost_per from emm_stations t,emm_spots s
  2  where t.station = s.station group by market
  3* order by cost_per

MARKET                                        SPOTS     AMOUNT   COST_PER
---------------------------------------- ---------- ---------- ----------
HOUSTON                                           1     111.54     111.54
```

> What station generated the most calls?
```sql 
SQL> select station,count(*) as calls from emm_stationnumbers n, emm_calls c
  2  where n.phone = c.phone
  3  group by station
  4  order by calls desc;

STAT      CALLS
---- ----------
WNBG          7
```

>BONUS:
>How many callers have names that are not alliterative?
 
What, no Francine Phillips?  ... Looks like 7 to me, but that way by eye.

