from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime 
from selenium.webdriver.support.ui import Select

URL = "https://mojinfo.knapp.at/Account/Login?ReturnUrl=%2FREGAttendance"
username = "petra.totar"
password = "121488Ha.."

def build_driver():
    opts = Options()
    opts.add_experimental_option("detach", True)

    service = Service()
    driver = webdriver.Edge(options = opts, service = service)
    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)
    return driver, wait, actions

def fillHours(hourList, workingDays, location, driver, wait):
    print("here")
    print(hourList)
    print(workingDays)
    #start, edn, step
    
    for x in range(0, len(hourList) - 1, 2):
        addHours = wait.until(EC.element_to_be_clickable((By.ID, "btnAddRecord")))      
        addHours.click()

        toggle = wait.until(EC.element_to_be_clickable((By.ID, "vecDniCheckBox")))
        toggle.click()

        datesField = wait.until(EC.element_to_be_clickable((By.ID, "Datumi")))
        datesField.clear()
            
        for i in range(len(workingDays)):
            datesField.send_keys(workingDays[i])
            if i < len(workingDays) - 1:
                datesField.send_keys(",")

        startTime = wait.until(EC.element_to_be_clickable((By.ID, "EventStart")))
        startTime.clear()
        startTime.send_keys(hourList[x])

        endTime = wait.until(EC.element_to_be_clickable((By.ID, "EventEnd")))
        endTime.clear()
        endTime.send_keys(hourList[x + 1])

        if (x == 2):
            eventField = Select(wait.until(EC.element_to_be_clickable((By.ID, "SifraDogodka"))))
            eventField.select_by_value("MAK")

        locationField = Select(wait.until(EC.element_to_be_clickable((By.ID, "SifraLokacije"))))
        locationField.select_by_value(location)

        saveButton = wait.until(EC.element_to_be_clickable((By.ID, "btnOk")))
        saveButton.click()

        spinner = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner-blade")))

def main():
    driver, wait, actions = build_driver()
    
    try:
        driver.get(URL)
        
        user = wait.until(EC.element_to_be_clickable((By.ID, "UserName")))
        user.send_keys("petra.totar")
        
        psw = wait.until( EC.element_to_be_clickable((By.ID, "Password")))
        psw.send_keys(password + Keys.ENTER)
        
        navLink = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Mjesečna')]")))
        navLink.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[contains(@class,'saop-tr-main') and @tabindex]")))

        rows = driver.find_elements(By.XPATH,"//tbody/tr[contains(@class,'saop-tr-main') and @tabindex]")
        
        workingDays = []
        a = input("Are weekend days work days as well (y/n)?  ")
        a = a.lower()
        print(a)
        while a != 'n' and a != 'y':
            print("Please enter y or n")
            a = input("Are weekend days work days as well (y/n)?  ")
            a = a.lower()
        
        while len(b := input("Until which day are you filling up to (dd format)? ")) != 2:
            print("Please enter exactly two digits (e.g. 05, 21).")
        
        for row in rows:
            date = row.find_element(By.XPATH, "./td[3]").text.strip()
            status = row.find_element(By.XPATH, "./td[4]").text.strip()
            weekday = row.find_element(By.XPATH, "./td[5]").text.strip()
            
            dDate = datetime.strptime(date, '%d.%m.%Y').weekday()

            if (date.startswith(b)):
                break

            if(dDate > 5):
                if(a == 'n'):
                    #print("its weekday, u dont work")
                    continue

            if (status == '' or status == 'Greška'):
                workingDays.append(date)

        print(workingDays)

        #u gotta do this 3 times
        workHours = []
        while len(choice := input("For which location are you putting hours in?\n 1 - KNAPP HR Office\n 5 - GRAZ Office\nYour choice; ")) > 2:
            print("Please enter exactly two digits (e.g. 05, 21).")
        
        print(choice)
        match choice:
            case "1":
                #KNAP HR OFFICE
                choice = "0001"
                workHours = ['07:00:00', '12:00:00','12:00:01', '12:30:01', '12:30:02', '15:00:00']
            case "5":
                # GRAZ TIME
                choice = "0005"
                workHours = ['08:00:00', '12:00:00','12:00:01', '12:30:01', '12:30:02', '17:00:00']
        
        fillHours (workHours, workingDays, choice, driver, wait)


        
    except Exception as e:
      print(e)

if __name__ == "__main__":
    main()
