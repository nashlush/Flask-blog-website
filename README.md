# Flask-blog-website
This is a python flask blog website which uses flask sql alchemy for mysql database connectivity.
You can also use sqlite for the database.
The website is highly scalable and reusable so you can pretty much change the look of the website just by changing the config.json file.
The website uses html css js and bootstrap for the frontend
Steps to run on you local machine:
1. Set the port as a second argument in app.run in main.py file as port = 8000 or default port will be 5000
2. And run the file after installing all the required packages 
3. Here's the list of packages you need to install as i havent provided the requirements.txt file 
      blinker==1.4
      click==8.0.1
      colorama==0.4.4
      Flask==2.0.1
      Flask-Mail==0.9.1
      Flask-SQLAlchemy==2.5.1
      greenlet==1.1.0
      gunicorn==20.1.0
      itsdangerous==2.0.1
      Jinja2==3.0.1
      MarkupSafe==2.0.1
      mysqlclient==2.0.3
      SQLAlchemy==1.4.15
      Werkzeug==2.0.1
4. you might also need to change the database uri in the main.py file so as to make  a connection to your database.
5. And you are good to go.
You can check out this website on [a link](https://avinash-blog-website.herokuapp.com)
