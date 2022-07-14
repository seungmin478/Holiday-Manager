import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from dataclasses import dataclass
from re import findall
from datetime import date as date_import
from sympy import nonlinsolve


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:  
    def __init__(self,name, date):
        self.name = name
        self.date = datetime.strptime(date, "%Y-%m-%d")      


  
    def __str__ (self):
        return str(self.name) + " - " + self.date.strftime("%Y-%m-%d")
        # String output
        # Holiday output when printed.
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []

    def addHoliday(self, holidayObj):
        if type(holidayObj) == Holiday:
            self.innerHolidays.append(holidayObj)
            print("Added " + str(holidayObj))
        else:
            print("You can only input a Holiday Object")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self, HolidayName, Date):
        for holidayObj in self.innerHolidays:
            if ( holidayObj.name == HolidayName and holidayObj.date == Date ):
                return holidayObj
        return None
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName, holiday):
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName:
                self.innerHolidays.remove(holiday)
                print(f"Success:\n{holiday} has been removed from the holiday list.")
                break  
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, filelocation):
        f = open(filelocation)
        data = json.load(f)
        f.close()
        for i in data["holidays"]:
            name = i["name"]
            date = i["date"]
            self.addHoliday(Holiday(name,date))
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        json_list = []
        json_dict = {"holidays": json_list}
        # Write out json file to selected file.
        with open(filelocation, "w") as jsonfile:
            for holiday in self.innerHolidays:
                holiday.date = str(holiday.date)
                json_list.append(holiday.__dict__)
            json.dump(json_dict, jsonfile, indent=4)
        jsonfile.close()
        # with open(filelocation, "w") as f:
        #     f.write(str(self.innerHolidays))
        #     print("Success:")
        #     print("Your changes have been saved")
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024] #All 5 years
        for year in years:

            url = (f"https://www.timeanddate.com/holidays/us/{year}?hol=33554809")
            response = requests.get(url)
                # print(response)
                # print(response.text)

            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", attrs = {"id":"holidays-table"}).find("tbody")
            rows = table.find_all("tr", attrs = {"class":"showrow"})
        #     print(rows)
                # print(table)

            

            for row in rows:
                namecells = row.find("a").text
        #         print(namecells)
        #         for elem in namecells:
        #             print(elem.get_text())
                # holidayweb = {}
                # holidayweb["name"] = namecells.text
                month = row.find("th").text.split(" ")[0]
                day = row.find("th").text.split(" ")[1]
                if month == "Jan":
                    month = "01"
                elif month == "Feb":
                    month = "02"
                elif month == "Mar":
                    month = "03"
                elif month == "Apr":
                    month = "04"
                elif month == "May":
                    month = "05"
                elif month == "Jun":
                    month = "06"
                elif month == "Jul":
                    month = "07"
                elif month == "Aug":
                    month = "08"
                elif month == "Sep":
                    month = "09"
                elif month == "Oct":
                    month = "10"
                elif month == "Nov":
                    month = "11"
                elif month == "Dec":
                    month = "12"
                dateYear = (f'{year}-{month}-{day}')
        #         print(type(dateYear))
                # holidayweb["date"] = dateYear
        #         print(holidayweb)
        #                 # scrapedholiday.append(holidayweb)
                self.addHoliday(Holiday(namecells,dateYear))                

        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        return len(self.innerHolidays)
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        holidays = list(filter(lambda holiday: holiday.date.isocalendar()[0] == year and
                        holiday.date.isocalendar()[1] == week_number, self.innerHolidays))
        return holidays
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, innerHoliday):
        if(len(innerHoliday) == 0):
            print("There are no holidays in this week")
        else:
            year = innerHoliday[0].date.isocalendar()[0]
            week = innerHoliday[0].date.isocalendar()[1]
            print("The holidays for the year {} and week {} are:".format(year,week))
            for holiday in innerHoliday:
                print(holiday)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    # def getWeather(weekNum):
    #     pass
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        print("These are the holidays for the current week")
        print("============================================")
        year = datetime.now().isocalendar()[0]
        week = datetime.now().isocalendar()[1]
        self.displayHolidaysInWeek(self.filter_holidays_by_week(year,week))
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



def main():
    exit = False
    holidayList = HolidayList()
    holidayList.scrapeHolidays()
    holidayList.read_json('holidays.json')
    print(f"There are {len(holidayList.innerHolidays)} holidays stored in the system")

    while(True):
        print("\nHoliday Menu\n==============")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        menuInput = input("Please enter the number for the menu options (1-5):")

        if menuInput.strip() == "1":
            name = input("Enter a holiday name: ")
            date_string = input("Enter a holiday date (YYYY-MM-DD): ")
            # date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            if ( holidayList.findHoliday(name, date_string) is None ):
                holidayList.addHoliday(Holiday(name,date_string))
        if menuInput.strip() == "2":
            name = input("Enter a holiday name: ")
            date_string = input("Enter a holiday date (YYYY-MM-DD): ")
            # date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            holidayList.removeHoliday(name,date_string)
        if menuInput.strip() == "3":
            saveChoice = input("Are you sure you want to save your changes? [y/n]")
            if saveChoice == 'y':
                holidayList.save_to_json('holidaysoutput.json')
                print("Your changes have been saved!")
                
            else:
                print("File will not be saved and data will be lost.")
                
        if menuInput.strip() == "4":
            incinput = True

            while(incinput):
                try:
                    yearChoice = input("Which year?: ")
                    weekChoice = input("Which week? [1-53, leave blank for current week]: ")

                    if(weekChoice) !="":
                        if(int(weekChoice) <= 53 and int(weekChoice) >= 1):
                            # weekChoice = int(weekChoice)
                            holidayList.displayHolidaysInWeek(holidayList.filter_holidays_by_week(yearChoice,weekChoice))
                            incinput = False
                            break
                        else:
                            print("Please input an integer between 1 and 53")
                    else:
                        # week = datetime.now().isocalendar()[1]
                        # print(week)
                        incinput = False
                        holidayList.viewCurrentWeek()
                        break
                except:
                    print("Input a integer")        
            # holidayList.displayHolidaysInWeek(holidayList.filter_holidays_by_week(yearChoice,weekChoice))

        if menuInput.strip() == "5":
            exitChoice = input("Would you like to exit? [yes/no]:")
            if exitChoice == "yes":
                print("Exiting")
                exit = True
                break
            else:
                exit = False
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the 
    # program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





