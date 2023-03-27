# Step 1: Clone the project
```shell
git clone https://github.com/etcmid/ratestask.git
```


# Step 2: Run the containers
```shell
docker-compose up -d && docker-compose logs --tail 10 -f
```

# Step 3: Fetch the rates
```shell
curl "http://localhost:5050/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```

Output Json
```json
[
  {
    "day": "2016-01-01", 
    "average_price": "1077"
  }, 
  {
    "day": "2016-01-02", 
    "average_price": "1077"
  }, 
  {
    "day": "2016-01-03", 
    "average_price": null
  }, 
  {
    "day": "2016-01-04", 
    "average_price": null
  }, 
  {
    "day": "2016-01-05", 
    "average_price": "1116"
  }, 
  {
    "day": "2016-01-06", 
    "average_price": "1117"
  }, 
  {
    "day": "2016-01-07", 
    "average_price": "1110"
  }, 
  {
    "day": "2016-01-08", 
    "average_price": "1094"
  }, 
  {
    "day": "2016-01-09", 
    "average_price": "1094"
  }, 
  {
    "day": "2016-01-10", 
    "average_price": "1094"
  }
]
```
# Step 4 Run the test cases
```shell
docker-compose exec web pytest --verbose
```


