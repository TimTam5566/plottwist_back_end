# Crowdfunding Back End
Tammy Healy
## Planning:
### Concept/Name
Plot Twist - You are the author: is a twist on a crowdfunding site where the user adds to a project the includes the start of a short story or poem.
Creativity is difficult to fit into the busy lives we lead and this allows people to have a short burst of creativity.

### Intended Audience/User Stories
For anyone who needs a short burst of creative energy to break up the monotony/stress of their day.

### Front End Pages/Functionality
- Log in
    -  log in/sign up for project submission
    - log in for/sign up supporter
    - profile information for both
- home page
    - featured projects
    - ability to choose to see all fundraisers
- Profile page
    - details of currently logged in users
    - change details of user accounts
    - delete user accounts?
- Projects page
    - ability to login/signup and create a projec
    - ability to login/signup to pledge
    - onectivity to update the pledge poem/story lines to the project pages

### API Spec


| URL              | HTTP Method | Purpose                             | Request Body | Success Response Code | Authentication/Authorisation |
| ---------------- | ----------- | ----------------------------------- | ------------ | --------------------- | ---------------------------- |
| /project/        | GET         | Fetch all projects                  | N/A.         | 200                   | None                         |
| /project/        | POST        | Create new project                  | JSON Payload | 201                   | Any authorised user          |
| /pledge/         | GET         | Fetch all Pledges                   | N/A          | 201                   | None                         |
| /pledge/.        | POST        | Create a pledge to a chosen project | JSOn Payload | 201                   | Any authorised user          |
| /project/pk/     | GET         | Fetch a specific project            | N/A          | 200                   | None                         |
| /pledge/pk       | GET         | Fetch a specific pledge             | N/A          | 200                   | None                         |
| /users/          | POST        | Create a new user                   | JSON Payload | 200                   | authorised user              |
| /users/pk/       | GET         | Fetch a specific user               | N/A          | 200                   | admin                        |
| /users/          | get         | Fetch all users                     | N/A          | 200                   | admin                        |
| /api-auth-token/ | POST        | Obtain auth Token                   | JSON Payload | authorised user       | none.                        |




### DB Schema
![](./database.drawio.svg)

# Link to Deployed project

https://plot-twist-you-are-the-author-fdc848555cc9.herokuapp.com/pledges/34/

# Screenshots users/api-token-auth

![Desktop Screenshot - POST Auth Token Create](.//plottwist/images/post_api_token_auth.png)
![Desktop Screenshot - POST User Create](.//plottwist/images/post_users_create_new.png)

# Screenshot pledges
![Desktop Screenshot - PUT Amend specific pledge](.//plottwist/images/put_pledges_pk.png)
![Desktop Screenshot - GET Retrieve all pledges](.//plottwist/images/get_pledges_all.png)

# Screenshots projects
![Desktop Screenshot - GET Retrieve specific project](.//plottwist/images/get_project_pk.png)
![Desktop Screenshot - POST Creat new project](.//plottwist/images/post_project_create_new.png)

# Instructions to register a new user (in insomnia)

Create a post
POST /users/ new user
enter JSON 
{
    "password": "(enter the password)", [CharField]
    "username": "(enter the username) [Charfield]
}

press send - dont forget to write details down.

# Instructions to create a new fundraiser/project

Create a post 
POST /project/ - create new project
enter JSON
{
    "title": [charfield]
	"description": [textfield]
	"goal": [integerfield]
	"image": [url feild]
	"genre": [charfield]
	"poemstart": [charfield]
	"storystart": [charfield]
	"is_open": [boolean]
}

Fill in the relevant details.
Hit send.