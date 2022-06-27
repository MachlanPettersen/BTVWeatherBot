#Machlan Pettersen
#CS 021 // Spring 2022
#Final Project
#This script creates a Twitter bot that uses NOAA data to post weather updates
#to the city of Burlington.

#import tweepy!
import tweepy
#import numpy
import numpy as np
#import NOAA software dev kit (SDK)
from noaa_sdk import NOAA
#import request to be able to access NOAA api
import requests
#import json to manage the JSON files provided by NOAA
import json
#import statistics to find the most common weather type on the given day.
import statistics
from statistics import mode
#Stored keys to access the twitter api. These have been redacted for the sake of security.
consumer_key = #REDACTED
consumer_key_secret = #REDACTED
bearer_token = #REDACTED
access_token = #REDACTED
access_token_secret = #REDACTED
NOAA_token = #REDACTED

#Using the keys above to securely sign into twitter, granting api access.
auth = tweepy.OAuth1UserHandler(
  consumer_key, consumer_key_secret, access_token, access_token_secret
)
#Unlocking the twitter api
api = tweepy.API(auth)

#Defining the main function.
def main():

    #call the get_weather_data() function, and store returned variables.
    max_temp, min_temp, avg_wind_speed, most_frequent_weather = get_weather_data()

    #pass weather data to the construct_tweet function
    construct_tweet(max_temp, min_temp, avg_wind_speed, most_frequent_weather)

#define the get_weather_data() function.
def get_weather_data():
    #define the http address where weather data will be pulled from.
    noaa_data = f'https://api.weather.gov/gridpoints/BTV/88,56/forecast/hourly'
    #use requests to make an http call to the noaa address.
    r = requests.get(noaa_data)
    #use JSON to gather the data in a usable (JSON) format.
    d = json.loads(r.text)
    #declare an empty dictionary to store weather data, using hourly time as keys.
    weather_dict= {}
    #access the important information from the noaa api.
    props = d['properties']
    #loop through 18 hours of forecast, from 8AM to 2AM.
    for i in range(18):
        #split the timestamp into an hh:mm format.
        split_one = props['periods'][i]['startTime'].split('T')
        #update each weather_dict key with timestamp, temperature, wind speed, and short forecast data (such as 'partly cloudy','mostly sunny' etc.)
        weather_dict[i] = split_one[1].split(':')[0]+':00', props['periods'][i]['temperature'], props['periods'][i]['windSpeed'], props['periods'][i]['shortForecast']
    #create a list that represents the important values of weather_dict.
    weather_summary = list(weather_dict.values())
    #create empty lists to hold summaries of all values extracted from the JSON file.
    time_of_day = []
    temps_list = []
    wind_list = []
    short_forecast_list = []
    #loop through each tuple in the weather_summary list, sorting each value into the appropriate list.
    for i in range(len(weather_summary)):
        time_of_day.append(weather_summary[i][0])
        temps_list.append(weather_summary[i][1])
        wind_list.append(int(weather_summary[i][2].split(' ')[0]))
        short_forecast_list.append(weather_summary[i][3])

    #get relevant data for the bot to report.
    #max temp.
    max_temp = max(temps_list)
    #min temp.
    min_temp = min(temps_list)
    #average wind speed.
    avg_wind_speed = sum(wind_list) / len(wind_list)
    #short forecast ('partly cloudy','mostly sunny' etc.)
    most_frequent_weather = mode(short_forecast_list)

    #return relevant data to main.
    return max_temp, min_temp, avg_wind_speed, most_frequent_weather

#define the construct_tweet() function.
def construct_tweet(max_temp, min_temp, avg_wind_speed, most_frequent_weather):
    #write out the tweet with the most important weather data for the day. This can be improved upon in the future.
    tweet_string = f"Good morning Burlington! It's going to be {most_frequent_weather} today with a high around {max_temp}."
    #post the tweet using the twitter api.
    api.update_status(tweet_string)

main()
