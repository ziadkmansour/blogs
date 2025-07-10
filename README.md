# FastAPI Blog Project

This is a simple blog API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- User registration
- Create, read, update, and delete blog posts
- Password hashing for user security
- Modular routing

## Project Structure

```
blog/
    main.py
    models.py
    schemas.py
    database.py
    utils.py
    routers/
        blog.py
        user.py
    requirements.txt
blog.db
```

## Setup

1. **Clone the repository**

2. **Create a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r blog/requirements.txt
   ```

4. **Run the application**
   ```sh
   uvicorn blog.main:app --reload
   ```

5. **Access the API docs**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- Passlib

## License

MIT