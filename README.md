# ReSort Application

A Streamlit-based application for data sorting and analysis.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git
- MySQL Server 8.0 or higher

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ReSort.git
cd ReSort
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Get a Google Gemini Api Key
   - Go to Google AI studio and click on create API key
   - In the ReSort directory, create a file titled ".env"
   - In the .env file, copy and paste the following (no quotes)
   ```
   GEMINI_API_KEY = "Your API Key here"
   ```
   
5. Database Setup:
   - Install MySQL Server if you haven't already
   - Create a new database:
   ```sql
   CREATE DATABASE resort_db;
   ```
   - Create a new user and grant privileges:
   ```sql
   CREATE USER 'resort_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON resort_db.* TO 'resort_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
   - Create a `.env` file in the project root with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=resort_user
   DB_PASSWORD=your_password
   DB_NAME=resort_db
   ```

6. Run the application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

- `app.py`: Main application file
- `requirements.txt`: Python dependencies
- `config.yaml`: Configuration settings
- `Modules/`: Core functionality modules
- `Module_pages/`: Streamlit page modules
- `documentation/`: Project documentation

## Dependencies

The project uses several key dependencies:
- Streamlit for the web interface
- Pandas for data manipulation
- NumPy for numerical operations
- MySQL Connector for database operations
- Various Google AI and authentication libraries

For a complete list of dependencies, see `requirements.txt`.

## Database Configuration

The application uses MySQL for data storage. Make sure to:
1. Have MySQL Server running
2. Create the database and user as described in the setup instructions
3. Set up the `.env` file with your database credentials
4. Ensure the MySQL service is running before starting the application

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
