import requests
import sys

BASE_URL = "http://api.weatherapi.com/v1/"
API_KEY = open('api_key.txt', 'r').read()

# check if there are saved locations

try:
    locations = open("saved_locations.txt", "r")
except FileNotFoundError:
    locations = open("saved_locations.txt", "w")

locations.close()

def search_location(LOCATION=None):
    if not LOCATION:
        LOCATION = input("Please enter a location to retrieve information about its weather: ")
    URL = BASE_URL + "current.json?key=" + API_KEY + "&q=" + LOCATION
    response = requests.get(URL).json()
    while True:
        if "error" in response:
            print("Invalid input. Try again.")
            continue
        else:
            name = response["location"]["name"]
            condition = response["current"]["condition"]["text"]
            temperature = response["current"]["temp_f"]

            print(f"The weather in {name} is {condition}.")
            print(f"The temperature is {temperature}°F.")
            break

    with open("saved_locations.txt", "r") as locations:
        saved_locations = locations.read().splitlines()

    if name not in saved_locations:
        while True:
            print(f"Would you like to save {name} to your list of locations? Type '1' for YES, '2' for NO.")

            save = input()

            if save == '1':
                with open("saved_locations.txt", "a") as locations:
                    locations.write(f"\n{name}")
                print("Saved!")
                break
            elif save == '2':
                break
            else:
                print("Invalid input. Try again.")

def main():
    while True:
        print("Type '1' to search a location for information about its weather.")
        print("Type '2' to view saved locations.")
        print("Type '3' to exit the application.")

        action = input()

        if action == '3':
            sys.exit()

        elif action == '2':
            saved_locations = {}
            with open("saved_locations.txt", "r") as locations:
                for i, location in enumerate(locations.read().splitlines(), start=1):
                    saved_locations[i] = location
                    print(f"{i}. {location}", sep="")
            if not saved_locations:
                print("No saved locations. Returning to main menu.")
                continue
            print("Type the number of the location on the list to view its weather. Type any other character to return to the main menu.")
            saved_number = input()
            saved_number = int(saved_number)
            if saved_number not in saved_locations:
                continue
            else:
                location = saved_locations[saved_number]
                search_location(location)

        elif action == '1':
            search_location()

        else: 
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()
