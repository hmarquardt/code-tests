# ETL & SQL
Below (and attached) is the skills assessment that has been developed for you. Please email any code or packages you create back to me for review.
Good Luck & Have Fun!
 
The following files are attached:
 
### Calls.csv
This is a file that is uploaded from the call center.  Only calls with a result of 'lead' or 'sale' are considered successful calls. The Number column represents the phone number the customer called in on.
 
### Spots.csv
This represents the media spend for the campaign. Time is the date the spot aired, length is the length of the advertisement, and cost is how much we were charged for it.
 
### StationNumbers.csv
This is a collection of phone numbers, and their attached stations.
 
### Stations.csv
This is a collection of stations and the markets they are in.
 
 
Write a program that imports the data attached into the Database Management System of your choice so that you can deliver a table or view with the following information:
* Market, Station, Number of Spots that ran on the station, The cost of those spots, and the Number of successful calls those ads generated.
Assume that these files will have new data appended to them, so make sure your program can be run on a schedule to keep the database updated. Assume that data will only be appended to these files, never deleted.
Any calls that occurred on phone numbers not associated with our media spend should have a market of 'UNKNOWN' and a station of 'HALO'.
A successful call is only a call with a result of 'lead' or 'sale'
 
#### Answer the following about the data:
* How many successful phone calls were made?
* What was the total amount spent on the advertisements?
* What market has the highest cost per call?
* What market has the lowest cost per spot?
* What station generated the most calls?

 
#### BONUS:
* How many callers have names that are not alliterative?

