import requests

aqiURL = 'https://api.api-ninjas.com/v1/airquality?city='
API_KEY = open('microservice_api_key.txt', 'r').read()

while True:
    with open("request.txt", "r+") as f:
        data = [line.rstrip() for line in f]
        f.truncate(0)
    
    if data and data[0] == "AQI":
        location = data[1]

        fullURL = aqiURL + location
        print(f"Receiving AQI data from {fullURL}")

        response = requests.get(fullURL, headers={'X-Api-Key':API_KEY})
        if response.status_code == requests.codes.ok:
            f = open("response.txt", "w")
            f.write(response.text)
            f.close()
            print("Returning AQI data to calling program.")
        else:
            print("Error:", response.status_code, response.text)
        