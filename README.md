# VeManage - Vendor Management System with Performance Metrics

VeManage is a Django-based Vendor Management System (VMS) designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Features

### Vendor Profile Management:
- Create, retrieve, update, and delete vendor profiles.
- Store vendor information such as name, contact details, address, and unique vendor code.
- Track performance metrics including on-time delivery rate, quality rating average, average response time, and fulfilment rate.

### Purchase Order Tracking:
- Create, retrieve, update, and delete purchase orders.
- Track PO details such as PO number, vendor reference, order date, delivery date, items, quantity, and status.

### Vendor Performance Evaluation:
- Calculate and display vendor performance metrics including on-time delivery rate, quality rating average, average response time, and fulfilment rate.

## Installation

To run VeManage locally, follow these steps:

1. Clone the repository:

```bash

1. Clone the repository:

git clone https://github.com/your-username/VeManage.git

2. Navigate to the project directory:

cd VeManage

3. Install dependencies:

pip install -r requirements.txt

4. Apply database migrations:

python manage.py migrate

5. Create a superuser (admin account):

python manage.py createsuperuser

6. Start the development server:

python manage.py runserver

7. Access the VeManage admin interface at http://127.0.0.1:8000/admin/ and log in with the superuser credentials created in step 5.

Token Authentication
---------------------
This project uses token-based authentication. To authenticate requests to protected endpoints, include an `Authorization` header in the request with the token value.

Deployment
----------
For deployment instructions, refer to the Django Deployment Documentation: https://docs.djangoproject.com/en/stable/howto/deployment/.

Contributing
------------
Contributions are welcome! Please follow the contribution guidelines provided in the CONTRIBUTING.md file.

