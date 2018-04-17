[![Build Status](https://travis-ci.org/peterwade153/weconnect.svg?branch=challenge2)](https://travis-ci.org/peterwade153/weconnect)
[![Coverage Status](https://coveralls.io/repos/github/peterwade153/weconnect/badge.svg?branch=master)](https://coveralls.io/github/peterwade153/weconnect?branch=master)
# WeConnect-API

## Description

WeConnect provides a platform that brings businesses and individuals together. This platform 
creates awareness for businesses and gives the users the ability to write reviews about the 
businesses they have interacted with. 

## Functions
 - User signup
 - User login
 - User logout
 - User reset-password
 - Register a business
 - Update a business by user who registered it
 - View registered businesses
 - View a business by id
 - Delete a business by a user that registered it
 - Review a business
 - View reviews for a registered business
 
--- 

### End points

Request |       Endpoints                 |       Functionality
--------|---------------------------------|--------------------------------
POST    |  api/v2/auth/register           |        Register user
POST    |  api/v2/auth/login              |        Login user
POST    |  api/v2/auth/logout             |        Logout user
POST    |  api/v2/auth/reset-password     |        Reset-password
POST    |  api/v2/businesses              |        Register business
GET     |  api/v2/businesses              |        Get registered businesses
PUT     |  api/v2/businesses/id           |        Update registered business
GET     |  api/v2/businesses/id           |        Get a business 
DELETE  |  api/v2/businesses/id           |        Delete a business
POST    |  api/v2/businesses/id/reviews   |        Review a business
GET     |  api/v2/businesses/id/reviews   |        Get reviews for a business


---

## Create a virtual enviroment and activate it

$ python3 -m venv weconnect
to activate
$ source bin/activate

---

## Install requirements

$ pip install -r requirements.txt

## To run application

$ python run.py

## Usage

To test the api using postman(chrome extension) with the url below

$ https://weconnect-my.herokuapp.com/

To view the api documentation use the link below

$ https://peterweconnect.docs.apiary.io/

---
## User interfaces

To view the user interfaces click on the link below

$ https://peterwade153.github.io/

