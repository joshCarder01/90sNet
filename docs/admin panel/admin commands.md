# Admin Terminal
The admin terminal has access to many commands which can be used to interact with the backend. Control over the many containers, users, and events can occur from this terminal.

# Commands

## Get Events
**Command:** `get events <time>`

Accepts the unix time stamp as an argument. The server will return all of the pwn events which have occured since that time. Data is returned to the events panel.

## Get User Events
**Command:** `get user events <username|user_id>`

Accepts the desired username or user id. Will then return a list of all of the events which this user is connected too.

## Get Users
**Command:** `get users`

Gets all of the users which are in the database. Refreshes the scoreboard with any new users.

## Get User
**Command:** `get user <username|user_id>`

Get a single user based on either the user id or the username of the user. Either is acceptable to use, the backend will give preference to the `user_id` if both is given. Returned information about that single user.

## Get Machines
**Command:** `get machines`

Get all of the machines which are in the database. General information about the machines is returned.

## Restart Machine
**Command:** `restart machine <name|id>`

Signals the machine indicated to restart. This will happen regardless of the current state of the machine. Can help with many different problems which may occur and not be detected by the automatic maininence.
