## This is like a Social Media Platfrom to share "About your Day"
![logo](https://github.com/codekushi/howsyourday/blob/master/logo.png?raw=true)
## Dependencies used
### Flask, Flask-SocketIO
### HTML for jinja template
### CSS, BootStrap for styling
### Javascript for Flask-SocketIO
### SQL with PostgresSql

### This web app is designed that you can share your feeling that how was your day You can make your profile with an image, tell users about your day with an image and piece of text

## Instructions to use the app:
- Register and log into app
- Set up your profile
- Share about your day with an image and some text any number of times
- comment on your post and other posts
- All the data of the post will be deleted for the next day because we won't have same day every day
- you can delete your posts and Comments
- A global chatroom for you to chat with database storing of messages with a option of deleting your messages
- All the messages will be deleted at the the time of deleting posts

## All the pages are Mobile responsive

### I have used PostgresSql database on my local computer for storing information you will need to use a database with the templates in the sql folder to achieve the same results

# Files usedin application
## app.py the actual Flask app
## sql files folder - contains sql templates used in databases
- users.sql for user table
- posts.sql for post table
- globalchat.sql for chat table
- comments.sql for comments table
## static folder - for a background image in homepage and profile pictures
- images folder in static contains posts images
## templates folder for HTML templates to be rendered
- chat.html for chat page
- error.html for error page
- login.html for login page
- post.html for specific post page
- posts.html for posts page
- signup.html for registering page
- user.html for profile page
- welcome.html for homepage
- write.html for writing post
## cornjob.text - for scheduled deletions in filesystem(if deployed)
- The app states it deletes Posts at 23:59 PM everyday. As I have used PostgresSql Database which doesn't have ant events and triggers I have used cornjob for this task. So on scheduled time the cornjob deletes Posts table data which automatically deletes Comments table data and also images for respective posts in filesystem
## requirements.txt to install requried packages

#### This is my final Project for CS50 Web Programming with Python and Javascript
Here are my [Certificate of Completion from CS50](https://certificates.cs50.io/599882b0-91a8-41ea-a5eb-addfab25fce1) and [Verified Certificate of Achievement from edX](https://courses.edx.org/certificates/2c010d08b5cf4411b3d1c702a94d2e83)
