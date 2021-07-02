# test_task

REST API for working with transactions history. 
**PostgreSQL** and **Postman** must be installed for better experience of testing the API.

To start working with the API please follow the steps:
>1. Install requirements with command ```pip install -r requirements.txt```
>2. Initialize the database **postgres_db** and tables **limits** and **history** with the help of 
>```app/create_tables.py```. The name of the database can be changed in ```app.__init__.py```.
>3. Start ```app/main.py``` and feel free to test the API, either through ```test.py``` or via Postman app.

The API detailed description can be accessed via ```openapi.json```. 
Check it out [here](https://editor.swagger.io/) for better document view.

![screenshot of sample](https://i0.wp.com/marketplace-cdn.atlassian.com/files/images/3a8b0e69-dbfa-474f-9eb3-101d1449087e.png?resize=650,400)