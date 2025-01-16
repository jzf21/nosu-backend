### Backend Setup Instructions

### 1. Clone the Repository  
```bash
git clone https://github.com/jzf21/nosu-backend.git
```
cd nosu-backend

### 2. Create and Activate Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables:

Create a .env file in the root directory of the project.

Copy the contents of .env.example into the .env file.

Replace the placeholders in the .env file with your actual credentials.

### 5. Start the Application:

```bash
uvicorn main:app --reload
```
