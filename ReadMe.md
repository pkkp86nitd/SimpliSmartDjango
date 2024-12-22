Set Up the Virtual Environment
Create a virtual environment to isolate the project's dependencies:

On macOS/Linux:
python3 -m venv venv

On Windows:
python -m venv venv

Activate the virtual environment:

On macOS/Linux:
source venv/bin/activate

On Windows:
venv\Scripts\activate

Install the Dependencies
Install all required dependencies using pip:
pip install -r requirements.txt

Set Up the Database
Before running the project, you need to set up the database. Django uses migrations to set up the database schema.

Run the following command to create the necessary database tables:
python manage.py migrate

Create Superuser (Optional)
If you want to access the Django admin panel, you can create a superuser by running:
python manage.py createsuperuser
Follow the prompts to create the superuser account.

Run the Development Server
Now, you're ready to run the Django development server. Use the following command to start the server:
python manage.py runserver
This will start the server on http://127.0.0.1:8000/. You can access the application in your browser by visiting this URL.

Accessing the Admin Panel (Optional)
If you created a superuser in Step 5, you can access the Django admin panel at:
http://127.0.0.1:8000/admin/
Log in using the superuser credentials you created and manage your clusters, resources, and deployments.

Testing the Application
If you want to run the tests to ensure everything is working correctly, you can run the following command:
python manage.py test

Curl Requests for API Endpoints:

1. Register User:
curl --location 'http://127.0.0.1:8000/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "john_doe",
  "password": "password123",
  "email": "john@example.com"
}'

2. Login User:
curl --location 'http://127.0.0.1:8000/auth/login/' \
--header 'Content-Type: application/json' \
--data '{
  "username": "john_doe",
  "password": "password123"
}'

3. Create Cluster:
curl --location 'http://127.0.0.1:8000/clusters/' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "name": "New Cluster 4",
  "total_cpu": 100.0,
  "total_ram": 256.0,
  "total_gpu": 4.0
}'

4. Get Cluster Details:
curl --location 'http://127.0.0.1:8000/clusters/1/' \
--header 'Authorization: Bearer <TOKEN>'

5. Check Resources of Cluster:
curl --location 'http://127.0.0.1:8000/clusters/1/check_resources/' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "required_cpu": 10.0,
  "required_ram": 20.0,
  "required_gpu": 1.0
}'

6. Create Deployment:
curl --location 'http://127.0.0.1:8000/deployments/' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "name": "New Deployment 1",
  "cluster_id": 1,
  "cpu_request": 5.0,
  "ram_request": 10.0,
  "gpu_request": 1.0
}'

7. Get Deployment Details:
curl --location 'http://127.0.0.1:8000/deployments/1/' \
--header 'Authorization: Bearer <TOKEN>'

8. Update Deployment:
curl --location 'http://127.0.0.1:8000/deployments/1/' \
--header 'Authorization: Bearer <TOKEN>' \
--header 'Content-Type: application/json' \
--request PUT \
--data '{
  "name": "Updated Deployment",
  "cluster_id": 1,
  "cpu_request": 10.0,
  "ram_request": 20.0,
  "gpu_request": 2.0
}'

9. Delete Deployment:
curl --location 'http://127.0.0.1:8000/deployments/1/' \
--header 'Authorization: Bearer <TOKEN>' \
--request DELETE
   


I tried redis as scheduler , it periodic scheduler didn't worked for me
Commands to check worker and scheduler logs

celery -A backend_service worker --loglevel=info
celery -A backend_service  beat --loglevel=info