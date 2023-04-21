# Design Manual
## *University database*
## Table of Contents
1. [Original Plan](#Original-Plan)
1. [Restructure](#Restructure)
1. [Login](#Login)
1. [Backend](#Backend)
	1. [Tools](#Tools)
	1. [Database details](#Database-details)
1. [ER Diagram and Database Schema](#ER-Diagram-and-Database-Schema)
1. [Security](#Security)


## Original Plan
Our original design going forward was for us to make a distinct app for each individual page on the website. This turned out to be rather problematic for it was redundant because it did not take in to use "views."

## Restructure
We subsequently restructured the format of the Django project by creating one single and final app which contains "views" for what were apps in the previous version. This removes the redundancy of having multiple apps.

## Login
For our login page, we designed it to have several types of users in which the user can pick from. This determines what privilege level the user will have (given that their `ID #` permits this level.) As soon as a correct ID is inputted and the page is redirected to the respective "view," the next "view" must know which user logged into the previous page. This is accomplished by means of "Middleware," a tool that allows different pages to pass information on. We specifically opted to utilize the cookie method, which uses session cookies to transfer information between "views."

## Backend

### Tools
For this project, we used Python programing language for the backend, and HTML (and Django templates) for the front end. We used Django templates to pass Python objects through it in order to have a dynamic HTML. 

Python files:

1. __ init __.py: This file was created automatically to allow us to define any variable at the package level.\

1. admin.py: This file is has also been created automatically; it is not used directly in this project. (we created our own admin page from scratch) \
 
1. apps.py: This file was created to assist users in including any application configuration for the program. It is used to configure some of the application's attributes. \

1. forms.py: A Django forms file that does the following:
	1. Prepares and arranges data for rendering. 
	1. Create HTML forms.
	1. Receiving and processing the user's submitted forms.\

1. models.py: This is where the access of our university database happen. Models access and manage data through Python objects. 
1. views.py: This python file holds Python views that are classes or methods that take a web request and provide a web response. (Like HTTP or HTML) 
1. urls.py: Here is where we use "urlpatterns" tuples; we define the mapping between URLs and views by importing module and adding a path function in urlpatterns[] list.
1. manage.py : A command-line utility that allows us to execute our Django project in various ways.

<br>

### Database details

MySQL queries were used to manage the database of this project. 
The database is approximately of size 4-5 gigabytes. 


## ER Diagram and Database Schema

In this section, we are presenting university database's entity relationship diagram (ERD) along with it's schema (where in the diagram, it shows entities are represented)

![ER diagram and Schema](./images/ER-schema.png)

<br>
<br>

## Security
This project has simple security components. There is no cryptographic concepts  of any sort involved. Each user cannot access other users' account; the system checks the correctness of inputed passwords for each user. We also take advantage of MySQL's built in user creation queries and user system.