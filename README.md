# crypto-portfolio

# Instructions to run this project locally

#git clone https://github.com/sharvadlamani/crypto-portfolio.git

#cd into repo: cd crypto-portfolio

#install the requirements: pip install -r requirements.txt

#navigate to folder that contains run.py : cd backend

#run the backend : flask run.py

navigate to folder that contains index.html : cd ../frontend

#run the frontend: python3 -m http.server

# Make sure to click name of portfolio again to reload the page after changing the quantity of a coin 

# Still need to update percentage (right now it assumes max of 1 coin per coin type)



# Structure of backend
backend

 ┣ app
 
 ┃ ┣ auth.py
 
 ┃ ┣ coins.py
 
 ┃ ┣ config.py
 
 ┃ ┣ models.py
 
 ┃ ┣ portfolio.py
 
 ┃ ┣ views.py
 
 ┃ ┗ __init__.py
 
 ┣ migrations
 
 ┗ run.py

#SQL Schema
SQL schemas will be created by the Flask ORM, which will update by using Flask Migration when we update models.py


#Postman
Link to endpoint API documentation: https://documenter.getpostman.com/view/37286225/2sA3rxqZAT
