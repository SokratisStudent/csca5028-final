# csca5028-final-project
Final Project for CSCA 5028 - Applications of Software Architecture for Big Data

### Initialize python environment
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Run tests
```bash
pytest -v
```

### Run with flask in local development server
```bash
 flask --debug --app main.py run
```
To test:
open browser to http://localhost:5000/

