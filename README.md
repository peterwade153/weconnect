[![Build Status](https://travis-ci.org/peterwade153/weconnect.svg?branch=challenge2)](https://travis-ci.org/peterwade153/weconnect)
[![Coverage Status](https://coveralls.io/repos/github/peterwade153/weconnect/badge.svg?branch=master)](https://coveralls.io/github/peterwade153/weconnect?branch=master)
# weconnect
WeConnect provides a platform that brings businesses and individuals together. This platform 
creates awareness for businesses and gives the users the ability to write reviews about the 
businesses they have interacted with. 

## Functions
 - User signup
 - user login
 - user logout
 - user reset-password
 - register a business
 - update a business by user who registered it
 - view registered businesses
 - view a business by id
 - delete a business by a user that registered it
 - review a business
 - view reviews for a registered business
## Create a virtual enviromenet and activate it
$ python3 -m venv weconnect
to activate
$ source bin/activate
## Install requirements
$ pip install -r requirements.txt

## To run application
$ python app.py
## Usage
To test the api using postman(chrome extension) with the url below

$ https://weconnect-my.herokuapp.com/

To view the api documentation use the link below

$ https://peterweconnect.docs.apiary.io/
