import datetime
import json
from bs4 import BeautifulSoup
import pytz
import requests
from dataclasses import dataclass
import os
from config_norm import menu_text_loc
from config_norm import starter_json_loc

@dataclass
class Holiday:
    """Data class for holidays that will be in the app"""
    name: str
    date: datetime 
 
    def get_date(self):
        return self.date

    def asdict(self):
        return {'name': self.name, 'date': self.date}
    
    def __str__ (self):
        return f'{self.name} - ({self.date})'
        # Returns Holiday - (Date) when printed

          
           
class HolidayList:
    """ Class that contains and wraps list of holidays"""
    def __init__(self):
        self.inner_holiday = []
   
    def addHoliday(self, holidayObj):
        if (type(holidayObj) == Holiday):
            self.inner_holiday.append(holidayObj)
            print(f"{holidayObj} has been added")
        else:
            print("You can only input a Holiday Object")

    def findHoliday(self, holiday_name, date):
        searched_holiday = Holiday(holiday_name, date)
        if searched_holiday in self.inner_holiday:
            return searched_holiday

    def removeHoliday(self, holiday_name):
        # Searches active holiday list by names
        for holiday in self.inner_holiday:
            if holiday_name == holiday.name:
                date = holiday.date
                removed_holiday = Holiday(holiday_name, date)
                self.inner_holiday.remove(removed_holiday)
                print(f'{removed_holiday} removed successfully.')
        else:
                print("Holiday not found.")


    def read_json(self, file_location):
        with open(file_location) as json_file:
            # Loads JSON and adds to inner_holidays list
            json_dict = json.load(json_file)
            json_list = json_dict["holidays"]
            for record in json_list:
                name = record["name"]
                date = record["date"]
                
                holiday_record = Holiday(name, date)
                self.inner_holiday.append(holiday_record)
            

    def save_to_json(self, file_location):
        # Saves Holiday List Object to a JSON file
        with open(file_location, "w") as f:
            holiday_dict_list = []
            holiday = {}
            for holiday_record in self.inner_holiday:
                holiday = {'name':holiday_record.name, 'date':holiday_record.date}
                holiday_dict_list.append(holiday)
            holiday_list_dict =  {"holidays" : holiday_dict_list} 
            json.dump(holiday_list_dict, f, indent= 4)
        
    def scrapeHolidays(self):

        for page in range (0, 5):
            # Shows years from 2020 to 2024
            url = f'https://www.timeanddate.com/holidays/us/202{page}?hol=33554809'

            response=requests.get(url)
            site_content = response.text
            soup = BeautifulSoup(site_content, 'html.parser')

            shown_rows = soup.find_all("tr", attrs= {"class":"showrow"})
            
            for row in shown_rows:
                # Grabs UNIX time with milliseconds
                date_raw = row["data-date"]
                # Removes Milliseconds
                dt_object = datetime.datetime.fromtimestamp(int(str(date_raw)[0:-3]))
                # Adjusts timezone to correct date
                dt_object = dt_object.astimezone(pytz.timezone("UTC"))
                # strips away the time from datetime
                short_date = dt_object.strftime("%Y-%m-%d")
                
                # Finds the link in each row and assigns the text as holiday name
                holiday_raw = row.find("a")
                holiday_name = holiday_raw.text
                
                holiday_record = Holiday(holiday_name, short_date)
                
                if not holiday_record in self.inner_holiday:
                    self.inner_holiday.append(holiday_record)
        


    def num_holidays(self):
        num_of_holidays = len(self.inner_holiday)
        return num_of_holidays
    
    def filter_holidays_by_week(self, year, week_number):
        # Uses entered or calculated year and week to filter holidays and returns result

        desired_year = int(year)
        desired_week = int(week_number)

        filtered_holidays = []
        filtered_holidays = list(filter(lambda holiday : holiday.date.isocalendar()[0] == desired_year and 
            holiday.date.isocalendar()[1] == desired_week, self.inner_holiday))

        return filtered_holidays

    def displayHolidaysInWeek(holiday_list):
        if (len(holiday_list)) == 0:
            "There are no holidays for the week"
        else:   
            for holiday in holiday_list:
                print(holiday)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def view_current_week(self):
        my_date = datetime.date.today()
        # Take today's date and extract the iso year and week
        year = my_date.isocalendar()[0]
        week_num = my_date.isocalendar()[1]
        return year, week_num


    def is_saved(self):
        with open('data\saved_holidays.json') as json_file:
        # Loads JSON and
            saved_list = [] 
            json_dict = json.load(json_file)
            json_list = json_dict["holidays"]
            for record in json_list:
                name = record["name"]
                date = record["date"]
                
                holiday_record = Holiday(name, date)
                saved_list.append(holiday_record) 
            active_list = self.inner_holiday

            if saved_list == active_list:
                return True
            else:
                return False 

def date_validation(date_string):
    format = "%Y-%m-%d"
    # checking if format matches the date
    res = True
    # using try-except to check for truth value
    try:
        res = bool(datetime.datetime.strptime(date_string, format))
    except ValueError:
        res = False

    return res
 

