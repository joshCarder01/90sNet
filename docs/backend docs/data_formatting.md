# Data Formatting

## Pwn Events
Pwn events keep track of the time in which a user has taken control of a machine. The backend will record and store the event for logging and score keeping purposes.

- `id`
  - This is the id of the event, stored for simplicity on the backend.
- `time`
  - Unix Timestamp in milliseconds (GMT).
- `user_id`
  - The id of the user which is involved in the event.
- `machine_id`
  - The id of the machine which is involved in the event.

### Example
```json
{
    "id": 1,
    "time": 1371297620301,
    "user_id": 234,
    "machine_id": 555
}
```

## Users
These are the competitors and the data which is associated with them.

- `id`
  - The id of the user, used internally.
- `username`
  - The username of the user, this is shown publically and should be unique
- `name`
  - Name of the user, can be used for any marketing uses.

