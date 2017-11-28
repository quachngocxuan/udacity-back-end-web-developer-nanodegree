# My Neighbourhood Map Project

## Table of Contents

* [Project Overview](#project-overview)
* [How to Run](#how-to-run)
* [Features](#features)
* [Creadits](#credits)

## Project Overview

This project is to create a map application which displays nearby places. It uses the Google Maps API in Javascript service which supports to render a map.

## How to Run
It's very easy to run this test project. Double click on the ```index.html``` to open it on a web browser. You can the feed reader application above and testing result underneath. 

When the application asking for your location, please accept it. The map would be display with markers of places which are far from your location in a range of 500 metres.

## Features
The application has some following features:
- Clicking on the location's item to select it on the map
- Entering keyword to filter the location's list
- Clicking on the location's marker to display images which are captured near that place from Flickr

## Tables

This tool works on the database with three tables as below details:

Table "category"
```
 Column |           Type           |                       Modifiers                       
--------+--------------------------+-------------------------------------------------------
 title  | text                     | not null
 id     | integer                  | not null primary_key
```
 
Table "item"
```
 Column |  Type   |                      Modifiers                       
--------+---------+------------------------------------------------------
 title  | text    | not null
 desc   | text    | 
 cid    | text    | not null
 id     | integer | not null primary_key
```   
    
Table "user"
```
 Column   |           Type           |                    Modifiers                     
----------+--------------------------+--------------------------------------------------
 user     | text                     | not null primary_key
 password | text                     | 
```

## Credits
- Login form: thanks to [Simple login form](https://bootsnipp.com/snippets/featured/simple-login-form-bootsnipp-style-colorgraph)