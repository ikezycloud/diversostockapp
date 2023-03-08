# Shares Brokering System

SBS is a Python Django Web App for dealing with Shares sales and purchases.

## Installation
### 1
First, create a folder with any name for example: 'sbs'.
paste the project in the 'sbs' folder

open the terminal(PowerShell) and go to 'your_path\sbs>'
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

### 2 create and activate the virtual environment
```bash
your_path\sbs> python -m venv venv
# command for windows
your_path\sbs> .\venv\Scripts\activate
```

### 3
```bash
(venv) your_path\sbs> cd shares_broker
(venv) your_path\sbs\shares_broker> pip install  requirements.txt
```
after successful installation

### 4 Runt the project
```bash
(venv) your_path\sbs\shares_broker> python manage.py makemigrations
(venv) your_path\sbs\shares_broker> python manage.py migrate
(venv) your_path\sbs\shares_broker> python manage.py runserver
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change. Or if you found any issues let us know.