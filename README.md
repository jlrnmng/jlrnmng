# Database Management System (DBMS)

## Overview
This project is a web-based Database Management System built with Flask, replacing a PyQt5 GUI application. It simplifies database tasks like viewing, adding, updating, and deleting records in a MySQL database.

## Features
- Web-based interface using Flask and Bootstrap.
- CRUD operations (Create, Read, Update, Delete).
- Responsive design for all devices.
- Form validation and error handling.
- Flash messages for user feedback.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd db-management
   ```
2. **Set Up Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access:** Open `http://127.0.0.1:5000/` in your browser.

## Usage
- **View Data:** Select a table to view records.
- **Add Record:** Use forms to add new data.
- **Update Record:** Modify existing records.
- **Delete Record:** Remove records based on conditions.

## Technical Details
- **Frameworks and Libraries:** Flask, Bootstrap, MySQL Connector.
- **Functions:**
  - `connect_to_db()`: Connects to MySQL.
  - Flask routes handle CRUD operations.
- **Security:** Parameterized queries to prevent SQL injection.

## Future Enhancements
- User authentication and roles.
- Pagination for large datasets.
- Support for multiple databases (PostgreSQL, SQLite).
- API integration.

## References
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [MySQL Connector Documentation](https://dev.mysql.com/doc/connector-python/en/)
"# jlrnmng" 
"# jlrnmng" 
