# ticket_vendor_app
Here is a RESTful API for a ticket vendor app written in:
- Python
- Flask
- Flask-RestPlus
- SQLAlchemy

connected to a PostGreSQL database hosted on AWS RDS.  This Flask application is containerized with Docker and built on a Python image.  

- The API is documented and demonstratable through the Swagger UI, URL which is accessible by starting the app.
- The app takes care of generating the database models as well as table creation from scratch.

### The app can be run in the docker container 
1. While in the main directory, build the docker image with the command `sh scripts/build.sh`
2. `sh scripts/run.sh` will start the app on port 5000.  Access the Swagger UI page with http://0.0.0.0:5000/api/
