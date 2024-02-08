# API
The backend has an api with extensive commands which integrate with the frontend. This api allows the frontend to control much of the tasks which occur. You could even add your own front end if you really wanted too.

# Commands

## Get Events
**Route: ** `/get_events?time=<<unix_timestamp>>`

Accepts the unix time stamp as an argument. The server will return all of the pwn events which have occured since that time. Data is returned in a [json format](data_formatting.md#pwn-events)

## 
