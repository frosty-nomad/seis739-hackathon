# Party Guest List

A Flask web app for creating party lists and managing guests. Includes REST APIs plus simple HTML forms.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

2. Initialize the SQLite database:

```bash
python init_db.py
```

3. Run the app:

```bash
python run.py
```

Open `http://127.0.0.1:5000` in your browser.

Swagger UI is available at `http://127.0.0.1:5000/docs`.

## REST API Overview

Base URL: `http://127.0.0.1:5000/api`

- `GET /lists`
- `POST /lists` {"name": "Birthday Bash"}
- `GET /lists/<id>`
- `PUT /lists/<id>` {"name": "New name"}
- `DELETE /lists/<id>`

- `GET /guests`
- `POST /guests` {"name": "Alex", "email": "alex@email.com", "rsvp_status": "yes"}
- `GET /guests/<id>`
- `PUT /guests/<id>` {"name": "Alex", "email": "alex@email.com", "rsvp_status": "maybe"}
- `DELETE /guests/<id>`

- `GET /lists/<id>/guests`
- `POST /lists/<id>/guests` {"guest_id": 1} or {"name": "Alex", "rsvp_status": "pending"}
- `DELETE /lists/<id>/guests/<guest_id>`
