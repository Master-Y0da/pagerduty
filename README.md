# Pagerduty Backend API

This app is an API made in Flask, with a MYSQL database, that fetch data from Pagerduty API!.

In this app, the effort was made to largely use a strictly modular architecture design pattern, known as a modular monolith, in which coupling between modules is prohibited. Therefore, it can be seen in some of the data layers, asynchronous calls to other endpoints of the same app, to request the required data. In a more elaborate production application, the idea is that there is an extra service that communicates the endpoints, to my personal taste it could be rabbit MQ, or if warranted, a layer such as camunda. However, this was not feasible to apply to this test due to time restrictions.


## Running the app

 Detailed info about dependencies used on this app, can be found in requirements.txt file.
 Also is using docker!

 
- Move to project root.
- Up the services ```docker compose up -d --build```
- Visit http://localhost:5000/api/v1/docs for swagger documentation and primary test of the endpoints.

## Testing

 A testing service is incorporated in docker-compose file. All docker services are chained, so the test services run once the flask
 server is up!.

## Special Considerations

- In Windows, the mysql service tends to take longer to start, which is why the app sometimes fails to connect to the database in time. I try some known mechanism to solve this but some times not work properly.
   This is resolved by manually restarting the web app container. This behavior was tested on Linux without being able to replicate.

- If the previous event occurs, the test service must also be restarted manually for its correct functioning.
