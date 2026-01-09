# Employee-Record-Management-Portal
A Flask-based Employees Management System that allows administrators to manage active employees and ex-employees, view detailed employee profiles, upload documents/photos, and mark employees as inactive with an automatic leaving date.

This project is designed for internal HR/Admin usage with a clean UI, role-based access, and a clear separation between active employees and ex-employees.

# Admin Features
• Secure Admin Login & Logout

• View Active Employees Dashboard

• View Ex-Employees List

• View detailed Employee / Ex-Employee Profile

• Upload employee photos

• Set / reset employee passwords

• Mark employee as Inactive using a toggle button

• Automatically sets work_status = inactive

• Automatically sets leaving_date = current date

• Role-based access using @admin_required

# Employee Profile
• Personal Details

• Designation & Contact details

• LinkedIn Profile Link

• Uploaded Documents --> Aadhar card, Degree Certificate

• Profile photo with click-to-enlarge modal view

# Navigation Logic
• Toggle button appears only when profile is opened from Admin Dashboard.

• Toggle is hidden when profile is opened via Ex-Employees list.

• Back button appears only when applicable.

# Tech Stack
• Backend: Python (Flask)

• Frontend: HTML, CSS, Bootstrap 5, Jinja2

• Database: PostgreSQL

• Auth: Flask Sessions

• UI: Responsive design with modern UX

<img width="1916" height="868" alt="Screenshot 2026-01-09 153556" src="https://github.com/user-attachments/assets/72ab8c0d-6c1c-4c68-8d30-46ac7368dbd1" />

<img width="1885" height="860" alt="Screenshot 2026-01-09 153647" src="https://github.com/user-attachments/assets/d45d19e9-53bd-43ce-93d1-0f4b62c5303a" />

<img width="1901" height="751" alt="Screenshot 2026-01-09 153811" src="https://github.com/user-attachments/assets/f07cfdb6-c9f8-451d-b33d-094cb0a88d5e" />

<img width="1849" height="863" alt="Screenshot 2026-01-09 153929" src="https://github.com/user-attachments/assets/255b02a6-cf12-4b75-bc6b-39fab0f72e24" />

