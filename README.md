# AuctionPulse

## Description

This is a web-based auction platform designed to facilitate the buying and selling of items through a transparent and competitive bidding process. It connects sellers looking to maximize their sales with buyers eager to find unique items at competitive prices.

## Technologies Used

- **Backend**: python with Django webframework
- **Database**: relational mysql
- **Task Processing**: Celery for asynchronous task handling and scheduling
- **Message Broker & Caching**: Redis for task queuing, caching, and fast data access

## Features

- User registration and authentication
- Real-time bidding on auctions
- Automatic auction closing
- Auction scheduling and bid processing via Celery

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- MySQL 8.x+
- Redis 6.x+
- Celery 5.x+

## Installation

- Clone the repository: 

    ``` bash
    git clone https://github.com/Danielyilma/AuctionPulse.git
    ```


- Navigate to the project directory

    ``` bash
    cd AuctionPulse
    ```

- Set up a virtual environment (optional but recommended):

    ``` bash
    python3 -m venv venv
    source venv/bin/activate # for windows: venv/Scripts/activate
    ```

- Install project dependencies

    ``` bash
    pip install -r requirements.txt
    ```

- Configure environment variables:

    AuctionPulse uses environment variables to manage sensitive data
    such as the database credentials, Google OAuth2 keys, and payment keys.
    These settings should be placed in a .env file.

    Create a .env file in the project root directory (where manage.py is located):

    ``` bash
    touch .env
    ```
    
    Add the following variables to your .env file:

    ``` env
    # Django secret key
    SECRET_KEY=your_django_secret_key

    # Database settings
    DB_NAME=auctionpulse_db
    DB_USER=auctionpulse_user
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_PORT=3306

    # Google OAuth2 settings
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_client_id
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_client_secret

    # Chapa payment secret key
    CHAPA_SECRET_KEY=your_chapa_secret_key
    ```

-  Configure the MySQL database:

    ``` sql
    CREATE DATABASE auctionpulse_db;
    CREATE USER 'auctionpulse_user'@'localhost' IDENTIFIED BY 'yourpassword';
    GRANT ALL PRIVILEGES ON auctionpulse_db.* TO 'auctionpulse_user'@'localhost';
    FLUSH PRIVILEGES;
    ```

- Migrate model schema's

    ``` bash
    python manage.py migrate
    ```

- Set up Redis and Celery:

  Ensure Redis is running:
    ``` bash
    redis-server
    ```

- Running the server

    ``` bash
    python manage.py runserver
    ```

- Run the Celery worker:

  In a separate terminal window, start the Celery worker:
    ``` bash
    celery -A AuctionPulse worker --loglevel=info
    ```

## API Documentation
AuctionPulse provides a fully interactive API documentation using Swagger UI. You can use Swagger to explore the API, try out requests, and view detailed information about each endpoint.

Access the Swagger documentation at:
    ``` URI
    http://127.0.0.1:8000/api/schema/swagger-ui
    ```
