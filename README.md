# Plant DataPoint Microservice

## How to run
```bash
docker-compose up --build
```
After all containers are up and ready you can access the backend through `http://127.0.0.1:8000`. You can change the server API endpoint port in `.env` file located at the top directory.
 
## Endpoints:
##### Swagger documentations
You can access swagger documentation of Available endpoints using the following URL:
```text
http://127.0.0.1:8000/v1/docs/
```
##### Update DataPoints
```text
// Update datapoints of Plant with id=1
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{ "after": "2020-01-01", "before": "2020-02-02" }' \
  http://127.0.0.1:8000/v1/plant/plant/1/datapoints_update/ 
```

##### List plants
```text
http://127.0.0.1:8000/v1/plant/plant/
```
##### List DataPoints
```text
http://127.0.0.1:8000/v1/plant/datapoint/
```
## How to run tests
```bash
cd src
make venv && source venv/bin/activate
make test
```

## Run coverage
```bash
cd src
make coverage
```

## Where to change settings
```text
edit .env file
```

## TODO:
- Add custom permission control based on user roles
- Update DataPoints based on source_id of plants  
