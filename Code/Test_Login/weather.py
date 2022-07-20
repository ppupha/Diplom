#Downloading weather data using Python as a CSV using the Visual Crossing Weather API
#See https://www.visualcrossing.com/resources/blog/how-to-load-historical-weather-data-using-python-without-scraping/ for more information.
import csv
import codecs
import urllib.request
import urllib.error
import sys

def getWeatherDay():
    CSVFile = open('Vietnam 2021-08-05 to 2022-06-10.csv', newline='')
    CSVText = csv.reader(CSVFile)
    RowIndex = 0
    NeedData = []

    for Row in CSVText:
        if RowIndex == 0:
            pass
        else:
            NeedData.append(Row[5])
        RowIndex += 1
    return NeedData


def getWeatherHour():
    CSVFile = open('Vietnam 2021-08-05 to 2021-08-19.csv', newline='')
    CSVText = csv.reader(CSVFile)
    RowIndex = 0
    NeedData = []

    for Row in CSVText:
        if RowIndex == 0:
            pass
        else:
            NeedData.append(Row[3])
        RowIndex += 1
    return NeedData


