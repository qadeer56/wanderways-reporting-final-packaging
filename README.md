WanderWays – Travel Package Inventory System

A Python-based Travel Package Inventory Management System designed to help WanderWays Travel manage travel packages through a simple command-line interface.

Features

- Add new travel packages
- View all available packages
- Search packages by ID or name
- Update package prices
- Update package stock
- Delete travel packages
- Generate a formatted inventory report
- Responsive table formatting based on terminal width
- Automatic wrapping of long package names
- JSON-based data storage
- Input validation and error handling

Technologies Used

- Python 3
- JSON
- pathlib
- File Handling
- String Formatting
- Exception Handling

Project Structure

wanderways-reporting-final-packaging/
│
├── main.py
├── packages.json
├── README.md
├── SUBMISSION_NOTE.md
└── .gitignore

Requirements

- Python 3.8 or newer
- No external libraries required.

Installation and Setup

1. Download or clone this repository.
2. Open the project folder.
3. Make sure Python is installed.
4. Open the terminal in the project directory.
5. Run the application:

python main.py

Application Menu

===== WANDERWAYS INVENTORY =====

1. Add Package
2. View Packages
3. Search Package
4. Update Package
5. Delete Package
6. Generate Report
7. Exit

Inventory Reporting

The application includes a report generator that displays all travel packages in a readable, aligned console table.

The report contains:

- Package ID
- Package Name
- Price
- Stock

The table automatically adjusts its package-name column according to terminal width and wraps long package names for better readability.

Data Storage

All package information is stored in "packages.json".

Each package contains:

- "id": Unique package identifier
- "name": Travel package name
- "price": Package price
- "stock": Available package quantity

The application automatically saves changes to the JSON file.

Example Report

========== WANDERWAYS INVENTORY REPORT ==========

+-----+--------------+----------+-------+
| ID  | Package Name | Price    | Stock |
+-----+--------------+----------+-------+
| 120 | hunza tour   | 50,000.00| 5     |
| 122 | swat tour    | 55,000.00| 5     |
| 111 | murree tour  | 45,000.00| 6     |
+-----+--------------+----------+-------+

Total packages: 3

Note: Actual table widths depend on terminal size and inventory data.

Project Objective

To develop a reliable command-line inventory management system that helps WanderWays Travel manage package availability, pricing, searching, and reporting efficiently.

Author

Muhammad Qadeer Khan

Python Development Intern
