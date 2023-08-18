import requests, sys, json, time
from art import *

BASE_URL = "http://api.weatherapi.com/v1/"
API_KEY = open('api_key.txt', 'r').read()

# Open list of saved locations

try:
    locations = open("saved_locations.txt", "r")
except FileNotFoundError:
    locations = open("saved_locations.txt", "w")

locations.close()

# Search weather for a location

def search_location(LOCATION=None):
    while True:
        if not LOCATION:
            LOCATION = input("Please enter a location to retrieve information about its weather: ")
        URL = BASE_URL + "current.json?key=" + API_KEY + "&q=" + LOCATION
        response = requests.get(URL).json()
        if "error" in response:
            print("Invalid input. Try again.")
            LOCATION = None
            continue
        else:
            name = response["location"]["name"]
            condition = response["current"]["condition"]["text"]
            temperature = response["current"]["temp_f"]

            print(f"The weather in {name} is {condition}.")
            print(f"The temperature is {temperature}°F.")
            find_aqi(name)
            return name
    
# Save location to list

def save(location):
    with open("saved_locations.txt", "r") as locations:
        saved_locations = locations.read().splitlines()

    if location not in saved_locations:
        while True:
            print(f"Would you like to save {location} to your list of locations for quicker access? Type '1' for YES or '2' for NO.")

            save = input()

            if save == '1':
                with open("saved_locations.txt", "a") as locations:
                    locations.write(f"{location}\n")
                print("Saved!")
                break
            elif save == '2':
                break
            else:
                print("Invalid input. Try again.")

# View saved locations

def view_locations():
    saved_locations = {}
    with open("saved_locations.txt", "r") as locations:
        saved_locations[0] = "Clear list of locations."
        for i, location in enumerate(locations.read().splitlines(), start=1):
            saved_locations[i] = location
            print(f"{i}. {location}", sep="")
        if len(saved_locations) <= 1:
            print("No saved locations. Returning to main menu.")
            return
        else:
            print(f"0. {saved_locations[0]}")
    print("Type the number of the location on the list to view its weather. Type any other character to return to the main menu.")
    saved_number = input()
    if saved_number.isnumeric() or int(saved_number) in saved_locations:
        if saved_number == "0":
            confirm = input("Are you sure you want to clear the list? Type '1' to confirm. Type any other character to return to the main menu.\n")
            if confirm == "1":
                with open("saved_locations.txt", "r+") as locations:
                    locations.truncate(0)
                print("Cleared!")
        else:
            location = saved_locations[int(saved_number)]
            search_location(location)

# Call and receieve data from partner's microservice

def find_aqi(location):
    print("Would you like to check the air quality index (AQI)? Type '1' for YES or '2' for NO.")
    
    while True:

        check_aqi = input()

        if check_aqi == '1':
            # clear any old data
            with open("response.txt", "r+") as infile:
                infile.truncate(0)

            with open("request.txt", "w") as outfile:
                outfile.write("AQI\n")
                outfile.write(f"{location}")

            print("Calling AQI microservice . . .")

            time.sleep(5)

            # receive AQI data
            with open("response.txt", "r") as infile:
                data = infile.read()
                try:
                    data = json.loads(data)
                except json.decoder.JSONDecodeError:
                    print("AQI microservice offline. Please try again later.")
                    # clear failedrequest
                    with open("request.txt", "r+") as f:
                        f.truncate(0)
                    return
                aqi = data["overall_aqi"]
                print(f"The air quality index in {location} is {aqi}.")
            return
        elif check_aqi == '2':
            return
        else:
            print("Invalid input. Try again.")


def main():
    art_1 = text2art("Forecaster")
    print(art_1)

    while True:
        print("Type '1' to search a location for information about its weather.")
        print("Type '2' to view saved locations. Saved locations allow for quicker access to weather information.")
        print("Type '3' to exit the application.")

        action = input()

        if action == '3':
            confirm = input("Are you sure? Type '1' to confirm exit. Type any other character to return to the main menu.\n")
            if confirm == "1":
                sys.exit()
            else:
                continue

        elif action == '2':
            view_locations()

        elif action == '1':
            location = search_location()
            save(location)

        else: 
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()
