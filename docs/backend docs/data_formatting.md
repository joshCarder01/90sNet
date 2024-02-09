# Data Formatting

## Pwn Events
Pwn events keep track of the time in which a user has taken control of a machine. The backend will record and store the event for logging and score keeping purposes.

- `id` : `int`
  - This is the id of the event, stored for simplicity on the backend.
- `time` : `datetime`
  - Unix Timestamp in seconds (GMT).
- `user_id`
  - The id of the user which is involved in the event.
- `machine_id`
  - The id of the machine which is involved in the event.

### Example
```json
{
    "id": 943,
    "time": 1371297923,
    "user_id": 223,
    "machine_id": 953
}
```

## Users
These are the competitors and the data which is associated with them.

- `id` : `int`
  - The id of the user, used internally.
- `username` : `text`
  - The username of the user, this is shown publically and should be unique
- `name` : `text`
  - Name of the user, can be used for any marketing uses.

### Example
```json
{
    "id": 223,
    "username": "user_234",
    "name": "User's Name"
}
```
## Machine

- `id` : `int`
  - The id of the machine, used internally.
- `name` : `text`
  - unique human readable name of the machine. Seen admin side for ease.
- `score` : `int`
  - Score the user will earn for completing this machine
 
### Example
```json
{
    "id": 953,
    "name": "machine_here_233",
    "score": 500
}
```
