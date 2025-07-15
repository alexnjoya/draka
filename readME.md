# Student Result Management CLI Tool

A command-line Python application for managing student results with PostgreSQL database integration.

## Features

- **File Reading**: Import student data from CSV/TXT files
- **Database Operations**: Store and manage data in PostgreSQL
- **Grade Calculation**: Automatic grade assignment based on scores
- **Interactive CLI**: User-friendly command-line interface
- **Report Generation**: Export summary reports to text files
- **Data Validation**: Input validation and error handling

## Prerequisites

- Python 3.7+
- PostgreSQL database server
- psycopg2 package

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**:
   - Create a database named `student_results_db`
   - Update database credentials in `config/settings.py`

4. **Configure database settings**:
   Edit `config/settings.py` with your database credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'student_results_db',
       'user': 'your_username',
       'password': 'your_password',
       'port': '5432'
   }
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Main Menu Options**:
   - **View all records**: Display all student records
   - **View student by index number**: Search for specific student
   - **Update student score**: Modify existing student scores
   - **Export summary report**: Generate and save summary reports
   - **Load data from file**: Import student data from files
   - **Exit**: Close the application

## File Format

### CSV Format
```csv
IndexNumber,FullName,Course,Score
STU001,John Doe,Computer Science,85
STU002,Jane Smith,Mathematics,92
```

### TXT Format
```
STU001,John Doe,Computer Science,85
STU002,Jane Smith,Mathematics,92
```

## Grade Scale

- **A**: 80-100 (Excellent)
- **B**: 70-79 (Good)
- **C**: 60-69 (Average)
- **D**: 50-59 (Below Average)
- **F**: 0-49 (Fail)

## Database Schema

```sql
CREATE TABLE student_results (
    id SERIAL PRIMARY KEY,
    index_number VARCHAR(10) NOT NULL,
    full_name TEXT NOT NULL,
    course TEXT NOT NULL,
    score INTEGER NOT NULL,
    grade CHAR(1)
);
```

## Project Structure

```
student_result_management/
├── main.py                 # Main application entry point
├── database/
│   ├── connection.py       # Database connection management
│   └── operations.py       # Database CRUD operations
├── utils/
│   ├── file_handler.py     # File reading and writing
│   └── grade_calculator.py # Grade calculation logic
├── config/
│   └── settings.py         # Database configuration
├── data/
│   ├── sample_students.csv # Sample data file
│   └── reports/            # Generated reports directory
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Sample Data

The application includes sample student data for testing. Use menu option 5 → 3 to create the sample data file, then option 5 → 1 to load it.

## Error Handling

The application includes comprehensive error handling for:
- Database connection failures
- Invalid file formats
- Duplicate student records
- Invalid score inputs
- File I/O errors

## Example Usage

1. **First Run**: Create sample data and load it
2. **View Records**: Check all loaded students
3. **Update Score**: Modify a student's score
4. **Generate Report**: Export summary to file

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `config/settings.py`
- Check if database `student_results_db` exists

### File Import Issues
- Verify file format (CSV with headers or comma-separated TXT)
- Check file path and permissions
- Ensure data follows the required format

### Permission Issues
- Ensure write permissions for `data/reports/` directory
- Check PostgreSQL user permissions

## Development Notes

- Built with raw Python (no frameworks)
- Uses psycopg2 for PostgreSQL connectivity
- Modular design with separate utility functions
- Comprehensive input validation
- Clean CLI interface with user-friendly messages

## Contributing

Feel free to submit issues and enhancement requests!