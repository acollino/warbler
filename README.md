# Warbler
A light clone of Twitter, allowing users to post messages, follow others, and like posts!

Try it out here: [Warbler on Heroku](https://acollino-warbler.herokuapp.com/)

## Usage
Users can use the search bar to find other users; their profiles will show their posts and links to their followers, who they follow, and any posts they've liked. While these can be viewed, a signed-in account is required to like posts and follow other users; this can be done using the 'Sign Up' and 'Log In' links in the navbar. 

Once logged in, users will be able to edit their own profiles - adding locations, bios, and changing their profile or header image URLs. They will also be able to create posts (AKA 'warbles') for other users to view and like. Logged-in users can additionally delete their own posts or even delete their account if desired. 

## Code Information
Users and Messages are stored in their corresponding tables in the database.

User rows require storing a username, email address, and a hashed password, have a numerical ID for a primary key, and they have default values for the profile and header image URLs. They can also store values for the optional columns bio and location.

Message rows require the message text, have a numerical ID for a primary key, will include a default datetime value for the timestamp column, and have a user_id foreign key that refers to a user's ID.

The database's relationships include: 
- User (message creator)-Message
  - This is a one-to-many relationship, as a single user can create many messages, but a given message will have only one creator.
- User (liked a message)-Message
  - This is a many-to-many relationship, as a user can like many messages, and a message can be liked by many users. This relationship utilizes the associative table 'Likes' to connect a liking-user's ID with a message ID.
- User (follows a user)-User (followed by a user)
  - This is a self-referential many-to-many relationship; a user can follow many other users, and a user can by followed by many other users as well. This relationship utilizes the associative table 'Follows' to connect a user-being-followed's ID with a user-following-another's ID. This relationship requires joins with the User table to ensure correct identification of the 'following user' and the 'user being followed'.

Information is stored in a server-side database using PostgreSQL, accessed via Flask-Sqlalchemy. The server itself uses Flask, and form generation and validation is performed using Flask-WTForms. CSS styling uses Bootstrap via CDN.

## Previews
<img src="https://user-images.githubusercontent.com/8853721/191111532-f173a4be-ddd4-4723-8c33-b43259dc56bd.png" alt="Warbler home page" style="width: 700px">

<img src="https://user-images.githubusercontent.com/8853721/191111887-067f0304-5e94-46c1-95d1-5187baa53e1f.png" alt="User search results" style="height: 500px;">

<img src="https://user-images.githubusercontent.com/8853721/191112244-14261444-5de9-453a-9ab4-8d1e14024c46.png" alt="User profile page" style="height: 500px;">


### Additional Notes
This site was converted from its original structure into utilizing the Flask Application-Factory design; the original files from Springboard can be viewed in the 'original_files' folder. The overall organization could likely be further improved with better separation and subdivision of the packages - user_routes.py is particularly long, and repeated logic could be included in the user_util.py to help make the code more readable.

Lastly, it appears that the original files refer to an image API (Splashbase.co) that seems to have limited support and may have been deprecated since development on this project began. As such, while the preview images display user headers (based on images in my browser cache), these will likely be unavailable in future access to the Warbler site.



