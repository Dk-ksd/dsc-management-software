# DSC Manager

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.1.6-green?logo=django)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite)
![Celery](https://img.shields.io/badge/Celery-5.4.0-%2300C7B7?logo=celery)
![Redis](https://img.shields.io/badge/Redis-5.2.1-red?logo=redis)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-%23150458?logo=pandas)
![Numpy](https://img.shields.io/badge/Numpy-2.2.4-%23013243?logo=numpy)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.1.5-3776AB)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap)
![License](https://img.shields.io/badge/license-Custom-lightgrey)

A Django-based web application developed for **Tass & Hamjit** to streamline the management and tracking of Digital Signature Certificates (DSCs). The system introduces a structured role-based access model with three user roles—**Admin**, **Approver**, and **General User**.

---

##  Features

* Role-based access control (Admin, Approver, General User)
* DSC Request and Approval workflow
* Internal & External DSC management
* Renewal and Expiry tracking
* Email notifications for expired/expiring DSCs
* Backup & Restore system (SQLite based)
* Export DSC data to Excel/CSV
* Pagination & Search functionality for large datasets

---

##  Installation & Setup

### 1. Clone the Repository

```bash
 git clone https://github.com/Dk-ksd/dsc-management-software.git
 cd .\dsc-management-software\
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv dscenv
source dscenv/bin/activate   # On Linux/Mac
dscenv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

Now open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

##  Restoring Backup Database (Important)

After setup, you need to restore the provided **backup database** for the DSC Manager to work properly.

1. Login using the superuser account you just created.
2. You will be redirected to the **Admin Dashboard**.
   At the top-right, click on the **Backup/Restore** button.
3. On the Backup & Restore page, under **Restore Database**, upload the file:

   ```
   backup-restore.sqlite3
   ```
4. Click **Restore Now**.
   ⚠️ Warning: This will replace your current database with the backup.
5. Once restored, all DSC records, roles, and configurations will be available.

 After this step, you can use all the features of the DSC Manager normally.

---

##  Email Setup

Update settings.py with your SMTP configuration:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
---

##  User Roles

### 1. Admin

* Full access to the system.
* Can manage users (Admin, Approver, General User).
* Add and edit DSCs.
* Oversee all DSC operations.

### 2. Approver

* Approves DSC usage requests from General Users.
* Tracks DSC usage logs.

### 3. General User

* Requests DSCs for office tasks (GST filing, MCA filing, e-filing, etc.).
* Returns DSCs after usage.

---

##  Tech Stack

* **Backend**: Django, SQLite
* **Frontend**: HTML, CSS, JavaScript, Bootstrap
* **Task Queue:** Celery with Redis
* **Data Handling & Export:** Pandas, NumPy, OpenPyXL
* **Email Notifications**: Django Email Backend (SMTP)
* **Backup/Restore & Export**: Custom Django views + openpyxl

---

##  Email Notifications

* Admin can send alerts when DSCs are expired or about to expire (within 30 days).
* Users will receive email notifications automatically after the Admin triggers the action.

---

## License & Usage

This project was originally developed for **Tass & Hamjit**.  
The source code is made available here **for educational and portfolio purposes only**.  

 You may view and explore the code to understand the implementation.  
 You may NOT use, copy, modify, or distribute this project for commercial or personal use without explicit permission.  

If you are interested in a **customized DSC Manager** for your organization, feel free to reach out — the system can be tailored to meet your company’s needs.

##  Contact

For inquiries, customization, or collaboration:  
 Email: mrdeekshithk@gmail.com  
 LinkedIn: [Deekshith K](https://www.linkedin.com/in/deekshith-k123)
