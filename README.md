# BloodSync — Blood Donate & Request System

A Django-based web application where users can register as blood donors, create blood
requests, and find suitable donors based on blood group and location.

> "Find a donor. Save a life."

## Features

- **User Registration & Login** — Django's built-in authentication system, with an
  auto-created `Profile` (full name, email, phone, blood group, location, date of birth,
  optional profile picture).
- **Donor Profile** — Any logged-in user can create/update a `DonorProfile` (blood group,
  phone, location, last donation date, availability status, short description). Users can
  only edit/delete their own donor profile.
- **Blood Requests** — Full CRUD: create, read, update, delete, and update status
  (Pending / Fulfilled / Cancelled). Users can only edit/delete their own requests.
- **Donor Search** — Filter donors by blood group, location, and availability.
- **Blood Request Listing** — Filter requests by blood group, location, and status, with
  pagination.
- **Detail Pages** — Dedicated detail pages for both donors and blood requests.
- **Form Validation** — Required fields, phone number format, positive bag counts, and
  future-dated "required date" validation.
- **Django Messages** — Success/error feedback across the app.
- **Responsive UI** — Built with Bootstrap 5.

## Tech Stack

- Django 5.2 (Python)
- SQLite (default database)
- Bootstrap 5 (via CDN)
- Pillow (for image/profile picture handling)

## Project Structure

```
bloodsync/          # Project settings, root URLs, home/about views
accounts/           # User registration, login/logout, profile
donors/             # Donor profile model, views, search
requests_app/       # Blood request model, views, CRUD, search
templates/          # All HTML templates (base.html + app templates)
static/css/         # Custom stylesheet
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/sobuzytp/blood_sync.git
   cd bloodsync
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for the admin dashboard)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/` in your browser.

## Database Models

- **Profile** — one-to-one with `User`, auto-created on registration. Stores full name,
  phone number, blood group, location, date of birth, and an optional profile picture.
- **DonorProfile** — one-to-one with `User`, created when a user chooses to "Become a
  Donor". Stores donor-specific info and availability status.
- **BloodRequest** — foreign key to `User` (the requester). Stores patient/hospital
  details, required date, bags required, contact number, and status.

## Notes

- Profile pictures and other uploads are stored under `media/` (not tracked by git).
- The `db.sqlite3` file is excluded from version control; run `migrate` to create a fresh
  database.
