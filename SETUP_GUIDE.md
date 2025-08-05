# Setup Guide for Enhanced Student Result Management System

## 🔧 Quick Setup Steps

### 1. Database Setup
Make sure PostgreSQL is running and create the database:
```sql
CREATE DATABASE student_results_db;
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Reset Database Schema (IMPORTANT!)
If you're getting "column does not exist" errors, run:
```bash
python reset_database.py
```

### 4. Test Database Connection
```bash
python test_connection.py
```

### 5. Initialize Sample Data (Optional)
```bash
python initialize_sample_data.py
```

### 6. Run the Enhanced System
```bash
python enhanced_main.py
```

## 🔍 Troubleshooting

### Database Schema Issues
If you get errors like "column 'user_type' does not exist":

1. **Reset the database schema**:
   ```bash
   python reset_database.py
   ```

2. **This will drop and recreate all tables with the correct schema**

### Database Connection Issues
If you get connection errors:

1. **Check PostgreSQL is running**
   ```bash
   # On Windows
   net start postgresql
   
   # On Linux/Mac
   sudo systemctl start postgresql
   ```

2. **Verify database exists**
   ```sql
   \l
   -- Look for student_results_db in the list
   ```

3. **Check credentials in config/settings.py**
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'student_results_db',
       'user': 'your_username',
       'password': 'your_password',
       'port': '5432'
   }
   ```

### Transaction Error Fix
If you see "current transaction is aborted" error:

1. **Reset the database connection**
   ```bash
   python test_connection.py
   ```

2. **Or restart PostgreSQL**
   ```bash
   # Windows
   net stop postgresql
   net start postgresql
   
   # Linux/Mac
   sudo systemctl restart postgresql
   ```

## 📋 Sample Credentials

After running `initialize_sample_data.py`:

### Admin
- Email: `admin@university.edu`
- Password: `admin123`

### Staff
- Dr. John Smith: `12345678` / `12345`
- Prof. Sarah Johnson: `87654321` / `54321`
- Dr. Michael Brown: `11223344` / `11111`

### Students
- Alice Johnson: `20230001` / `11111`
- Bob Wilson: `20230002` / `22222`
- Carol Davis: `20230003` / `33333`
- David Miller: `20230004` / `44444`
- Eva Garcia: `20230005` / `55555`

## 🚀 First Time Setup

1. **Reset database schema** (if needed):
   ```bash
   python reset_database.py
   ```

2. **Run the test script**:
   ```bash
   python test_connection.py
   ```

3. **If tests pass, initialize sample data**:
   ```bash
   python initialize_sample_data.py
   ```

4. **Start the enhanced system**:
   ```bash
   python enhanced_main.py
   ```

5. **Login as admin** and explore the features!

## 🔧 Common Issues and Solutions

### Issue: "column 'user_type' does not exist"
**Solution**: The database has old schema. Run:
```bash
python reset_database.py
```

### Issue: "current transaction is aborted"
**Solution**: The database connection is in a bad state. Run:
```bash
python test_connection.py
```

### Issue: "Failed to connect to database"
**Solution**: Check your PostgreSQL configuration in `config/settings.py`

### Issue: "Import error"
**Solution**: Make sure you're in the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Issue: "Permission denied"
**Solution**: Check database user permissions:
```sql
GRANT ALL PRIVILEGES ON DATABASE student_results_db TO your_username;
```

## 📞 Support

If you continue to have issues:

1. Check the database logs for detailed error messages
2. Verify PostgreSQL is running and accessible
3. Ensure all dependencies are installed correctly
4. Try the test script to isolate the issue

The enhanced system includes better error handling and should now work more reliably! 