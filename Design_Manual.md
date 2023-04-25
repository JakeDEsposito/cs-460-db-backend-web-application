# Design Manual
## *University database*
## Table of Contents
1. [Introduction](#introduction)
1. [Goals and objectives](#goals-and-objectives) 
1. [Notes](#notes) 
	1. [Original Plan](#original-plan)
	1. [Restructure](#restructure)
1. [Backend](#backend)
	1. [Tools](#tools)	
	1. [Components](#components)
	1. [Login functionalities](#login-functionalities) 
	1. [Database details](#database-details)
1. [ER Diagram and Database Schema](#er-diagram-and-database-schema)
1. [Security](#security)
1. [Credits](#credits)  

## Introduction
This manual discusses and displays, in great detail, the design of our project website. From backend to front end, discussing files for each part of the website. It describes the structure, tools, diagrams and other components of the project website. 

## Goals and objectives 
This project is intended to provides users (Admins, professors, students) a highly user-friendly experience for running database queries and searches display desired results from the *university* database. It also helps developers to maintain the database, resolve received complaints from users, update features for each type of users and add new user type if needed.  

## Notes

### Original Plan
Our original design going forward was for us to make a distinct app for each individual page on the website. This turned out to be rather problematic for it was redundant because it did not take in to use "views."

### Restructure
We subsequently restructured the format of the Django project by creating one single and final app which contains "views" for what were apps in the previous version. This removes the redundancy of having multiple apps.

## Backend

### Tools
For this project, we used Python programing language for the backend, and HTML (and Django templates) for the front end. We used Django templates to pass Python objects through it in order to have a dynamic HTML. In addition, Markdown composer, MySQLWorkbench and GitHub all have been used in this project.
<br></br>
- Markdown composer: used to create both user manual and design manual.
- MySQLWorkbench: used to create the ER diagram for *university's*  database.
- Github: used to combine code from different group members (in the case where we used different devices).
<br></br>
### Components 

- Python files: 

All following python files are under *university* file in the cs-460-db-backend-web-application repository. 

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
<br></br>
- HTML files:

All following HTML files are under *Template* file in the cs-460-db-backend-web-application repository. 

1. admin :
	1.  Admin.html: This is where the homepage of an administrator can be displayed, where they can use the three below functionalities. Along with a *logout* button.
	1. F1.html: This is the interface of Functionality 1 of the project, that is, allowing the admin to indirectly run queries that list professors' sorting them by either name, department or salary; in an ascending or descending order.
	1. F2.html: This HTML file displays a table to the user of a list of professors' salaries. For each department, view the minimum, maximum and average salary in that department.
	1. F3.html: It displays the form that requests the user to input a professor's name, a given year and semester desired to display a professor's performance.
1. Instructor :
	1. instrutor.html: This is where the homepage of an instructor can be displayed, where they can use the two below functionalities. Along with a *logout* button.
	1. F4.html: Displays the interface of functionality 4 of the project. Where the user is prompted to input a desired year and semester to view each course and section that has been taught by the user and  the number of students in each section.
	1. F5.html: Similar to F4, this html file is responsible to view a course information with student's names and identification numbers by prompting the user to input a course name, year and semester.  
1. Student :
	1. student.html: This is where the homepage of a student can be displayed. Along with a logout button. The student user type has or is allowed to run one functionality (F6) which also being held under this HTML file. Student is prompted to select a year and semester to view a table of courses offered. 
<br></br>
- Images: 

This file collects all the images and diagrams needed for mainly user and design manuals.
<br></br>
- CSS files: 

There is a single css file under *static* file in the cs-460-db-backend-web-application repository. <br></br>
<span style="padding-left:5em"> -- styles.css: collection of all css styles for the whole website. </span><br>
<br></br>
### Login functionalities
For our login page, we designed it to have several types of users in which the user can pick from. This determines what privilege level the user will have (given that their `ID #` permits this level.) As soon as a correct ID is inputted and the page is redirected to the respective "view," the next "view" must know which user logged into the previous page. This is accomplished by means of "Middleware," a tool that allows different pages to pass information on. We specifically opted to utilize the cookie method, which uses session cookies to transfer information between "views."
<br></br>
### Database details

MySQL queries were used to manage the database of this project. 
The database is approximately of size 4-5 gigabytes. All members used the same database by connecting to one of our member's root user account virtually. 

<br></br>
## ER Diagram and Database Schema

In this section, we are presenting university database's entity relationship diagram (ERD) along with it's schema (where in the diagram, it shows entities are represented)

![ER diagram and Schema](./images/ER-schema.png)

<br></br>
## Security
This project has simple security components. There is no cryptographic concepts  of any sort involved. Each user cannot access other users' account; the system checks the correctness of inputed passwords for each user. We also take advantage of MySQL's built in user creation queries and user system.
<br></br>
## Credits

This project was created by Layan Alnamlah, Ethan Arnold, George Crochiere and Jake D'Esposito, under the supervision of Dr.Hou, Clarkson University, spring 2023.
