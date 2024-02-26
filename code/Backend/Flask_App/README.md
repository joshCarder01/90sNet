# For Running
Would recommend using whatever docker compose container which has been made

# CLI Commands

- `flask --app app db init`
  - Initializes the database with random data. Should be helpful to set everything up.

# API Documentation
This will represent the current documentation of the api. Each subheader is a blueprint in flask, the blueprint will use some base url for all of its commands.

For example, the [Events](#events) api uses `/events` as its base url. To get to use the [Events Since](#get-all-events-since) command you would query the url `{base-address}/events/since` and provide the json requested. To use the [Get All Events](#get-all-events) command you would query the url `{base-address}/events/`.

## Users

**Base URL:** `/user`

### Get All Users

Gets all of the users in the database

* route
  * `/`
* Method
  * `GET`
* JSON Request
  * N/A
* Returns
  * Json of all of the users in the database

## Events
**Base URL:** `/events`

Returned time attribute is in millisecond precision.

### Get All Events

* Route 
  * `/`
* Method
  * `GET`
* JSON Request 
    *   N/A
* Returns
  * JSON of all of the events


### Get All Events Since

* Route 
  * `/since`
* Method
  * `GET`
* JSON Request 
    *   ```
        {
            "time": {{unix-timestamp}}
        }
        ```
* Returns
  * JSON of all of the events with a timestamp after requested

## Machines

### Get All Machines
