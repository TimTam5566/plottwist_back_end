plot_twist_backend
Tamala Healy
Planning:
Concept/Name

Plot Twist - You are the author: is a twist on a crowdfunding site where the user adds to a project the includes the start of a short story or poem.
Creativity is difficult to fit into the busy lives we lead and this allows people to have a short burst of creativity.
Intended Audience/User Stories
For anyone who needs a short burst of creative energy to break up the monotony/stress of their day
Front End Pages/Functionality
Log in
log in/sign up for project submission
log in for/sign up supporter
profile information for both
home page
featured projects
ability to choose to see all fundraisers
Profile page
details of currently logged in users
change details of user accounts
delete user accounts?
Projects page
ability to login/signup and create a projec
ability to login/signup to pledge
conectivity to update the pledge poem/story lines to the project pages
API Spec
{{ Fill out the table below to define your endpoints. An example of what this might look like is shown at the bottom of the page.
It might look messy here in the PDF, but once it's rendered it looks very neat!
It can be helpful to keep the markdown preview open in VS Code so that you can see what you're typing more easily. }}
URL
HTTP Method
Purpose
Request Body
Success Response Code
Authentication/Authorisation
/project/
GET
Fetch all projects
N/A
200
None
/project/
POST
Create new project
JSON Payload
201
Any logged user
/pledge/
GET
Fetch all pledges
N/A.
200.
None
/pledge/
POST.
Create/add a pledge.
JSON Payload
201
Any logged supporter
/project/1/
GET.
Fetch a specific pledge
N/A
200
None
/pledge/1/
Get.
Fetch a specific pledge
N/A
200
specific logged in user
/user/
GET
Fetch all users
N/A
200
None
/user/1/
GET
Fetch a single user.
N/A
200
specific logged in user
/user/
POST.
Create a user
JSON Payload
201
specific logged in user
/supporter/
GET.
Fetch all supporters.
N/A
none


/supporter/1/
GET.
Fetch a specific supporter
N/A.
specific logged in user


/supporter/
POST.
Create/Add a supporter
JSON Payload
201
specific logged in user

DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )
