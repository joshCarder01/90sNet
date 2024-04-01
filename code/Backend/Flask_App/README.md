# For Running
Would recommend using whatever docker compose container which has been made

# CLI Commands

- `flask --app app db init`
  - Initializes a blank database
- `flask --app app db random`
  - Initializes the database with random data. Should be helpful to set everything up.
- `flask --app app db seed

# API Documentation
This will represent the current documentation of the api. Each subheader is a blueprint in flask, the blueprint will use some base url for all of its commands.

For example, the [Events](#events) api uses `/events` as its base url. To get to use the [Events Since](#get-all-events-since) command you would query the url `{base-address}/events/since` and provide the json requested. To use the [Get All Events](#get-all-events) command you would query the url `{base-address}/events/`.

## Users

### Get All Users

Gets all of the users in the database

* route
  * `/users`
* Method
  * `GET`
* JSON Request
  * N/A
* Returns
  * Json of all of the users in the database

### Add A User

Adds a user to the database

* route
  * `/users/add`
* Method
  * `POST`
* JSON Request
  ```json
  {
    "username": "{{username}}",   // Whatever their username is
    "name": "{{name}}",           // Optional
  }
* Returns
  * Json of the newly created user
  ```


## Events

Returned time attribute is in datetime.timestamp format as a double

### Get All Events

* Route 
  * `/eventss`
* Method
  * `GET`
* JSON Request 
    *   N/A
* Returns
  * JSON of all of the events


### Get All Events Since

* Route 
  * `/getEventsSince`
* Method
  * `GET`
* JSON Request 
    *   ```json
        {
            "time": "{{unix-timestamp}}"  // Expecting a timestamp which is made from datetime.timestamp()
        }
        ```
* Returns
  * JSON of all of the events with a timestamp after requested

### Add a new Event

* Route
  * `/events/add`
* Method
  * `POST`
* JSON Request
  *     ```json
        {
          "type": "{{event-type}}",             // from tuple in Methods.event.EventTypeTuple
          "time": "{{time event occured}}",     // Optional, by default the server handles setting the time
          "machine_id": "{{machine-id}}",       // What machine did the event happen on
          "machine_name": "{{machine-name}}",   // The machine name this happened on
          "user_id": "{{user-id}}",             // Optional: Which user if attribution is possible
          "description": "{{desc}}",            // Optional: Custom string to pass type specific information
        }
        ```
* Returns
  * JSON of the newly created event

## Machines

### Get All Machines

* Route
  * `/machines`
