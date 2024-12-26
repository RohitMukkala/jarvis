# Jarvis - AI-Powered Personal Assistant

## Overview
Jarvis is an AI-powered personal assistant integrating speech recognition, face authentication, a heart disease prediction model, and more. This project combines Python, TensorFlow, and web technologies for an interactive user experience.

---

## Setup Instructions

### Step 1: Clone the Repository

#### Open Terminal or Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, and hit Enter.
- **Mac/Linux**: Open the Terminal from the Applications menu or shortcuts.

#### Navigate to Your Desired Folder
Use the `cd` command to move to the folder where you want to save the project:
```bash
cd /path/to/your/folder
```

#### Copy Repository URL
1. Go to the Jarvis GitHub repository ([link](https://github.com/YourUsername/jarvis)).
2. Click on the green **"Code"** button.
3. Select **HTTPS**, then copy the URL (e.g., `https://github.com/YourUsername/jarvis.git`).

#### Clone the Repository
Run the following command in the terminal:
```bash
git clone https://github.com/YourUsername/jarvis.git
```

#### Navigate into the Project Folder
After cloning, move into the project directory:
```bash
cd jarvis
```

#### Verify the Cloning
List the files in the directory to confirm successful cloning:
```bash
ls  # On Mac/Linux
dir # On Windows
```
This will download all project files and history to your local computer, ready for further setup.

---

### Step 2: Create a Virtual Environment

#### Install `virtualenv` (if not already installed):
```bash
pip install virtualenv
```

#### Create a Virtual Environment
In the project directory, run:
```bash
python -m virtualenv venv
```

#### Activate the Virtual Environment
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### Verify Activation
You’ll see `(venv)` in your terminal prompt.

Now proceed to install the required libraries. This keeps your environment clean and portable.

---

### Step 3: Install Dependencies
Since no `requirements.txt` file exists, manually install the required libraries:
```bash
pip install tensorflow
pip install eel
pip install pandas
pip install joblib
pip install scikit-learn
```

---

### Step 4: Add Required Files

#### Step 1: Ensure the Database File Exists
Verify that `jarvis.db` is present in the root directory of the project.

#### Step 2: Initialize the Database Tables
Use `db.py` or the following commands to create necessary tables:
- **System Commands Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS sys_command(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(1000)
  );
  ```
- **Web Commands Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS web_command(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    url VARCHAR(1000)
  );
  ```
- **Contacts Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY,
    name VARCHAR(200),
    mobile_no VARCHAR(255),
    email VARCHAR(255) NULL
  );
  ```

#### Step 3: Populate Tables
Add system and web commands using SQL queries or via `db.py`. For example:
- Add a system command:
  ```python
  query = "INSERT INTO sys_command VALUES (null, 'command prompt', 'c:\\Windows\\system32\\cmd.exe')"
  cursor.execute(query)
  con.commit()
  ```
- Add a web command:
  ```python
  query = "INSERT INTO web_command VALUES (null, 'google', 'https://www.google.com/')"
  cursor.execute(query)
  con.commit()
  ```

#### Step 4: Import Contacts
Place `contacts.csv` in the root directory with contact details formatted as:
```
Name,Mobile,Email
John Doe,1234567890,john@example.com
```
Modify and uncomment the `db.py` section for importing contacts:
```python
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        cursor.execute('INSERT INTO contacts VALUES (null, ?, ?, ?)', (row[0], row[1], row[2]))
con.commit()
```

#### Step 5: Use Database Queries
Search Contacts: Use `db.py` or the following SQL to search:
```python
cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ?", ('%search_query%',))
results = cursor.fetchall()
print(results)
```

---

### Step 5: Configure API Keys in `long__response.py`

To enable weather and news functionalities, users need to add their own API keys.

#### **Step 1: Obtain API Keys**
1. **Weather API Key**:
   - Visit [OpenWeatherMap](https://openweathermap.org/api) to sign up and get a free API key.
2. **News API Key**:
   - Visit [NewsAPI](https://newsapi.org/) to sign up and obtain an API key.

#### **Step 2: Update `long__response.py`**
- Open the `longresponse.py` file in any text editor.
- Replace the placeholder values with your API keys:
  ```python
  WEATHER_API_KEY = "your_weather_api_key_here"
  NEWS_API_KEY = "your_news_api_key_here"
  ```

#### **Step 3: Save the File**
- Save the changes and close the editor.

#### **Step 4: Verify the Setup**
- Run the application (`python run.py`) and test weather or news commands to confirm that the APIs are functioning.

---

### Step 6: Heart Disease Model Setup

#### To train or test the heart disease prediction model:
1. Ensure the `heart_disease_model.h5` file is in the project root.
2. If training is required:
   - Use `savefile.py` with a dataset named `heart.csv`.
   - Run:
     ```bash
     python savefile.py
     ```

---

### Step 7: Launch Jarvis
Start the application:
```bash
python run.py
```
