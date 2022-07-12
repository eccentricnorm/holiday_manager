import datetime
import json
from bs4 import BeautifulSoup
import pytz
import requests
from dataclasses import dataclass
import os

@dataclass
class Holiday:
    """Data class for holidays that will be in the app"""
    name: str
    date: datetime        
    
    def __str__ (self):
        return f'{self.name} - ({self.date})'
        # Returns Holiday - (Date) when printed
          
           
class HolidayList:
    """ Class that contains and wraps list of holidays"""
    def __init__(self):
        self.innerHolidays = []
   
    def addHoliday(self, holidayObj):
        if (type(holidayObj) == Holiday):
            self.innerHolidays.append(holidayObj)
            print(f"{holidayObj} has been added")
        else:
            print("You can only input a Holiday Object")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, holiday_name, date):
        searched_holiday = Holiday(holiday_name, date)
        if searched_holiday in self.innerHolidays:
            return searched_holiday

    def removeHoliday(holiday_name, date):
        print("Removed")
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, file_location):
        with open(file_location) as json_file:
            # Loads JSON and 
            json_dict = json.load(json_file)
            json_list = json_dict["holidays"]
            for record in json_list:
                name = record["name"]
                # print(name)
                date = record["date"]
                # print(date)
                holiday_record = Holiday(name, date)
                self.innerHolidays.append(holiday_record)
            # print(self.innerHolidays)

    def save_to_json(self, file_location):
        # Saves Holiday List Object to a JSON file
        with open(file_location, "w") as f:
            holiday_dict_list = []
            holiday = {}
            for holiday_record in self.innerHolidays:
                holiday = {'name':holiday_record.name, 'date':holiday_record.date}
                holiday_dict_list.append(holiday)
            holiday_list_dict =  {"holidays" : holiday_dict_list} 
            json.dump(holiday_list_dict, f, indent= 4)
        
    def scrapeHolidays(self):
        from datetime import datetime

        for page in range (0, 5):
            
            url = f'https://www.timeanddate.com/holidays/us/202{page}?hol=33554809'

            response=requests.get(url)
            site_content = response.text
            soup = BeautifulSoup(site_content, 'html.parser')

            shown_rows = soup.find_all("tr", attrs= {"class":"showrow"})
            # print(shown_rows)
            for row in shown_rows:
                date_raw = row["data-date"]
                dt_object = datetime.fromtimestamp(int(str(date_raw)[0:-3]))
                dt_object = dt_object.astimezone(pytz.timezone("UTC"))
                short_date = dt_object.strftime("%Y-%m-%d")
                # print(short_date)
                holiday_raw = row.find("a")
                holiday_name = holiday_raw.text
                # print(holiday)
                holiday_record = Holiday(holiday_name, short_date)
                # print(holiday_record)
                if not holiday_record in self.innerHolidays:
                    self.innerHolidays.append(holiday_record)
        
            # print(self.innerHolidays)


            


        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        num_of_holidays = len(self.innerHolidays)
        return num_of_holidays
    
#     def filter_holidays_by_week(year, week_number):
#         # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
#         # Week number is part of the the Datetime object
#         # Cast filter results as list
#         # return your holidays

#     def displayHolidaysInWeek(holidayList):
#         # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
#         # Output formated holidays in the week. 
#         # * Remember to use the holiday __str__ method.

#     def getWeather(weekNum):
#         # Convert weekNum to range between two days
#         # Use Try / Except to catch problems
#         # Query API for weather in that week range
#         # Format weather information and return weather string.

    def viewCurrentWeek(self):
        
        my_date = datetime.date.today() # if date is 01/01/2018
        year, week_num, day_of_week = my_date.isocalendar()

        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
   

def main():
    # initiates instance of HolidayList class
    holidayDict = HolidayList()
    holiday_number = holidayDict.numHolidays()
    print("Welcome to the Holiday Calenday Manager App")
    print("-----------------")

    # If a JSON file exists already, load that else. else load starter
    file_exists = os.path.exists("data/saved_holidays.json")
    # print(file_exists)
    if file_exists:
        HolidayList.read_json(holidayDict, "data\saved_holidays.json")
        print("Existing holiday list loaded.")
    else:
        print('Loading presaved holidays...')
        HolidayList.read_json(holidayDict, "data\holidays.json")
        
    
    print("Searching for new holidays...")
    HolidayList.scrapeHolidays(holidayDict)

    holiday_number = holidayDict.numHolidays()
    print("Calendar loaded.")
    print(f'There are {holiday_number} holidays in the system.\n')
    still_working = True
    while still_working:
        # Prints Main Menu from TXT file
        f = open("data\mainmenu.txt")
        menu_text = f.read()
        print(menu_text)
        f.close()

        selection = str(input("Please choose an option: ").strip())
        options = ['1', '2', '3', '4', '5']
        while selection not in options:
            selection = str(input("Option not valid: Please choose an option: ").strip())
        else:
            if(selection == "1"):
                print("\nAdd a Holiday\n===========\n")
                hol = str(input("Holiday: "))
                date = str(input("Date: "))

                # print("Success:\n")
                # HolidayList.addHoliday(holidayDict, Holiday(hol,date))
            elif(selection == "2"): 
                print("\nRemove A Holiday")
                print("=============")
                # Remove a Holiday
            elif(selection == "3"):

                print("\nSaving Holiday List")
                print("=============")
                save_confirmation = input("Are you sure you want to save your changes? [Y/N]: ").strip().upper()
                save_options = ["Y", "N"]
                while save_confirmation not in save_options:
                    save_confirmation = input("Please select a valid option. [Y/N]: ").strip().upper()
                else:
                    if save_confirmation == "Y":
                        HolidayList.save_to_json(holidayDict, "data\saved_holidays.json")
                        print("Your changes have been saved.")
                    else:
                        print("Save Cancelled. Returning to Main Menu")
                
            elif(selection == "4"):
                print("\nView Holidays")
                print("=============")
                year_selection = input("Which year?")
                week_selection = input("Which week? [#1-52, Leave blank for the current week]: ")
                
            elif(selection == "5"):
                print("\nExit")
                print("=============")
                # Determine if JSON matches inner_list
                # If matches, confirm exit

                # If different, warn user it is not saved
                
            else:
                print("\n !!Please Select A Valid Option!!") 
    else:
        # App Closes when Still Working is False
        print("Goodbye")
    
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();