User models and how URLs work
"""
HOW URLS WORK:

These URLs are "nested" under /users/ in your main urls.py

So the full paths are:
- GET  /users/        → List all users
- POST /users/        → Create new user (register)
- GET  /users/1/      → Get user with ID 1
- GET  /users/42/     → Get user with ID 42

<int:pk> means "capture a number and call it pk"
"""
```

---

## 🔄 How They Work Together

Here's what happens when someone **registers** (creates an account):
```
FRONTEND (React)                    BACKEND (Django)
─────────────────                   ─────────────────
1. User fills signup form
   {username, email, password}
           │
           ▼
2. React sends POST to /users/
           │
           ▼
                                    3. urls.py routes to CustomUserList.post()
                                               │
                                               ▼
                                    4. views.py receives request
                                       Creates serializer with data
                                               │
                                               ▼
                                    5. serializers.py validates data
                                       - Is username unique?
                                       - Is email valid?
                                               │
                                               ▼
                                    6. serializer.save() calls create()
                                       - Uses create_user() to hash password
                                               │
                                               ▼
                                    7. models.py CustomUser saved to database
                                               │
                                               ▼
                                    8. Response sent back (201 Created)
           │
           ◄────────────────────────────────────
           ▼
9. React receives success
   Redirects to login page


PROJECTS APP

APPS CONFIGURATION

WHAT THIS DOES:
        When Django starts up and this app is "ready", import the signals module.
        
        SIGNALS are like "event listeners" in Django.
        They let you run code automatically when certain things happen.
        
        Example: "When a new pledge is created, automatically update the project's current_content"

HOW PROJECTS AND PLEDGES RELATE
# 🔄 How Project & Pledge Relate
```
┌─────────────────────────────────────────────────────────────┐
│                         PROJECT                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ id: 1                                                │    │
│  │ title: "The Haunted Lighthouse"                     │    │
│  │ owner: User #5 (Sarah)                              │    │
│  │ starting_content: "The lighthouse stood alone..."   │    │
│  │ current_content: "The lighthouse stood alone...     │    │
│  │                   The door creaked open...          │    │
│  │                   A ghost appeared..."              │    │
│  │ goal: 10                                            │    │
│  │ is_open: True                                       │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           │ project.pledges.all()            │
│                           ▼                                  │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ PLEDGE #1        │  │ PLEDGE #2        │                 │
│  │ supporter: Tim   │  │ supporter: Alex  │                 │
│  │ amount: 2        │  │ amount: 1        │                 │
│  │ add_content:     │  │ add_content:     │                 │
│  │ "The door        │  │ "A ghost         │                 │
│  │  creaked open.." │  │  appeared..."    │                 │
│  └──────────────────┘  └──────────────────┘                 │
└─────────────────────────────────────────────────────────────┘



projects/urls.py
"""
FULL URL MAP (assuming projects app is at /projects/):

/projects/                    GET=list all, POST=create project
/projects/1/                  GET=detail, PUT=update project
/projects/1/pledges/          POST=create pledge for project 1
/projects/pledges/            GET=list all pledges, POST=create pledge
/projects/pledges/1/          GET=detail, PUT=update pledge
"""
```

---

## 🔄 The Complete Data Flow

