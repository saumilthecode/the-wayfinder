

#This file is used to get the gps from an image. Do note that the image has to be a jpg to get the correct details. In order to maintain the metadata, save the image in google drive before downloading to PC
from selenium import webdriver
import webbrowser
from flask import Flask, render_template
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
import time 
import subprocess
import webbrowser
from gmplot import gmplot
import string
import os
import PIL.Image
import cmath


#image goes here
img = PIL.Image.open("Sample_1.JPG") 
#img = PIL.Image.open("Sample_2.JPG") 
#img = PIL.Image.open("Sample_3.JPG") 


import PIL.ExifTags

exif ={
    PIL.ExifTags.TAGS[k]:v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}
exif['GPSInfo']

#test 1: Positive
#this should print out the overall coords of the location
print(exif['GPSInfo'])

north= exif['GPSInfo'][2]
east= exif['GPSInfo'][4]

#test 2: Positive
#This should only show the north and east coords
# print(north)
# print(east)

#Turns values into gmplot values
lat= ((((north[0] *60) + north[1]) *60) + north[2]) /60 /60
long= ((((east[0] *60) + east[1]) *60) + east[2]) /60 /60

lat,long= float(lat), float(long)

#test 3: Positive
#print(lat,long)



gmap=gmplot.GoogleMapPlotter(lat,long,12)
gmap.marker(lat,long, "cornflowerblue")
gmap.draw("location.html")

from geopy.geocoders import Nominatim
geoLoc =Nominatim(user_agent= "GetLoc")


#webbrowser.open("location.html", new=2)
time.sleep(4)
print(lat,long)

#Loading Selenium Webdriver 

options=Options()
options.add_experimental_option("detach",True)

driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                         options=options)


chrome_driver_path = 'C:\Program Files (x86)\Google\Chrome\Application.exe'
#This should be your chrome driver path. mine is the above mentioned one. Yours will be different.

# Create a new instance of the Chrome driver
#driver = webdriver.Chrome(executable_path=chrome_driver_path)
# Open Google Maps
# driver.get("https://www.google.co.uk/maps/@1.3739933,103.8427279,18z/data=!3m1!4b1!4m2!6m1!1s10yPjhbcHUHVXMGrTgiQynp444Rf4XoI?entry=ttu")
# driver.maximize_window()


#creating a webbrowser to show lat,long

location_lat= float(lat) 
location_long= float(long)




output_part1= f"The Latitude and Longitude of the location is: {float(lat)} , {float(long)}. "
output_part2= "You can copy these values and paste it into this website : https://shorturl.at/jpqvT"
html_content=f"<html> <head> </head> <h1> {output_part1}  <br> <br>  <body> </body> <b1>  {output_part2}  </b1> <html>"
with open("index.html", "w") as html_file:
    html_file.write(html_content)
    print("Html File Created")


try:
    
  
    maps_url = "https://www.google.com/maps/@1.3734742,103.8332197,15z?entry=ttu"
    #custom map: https://shorturl.at/jpqvT
   
    driver.get(maps_url)
    driver.maximize_window()
    
    # Wait for the search box to be clickable
    search_box = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )

    # Enter a location value
    search_box.send_keys(f"{float(lat)}, {float(long)}")

    # Press ENTER to trigger the search
    ActionChains(driver).send_keys(Keys.ENTER).perform()

    # Wait for the search results to load (you may need to adjust the time depending on your internet speed)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "hArJGc")))
    


except Exception as e:
    print(f"An error occurred: {e}")