def main():
    # initiates instance of HolidayList class
    holiday_dict_list = HolidayList()
    holiday_number = holiday_dict_list.num_holidays()
    print("\nWelcome to the Holiday Calendar Manager App")
    print("-----------------")

    # If a JSON file exists already, load that else. else load starter
    file_exists = os.path.exists("data/saved_holidays.json")

    if file_exists:
        HolidayList.read_json(holiday_dict_list, "data\saved_holidays.json")
        print("Existing holiday list loaded.")
    else:
        print('Loading presaved holidays...')
        HolidayList.read_json(holiday_dict_list, starter_json_loc)
        
    try:
        print("Searching for new holidays...")
        HolidayList.scrapeHolidays(holiday_dict_list)
    except:
        print("Error loading new holidays.")

    holiday_number = holiday_dict_list.num_holidays()
    print("Calendar loaded.")
    print(f'There are {holiday_number} holidays in the system.\n')
    still_working = True
    while still_working:
        # Prints Main Menu from TXT file
        f = open(menu_text_loc)
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
                date = str(input("Date [YYYY-MM-DD]: "))
                while not date_validation(date):
                    date = str(input("Not a valid format. Try again. Date [YYYY-MM-DD]: "))
                else:
                    holiday_obj = Holiday(hol, date)
                    holiday_dict_list.addHoliday(holiday_obj)

            
            elif(selection == "2"): 
                print("\nRemove A Holiday")
                print("=============")
                remove_name = str(input("Holiday Name :"))

                holiday_dict_list.removeHoliday(remove_name)
                
            elif(selection == "3"):

                print("\nSaving Holiday List")
                print("=============")
                save_confirmation = input("Are you sure you want to save your changes? [Y/N]: ").strip().upper()
                save_options = ["Y", "N"]
                while save_confirmation not in save_options:
                    save_confirmation = input("Please select a valid option. [Y/N]: ").strip().upper()
                else:
                    if save_confirmation == "Y":
                        HolidayList.save_to_json(holiday_dict_list, "data\saved_holidays.json")
                        print("Your changes have been saved.")
                    else:
                        print("Save Cancelled. Returning to Main Menu")
                
            elif(selection == "4"):
                print("\nView Holidays")
                print("=============")
                # Strips entered values and creates integers
                calendar_years = [2020, 2021, 2022, 2023, 2024]
                year_selection = int(str(input("Which year? ")).strip())
                while year_selection not in calendar_years:
                    print("Not a valid year or currently not built in calendar.")
                    year_selection = int(str(input("Which year? ")).strip())
                else:
                    
                    week_selection = input("Which week? [#1-53, Leave blank for the current week]: ")

                    if week_selection == "":
                        current_week_num = holiday_dict_list.view_current_week()[0]
                        holiday_dict_list.displayHolidaysInWeek(holiday_dict_list.filter_holidays_by_week(year_selection, current_week_num))
                    else:    
                        while int(week_selection) < 1 or int(week_selection) > 53:
                            print("Week number must be between 1 and 53.")
                            week_selection = int(str(input("Which week? [#1-53]: ")).strip())
                        else:
                            filtered_holiday_list = holiday_dict_list.filter_holidays_by_week(year_selection, week_selection)
                            holiday_dict_list.displayHolidaysInWeek(filtered_holiday_list)


            elif(selection == "5"):
                print("\nExit")
                print("=============")
                exit_options = ["Y", "N"]
                # Determine if there is a saved JSON and if it matches inner_list
                save_file_exists = os.path.exists("data/saved_holidays.json")
                if file_exists:
                    if HolidayList.is_saved(holiday_dict_list):
                    # If matches, confirm exit
                        exit_confirmation = str(input("Are you sure you want to exit? [Y/N]: ")).strip().upper()
                        while exit_confirmation not in exit_options:
                            print("Please enter a valid option.")
                            exit_confirmation = str(input("Are you sure you want to exit? [Y/N]: ")).strip().upper()
                        else:
                            if exit_confirmation == "Y":
                                still_working = False
                            else:
                                print("Exit Cancelled. Returning to main menu.")
                    else:
                        # If different, warn user it is not saved
                        print("Are you sure you want to exit?")
                        print("Changes will be lost.")
                        exit_confirmation = str(input("[Y/N]: ")).strip().upper()
                        while exit_confirmation not in exit_options:
                            print("Please enter a valid option.")
                            exit_confirmation = str(input("Are you sure you want to exit? [Y/N]: ")).strip().upper()
                        else:
                            if exit_confirmation == "Y":
                                still_working = False
                            else:
                                print("Exit Cancelled. Returning to main menu.")
                else:
                    # If no file, warn user it is not saved
                    print("Are you sure you want to exit?")
                    print("Changes will be lost.")
                    exit_confirmation = str(input("[Y/N]: ")).strip().upper()
                    while exit_confirmation not in exit_options:
                        print("Please enter a valid option.")
                        exit_confirmation = str(input("Are you sure you want to exit? [Y/N]: ")).strip().upper()
                    else:
                        if exit_confirmation == "Y":
                            still_working = False
                        else:
                            print("Exit Cancelled. Returning to main menu.")
            else:
                print("\n !!Please Select A Valid Option!!") 
    else:
        # App Closes when Still Working is False
        print("\nGoodbye!\n")


if __name__ == "__main__":
    main();