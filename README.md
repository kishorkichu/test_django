====================================================================
====================================================================
			Steps
====================================================================


1.Make sure Python 3.7x and Pipenv are already installed.(Note that the attached progam is in python3.9. Check requirement.txt files for package informations)
    Clone the repo and configure the environment:


2.Set up the initial migration for our custom user models in user and build the database.

      python manage.py makemigrations user
      python manage.py migrate
      python manage.py runserver

3.Endpoints

	Register- (http://127.0.0.1:8000/api/register)
    Login- (http://127.0.0.1:8000/api/login)
    Logout- (http://127.0.0.1:8000/api/logout)
    Update user - (http://127.0.0.1:8000/api/updateUser)
	ListUserView-  (http://127.0.0.1:8000/api/listUser)



======================================================================
			Example Jsons
======================================================================

1. Register- (http://127.0.0.1:8000/api/register)
 
Input:
{
    "name": "test",
    "email": "tester@test.com",
    "password": "test123"
}

Output:
{
    "id": 5,
    "name": "test123",
    "email": "test123@test.com"
}
======================================================================
2. Login- (http://127.0.0.1:8000/api/login)

Here user can login with either Email address or the username given during the registration.

Input:
{
    "email": "",
    "password": ""
}

Output:
{
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6InVzZXIuaWQiLCJleHAiOjE2MjgxNjQ2ODYsImlhdCI6MTYyODE2MTA4NiwiZmlyc3RfbmFtZSI6ImZpcnN0X25hbWUifQ.Fg6i9Yc17JAa3BuRQwq6-M99lIoFezVqNTlNtpm-X3Y"
}

======================================================================
3.Logout- (http://127.0.0.1:8000/api/logout)
Input:
	Just call the api

Output:
{
	'message':' Logged out successfully'
}
======================================================================
4.Update user - (http://127.0.0.1:8000/api/updateUser)
Input:
{
    "email": "test123",
    "password": "test123",
    "phone": "88888",
    "city": "city123",
    "address": "addr123"
}

Output:
{
    "message": "Updated successfully",
    "Username": "test123",
    "UserEmail": "test123@test.com",
    "Phone": "88888",
    "City": "city123",
    "Address": "addr123"
}

======================================================================
5.ListUserView-  (http://127.0.0.1:8000/api/listUser)
To get all the user informations
Input:
     Just call the call the api

Output:
    List out all the users with ID,Name and Email
======================================================================
======================================================================
======================================================================
