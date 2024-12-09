# E-commerce-api

This is a E-commerce api that used Django. This project utilizes **Data Envelop** for standardized API responses, which enhances the clarity and consistency of the data exchanged between the client and server. By employing this structure, the API responses are easier to interpret, providing users with a clear understanding of success or failure, along with any associated messages and data.

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- A database (e.g., PostgreSQL, SQLite)

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

3. Apply migrations:

  ```bash
  python manage.py makemigrations
  python manage.py migrate

4. Create a superuser:

  ```bash
  python manage.py createsuperuser

5. Start the development server:
  ```bash
  python manage.py runserver

6. Access the admin panel at http://127.0.0.1:8000/admin/.

7. Api documentation http://127.0.0.1:8000/swagger/ or http://127.0.0.1:8000/redoc/


## Authentication
A custom user model and an OTP management system for authentication are added.

**User Authentication**: Secure user registration and login processes.
- **Password Recovery**: Implemented a feature for users to recover their passwords using a One-Time    Password (OTP) system. OTP will be vaild for 5 minutes.If OTP hasn't used and requested again old OTP will be deleted before generating a new one. No one can add and change OTPs even superusers. 
  - **Forgot Password**: Users can request an OTP to reset their password. 
  - **Reset Password**: After entering the OTP, users can set a new password securely.

License
This project is licensed under the MIT License. See the LICENSE file for details.

### Customization
- Replace `<repository-url>` with the actual GitHub repository URL.
- Add any specific details relevant to your project (e.g., API endpoints, deployment instructions).
