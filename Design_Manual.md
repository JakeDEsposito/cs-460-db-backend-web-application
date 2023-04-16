# Design Manual
## Table of Contents
1. [Original Plan](#Original-Plan)
1. [Restructure](#Restructure)
1. [Login](#Login)
1. [Backend](#Backend)
	1. [Feature 1](#Feature-1)
	1. [Feature 2](#Feature-2)
	1. [Feature 3](#Feature-3)
	1. [Feature 4](#Feature-4)
	1. [Feature 5](#Feature-5)
	1. [Feature 6](#Feature-6)
1. [Security](#Security)
1. [ER Diagram](#ER-Diagram)
1. [Database Schema](#Database Schema)

## Original Plan
Our original design going forward was for us to make a distinct app for each individual page on the website. This turned out to be rather problematic for it was redundant because it did not take in to use "views."

## Restructure
We subsequently restructured the format of the Django project by creating one single and final app which contains "views" for what were apps in the previous version. This removes the redundancy of having multiple apps.

## Login
For our login page, we designed it to have several types of users in which the user can pick from. This determines what privilege level the user will have (given that their `ID #` permits this level.) As soon as a correct ID is inputted and the page is redirected to the respective "view," the next "view" must know which user logged into the previous page. This is accomplished by means of "Middleware," a tool that allows different pages to pass information on. We specifically opted to utilize the cookie method, which uses session cookies to transfer information between "views."

## Backend

### Feature 1

### Feature 2

### Feature 3

### Feature 4

### Feature 5

### Feature 6

## Security