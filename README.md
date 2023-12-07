# csca5028-final-project
Final Project for CSCA 5028 - Applications of Software Architecture for Big Data

### Initialize python environment
```bash
source venv/bin/activate
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
(a) open browser to http://localhost:5000/createPerson
(b) Add any name in any country, this will add the public holidays of that country in the database (as given by https://api-ninjas.com/api/holidays)

### Look at the database data (requires sqlite3 installation)
```bash
sqlite3 instance/vacations.sqlite3
```
Check out
(a) select * from country;
(b) select * from public_holiday;
