# stockdemo
for testing the end-to-end from angular to python call

1 stock-front
  AngularJS front-end to display stock chart
  To run:
  npm start
  
2 Stockbackend
  Django rest framework to get the stock data from MySql database
  
  # create database
    cd stockbackend
    mysql -u{dblogin} -p{password} -e "CREATE DATABASE stocks"
    mysql -u{dblogin} -p{password} stocks < stocks.sql
    
  Setting for database
  
  update the file in stockbackend/stockbackend/settings.py
  
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stocks',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
        'PORT': '',
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

  }
  
  To run
  
  cd stockbackend
  virtualenv env
  source env/bin/activate
  python -m pip install django
  pip install djangorestframework
  pip install -U wheel
  pip install django-cors-headers
  pip install django mysqlclient
  python manage.py runserver
  
3. pystock
  A python file to retrieve the stock information based on date range. May schedule as cron job to pull the data in daily base
  
  
  
