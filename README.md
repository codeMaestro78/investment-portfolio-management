# Investment Portfolio Management System

## Overview

The **Investment Portfolio Management System** is a comprehensive application designed to help users track and manage their investments across different asset classes, including real estate, stocks, and mutual funds. The system leverages **MySQL** for efficient data storage and **Matplotlib** for data visualization, providing users with insightful analytics on their investments.

## Features

- **Real Estate Investment Tracking**

  - Store property details including purchase price, location, and current valuation.
  - Calculate return on investment (ROI) for properties.

- **Stock Portfolio Management**

  - Track stock purchases, current holdings, and performance trends.
  - Fetch real-time stock market data.
  - Generate graphical representations of stock performance using Matplotlib.

- **Mutual Fund Management**

  - Track SIP and lump sum investments.
  - Calculate NAV-based portfolio performance.
  - Visualize investment growth over time.

- **Data Visualization**

  - Use Matplotlib to generate interactive charts for performance analysis.
  - View asset allocation breakdown.

- **Database Management**
  - Store and retrieve investment records using MySQL.
  - Secure and optimize database queries for fast performance.

## Technologies Used

- **Backend:** Python (Flask/Django if applicable)
- **Database:** MySQL
- **Data Visualization:** Matplotlib
- **APIs:** Real-time stock/mutual fund data (if applicable)
- **Frontend (Optional):** React, HTML, CSS (if there's a UI component)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python libraries:
  ```bash
  pip install mysql-connector-python matplotlib pandas flask
  ```

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/investment-portfolio-management.git
   cd investment-portfolio-management
   ```
2. Configure the MySQL database:
   - Create a database: `CREATE DATABASE investment_db;`
   - Update database credentials in `config.py` (if applicable).
3. Run the application:
   ```bash
   python main.py
   ```
4. (Optional) Run a frontend application (if applicable):
   ```bash
   npm install
   npm start
   ```

## Usage

- Enter investment details for stocks, real estate, or mutual funds.
- View investment performance through interactive charts.
- Analyze returns and adjust portfolio allocation accordingly.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, reach out to: **thelogical369@gmail.com**
