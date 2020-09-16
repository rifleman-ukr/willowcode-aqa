Test task for Willowcode Automation QA Engineer position

To run on local environment run main.py with Python 3.8 (not lower).

To launch tests just execute "pytest" command in project directory.

NOTE: Do not forget to install required libs via "pip install -r requrements.txt" command before launch.
Also using virtual environment is highly recommended.

What does this API can?
1. GET request to '/' endpoint returns list of jsons of all available in database articles.
Request body: not required
Response: list of jsons

2. POST request to '/' endpoint creates new article in database and returns it.
Request body: {"title": string, "text": string}
Response: json

3. POST request to '/' endpoint updates an article in database if same title already existed and returns it.
Request body: {"title": string, "text": string}
Response: json

4. GET request to '/random' endpoint returns a random article.
Request body: not require
Response: json

5. GET request to '/version_set' updates display version of an article, available only with auth header.
Request body: {"title": string, "version": integer}
Header: Authorization="admin"
Response: json

6. GET request to '/versions' returns list of text versions for an article.
Request body: {"title": string}
Header: Authorization="admin"
Response: json


Developed by Sviatoslav Davydenkov