Here's what happens when someone **contributes to a story**:
```
┌─────────────────────────────────────────────────────────────────────┐
│  REACT FRONTEND                                                      │
│  User clicks "Add Contribution" on project page                      │
│  Fills in: add_content = "The hero drew their sword!"               │
│  Clicks Submit                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ POST /projects/1/pledges/
                                    │ Headers: Authorization: Token abc123
                                    │ Body: {"add_content": "The hero...", "amount": 1}
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│  urls.py                                                             │
│  path('<int:project_id>/pledges/', PledgeListCreate.as_view())      │
│  Routes to → PledgeListCreate.post()                                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  views.py - PledgeListCreate.post()                                  │
│  1. Check user is authenticated ✓                                    │
│  2. Find project with id=1 ✓                                         │
│  3. Create serializer with data                                      │
│  4. Validate data                                                    │
│  5. serializer.save(supporter=request.user)                         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  serializers.py - PledgeSerializer                                   │
│  Validates the data, creates Pledge object, saves to database       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  models.py - Pledge saved to database                                │
│  id: 5                                                               │
│  project_id: 1                                                       │
│  supporter_id: 3                                                     │
│  add_content: "The hero drew their sword!"                          │
│  amount: 1                                                           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼  🔔 SIGNAL FIRES! (post_save)
┌─────────────────────────────────────────────────────────────────────┐
│  signals.py - append_pledge_to_project()                             │
│  1. Detects new pledge was created                                   │
│  2. Gets the project (id=1)                                          │
│  3. Appends add_content to project.starting_content                 │
│  4. Saves project                                                    │
│                                                                      │
│  BEFORE: "Once upon a time... A dragon appeared!"                   │
│  AFTER:  "Once upon a time... A dragon appeared!                    │
│           The hero drew their sword!"                                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Response sent back to React                                         │
│  Status: 201 Created                                                 │
│  Body: {"id": 5, "add_content": "The hero...", ...}                 │
└─────────────────────────────────────────────────────────────────────┘

CLOUDINARY
1. Django Does the Heavy Lifting
You don't write any Cloudinary-specific code in your views or serializers! The STORAGES setting makes it automatic.
2. FormData vs JSON
javascript// ❌ WRONG - JSON can't handle files

fetch('/projects/', {
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Test', image: ??? })  // Can't include file!
})

// ✅ CORRECT - FormData handles files
const formData = new FormData();
formData.append('image', file);
fetch('/projects/', {
  body: formData  // Browser sets Content-Type automatically
})
```

### 3. **URL Structure**
```
OLD (Heroku local):
https://plot-twist-you-are-the-author.herokuapp.com/media/project_images/lighthouse.jpg
       └── Your Heroku app ──────────────────────────┘└── Local file path ──────────┘

NEW (Cloudinary):
https://res.cloudinary.com/dpki1hl3c/image/upload/v1/media/project_images/lighthouse_abc123
       └── Cloudinary CDN ─┘└─ Your cloud ┘              └── Path in Cloudinary ─────────┘

I integrated Cloudinary for image storage because Heroku has an ephemeral filesystem - files disappear after 24 hours. 
I configured Django's STORAGES setting to automatically route all media uploads to Cloudinary. 
The frontend sends images via FormData, Django's ImageField handles validation, and the cloudinary-storage package transparently uploads to their CDN. 
The database only stores the URL, and images are served directly from Cloudinary's global CDN for fast loading.

Here's every URL your backend responds to:
```
┌─────────────────────────────────────────────────────────────────────┐
│  ENDPOINT                        METHOD    WHAT IT DOES             │
├─────────────────────────────────────────────────────────────────────┤
│  /                               GET       Welcome message          │
│  /admin/                         GET       Django admin panel       │
├─────────────────────────────────────────────────────────────────────┤
│  /api-token-auth/                POST      Login (get token)        │
├─────────────────────────────────────────────────────────────────────┤
│  /users/                         GET       List all users           │
│  /users/                         POST      Register new user        │
│  /users/1/                       GET       Get user #1              │
├─────────────────────────────────────────────────────────────────────┤
│  /projects/                      GET       List all projects        │
│  /projects/                      POST      Create new project       │
│  /projects/1/                    GET       Get project #1 + pledges │
│  /projects/1/                    PUT       Update project #1        │
│  /projects/1/pledges/            POST      Add pledge to project #1 │
│  /projects/pledges/              GET       List all pledges         │
│  /projects/pledges/              POST      Create pledge            │
│  /projects/pledges/1/            GET       Get pledge #1            │
│  /projects/pledges/1/            PUT       Update pledge #1         │
└─────────────────────────────────────────────────────────────────────┘

