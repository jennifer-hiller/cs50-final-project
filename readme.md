# TWITTER CLONE
#### Video Demo:  <URL HERE>
#### Description:
Some of the simplest functionality from Twitter are duplicated here. Users can:
* Register
* Log In
* Tweet
* See tweets
* Like/Unlike tweets
* Delete tweets

This project takes some aspects of the Finance project since I liked how it stored passwords, had an "apology" page for when things went wrong, and used sessions. It utilizes Bootstrap since Finance did as well, as well as Bootstrap being actually a Twitter invention.

Most of the project involves static pages being returned except the "like" function, which utilizes async/await and turns the function into an API.

There are 3 tables involved in sqlite: a users table, a tweets table which references the users table, and a "likes" table, where there is no primary key and instead references 2 foreign keys from the users and tweets table. When queried correctly, the table can reveal if the logged-in user liked the tweet, and counting rows can reveal how many likes the tweet has.

There wasn't much in the way of custom CSS as Bootstrap takes care of most of it.

The hearts are SVG I took from Twitter's own site, and it was a bit of a challenge coloring the "liked" heart red.

app.py defines all the functionality in the application:

index ("/") queries the database for all tweets and outputs them in descending order of date. Since the tweets table uses a datetime updater to record date and time of the tweet, I needed 2 libraries: datetime and humanize. This can show the user how old the tweet is, rather than the ugly datetime format sqlite uses.

register, login, and logout do exactly that.

tweet ("/tweet") handles the form submission from the index page and inserts into the "tweets" database. It only enters the user id and the tweet contents, as the database handles the date and time on time of insertion.

like ("/like") adds or deletes records from the "likes" table and returns either a success message and the new number of likes, or an error message, which is handled as a javascript alert().

delete ("/delete") deletes a record from the "tweets" table and returns either a success message, in which the javascript will remove the tweet, or an error message, which is handled by a javascript alert();

All of the HTML forms use client-side validation, in addition to the server side validation.

You may notice that I'm "deferring" the script tag. This is something I learned can bypass the problem of the dom being entirely loaded and listening for that event. In essence, this does the same thing.