#!/usr/bin/env python

__author__ = 'cmjoy136'

import requests
import json
import turtle
import time


# const
astro_API = 'http://api.open-notify.org/astros.json'
iss_loc = 'http://api.open-notify.org/iss-now.json'


def astros_in_space():
    '''returns number of astronauts and their names as a list'''
    r = requests.get(astro_API)
    d = r.json()
    people_on_iss = d["people"]
    in_space=[d["number"], ]
    for person in people_on_iss:
        pers_dat= (person["name"])
        in_space.append(pers_dat)
    return in_space


def find_iss():
    '''finds current ISS location'''
    r=requests.get(iss_loc)
    d=r.json()
    iss_pos=d["iss_position"]
    timestamp=d["timestamp"]
    iss_lon=iss_pos["longitude"]
    iss_lat=iss_pos["latitude"]

    return float(iss_lon), float(iss_lat), float(timestamp)


def iss_pass(lon, lat):
    '''Returns timetamp of given location'''
    i_pass='http://api.open-notify.org/iss-pass.json'
    url=i_pass + "?lat=" + str(lat) + "&lon=" + str(lon)
    resp=requests.get(url)
    res=resp.json()
    return res["response"][1]["risetime"]


def turtle_stuff(iss_lon, iss_lat):
    '''handles turtle initialization code'''
    # Screen
    screen=turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic("map.gif")
    screen.addshape("iss.gif")
    screen.setworldcoordinates(-180, -90, 180, 90)

    # ISS Turtle
    iss=turtle.Turtle()
    iss.shape("iss.gif")
    iss.penup()
    iss.goto(iss_lon, iss_lat)

    # IN Turtle
    indy_pos=(-86.15804, 39.76838)
    indy=turtle.Turtle()
    indy.penup()
    indy.shape('triangle')
    indy.shapesize(0.25, 0.25)
    indy.color('yellow')
    indy.goto(indy_pos[0], indy_pos[1])
    indy.write(time.ctime(iss_pass(indy_pos[0], indy_pos[1])))
    screen.exitonclick()


def main():
    astronauts=astros_in_space()
    iss_lon, iss_lat, timestamp=find_iss()

    print('Timestamp: {} Latitude: {}, Longitude: {}'.format(
        timestamp, iss_lon, iss_lat))
    print('This many in space on ISS: {}\nList of ppl in Space: {}'.format(
        astronauts[0], str(astronauts[1:])))
    turtle_stuff(iss_lon, iss_lat)


if __name__ == '__main__':
    main()
