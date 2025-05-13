# ReSort Application

A Streamlit-based application for data sorting and analysis.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

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

4. Run the application:
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
- Various Google AI and authentication libraries

For a complete list of dependencies, see `requirements.txt`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
