# Job Tracker API

A clean REST API to keep track of where you've applied. I built this to manage the chaos of job/internship hunting without using a messy spreadsheet.

## Project Structure

It’s pretty modular so it’s easy to find things:
- `app/main.py`: The entry point for FastAPI.
- `app/models.py`: Database tables (SQLAlchemy models).
- `app/schemas.py`: Data shapes for requests/responses (Pydantic).
- `app/routes/`: All the API endpoints split by category (`auth`, `users`, `applications`).
- `app/crud.py`: Logic for Create, Read, Update, Delete.
- `requirements.txt`: The libraries you need.

## Setup

1. **Virtual Env**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Check it out at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Auth & Users
| Method | Route | What it does |
|---|---|---|
| `POST` | `/auth/login` | Log in and get a JWT token |
| `POST` | `/users/` | Create a new user account |
| `GET`  | `/users/me` | Get your own profile (needs token) |

### Applications
| Method | Route | What it does |
|---|---|---|
| `GET`    | `/applications/` | List all applications |
| `POST`   | `/applications/` | Add a new one (needs token) |
| `PATCH`  | `/applications/{id}` | Update status (needs token) |
| `DELETE` | `/applications/{id}` | Remove an entry (needs token) |

## Notes

- **Why SQLite?** It's just a file (`app.db`). No need to install a heavy database server like PostgreSQL while just testing or building.
- **Why JWT?** It’s stateless. Instead of the server remembering who you are via sessions, the server gives you a signed "token" that you send back with every request.
- **FastAPI?** Because the auto-generated documentation (`/docs`) is a lifesaver.

## Quick Test (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/applications/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"company": "Google", "position": "Intern", "user_id": 1}'
```
<img width="1686" height="553" alt="image" src="https://github.com/user-attachments/assets/257d4545-ae14-4db4-8ff9-926e74ab819e" />


