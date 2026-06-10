# LeoGram — Mini Instagram REST API

## Tech Stack
- **Python 3.13**
- **Django 6.0** — backend web framework
- **Django REST Framework** — REST API endpoints
- **PostgreSQL 17** — database
- **Redis 7** — cache (rate limiting)
- **MinIO** — S3-compatible object storage for images
- **SimpleJWT** — JWT authentication
- **Docker & Docker Compose** — containerized setup

## Architecture
The project follows a strict two-layer architecture:
- **API Layer** (`api/`) — receives HTTP requests, validates input via serializers, sends responses. No business logic.
- **Actions Layer** (`actions/`) — all business logic and database operations. No HTTP or serializer code.
```
leogram/
  apps/
    accounts/
      api/          → serializers, views, urls
      actions/      → business logic
      models.py
      tests/
        unit/
        integration/
    posts/
      api/          → serializers, views, urls
      actions/      → business logic
      models.py
      tests/
        unit/
        integration/
  config/
    settings.py
    urls.py
Dockerfile
docker-compose.yml
pyproject.toml
```
## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Setup

1. Clone the repository:
```
git clone https://github.com/leonardovreka/leogram.git
cd leogram
```

2. Create your environment file:
```
cp .env.example .env
```

3. Fill in your values in `.env` — see `.env.example` for all required variables

4. Start everything with one command:
```
docker compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register — sends verification email |
| POST | `/api/auth/login` | Login with email or username |
| POST | `/api/auth/logout` | Logout — invalidates token |
| POST | `/api/auth/token/refresh` | Refresh access token |
| POST | `/api/auth/email/confirm` | Confirm email with token (single-use) |
| POST | `/api/auth/email/resend` | Resend verification email (rate limited) |
| POST | `/api/auth/password/reset-request` | Request password reset (generic response) |
| POST | `/api/auth/password/reset-confirm` | Confirm password reset with token |

### Users & Follows
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/{username}/follow` | Follow a user |
| POST | `/api/users/{username}/unfollow` | Unfollow a user |
| POST | `/api/follows/{id}/accept` | Accept follow request (followee only) |
| POST | `/api/follows/{id}/reject` | Reject follow request |
| GET | `/api/users/{username}/followers` | List followers |
| GET | `/api/users/{username}/following` | List following |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts/` | Create post with image (multipart) |
| GET | `/api/posts/feed` | Get feed from followed users |
| GET | `/api/posts/{id}` | Get a single post |
| DELETE | `/api/posts/{id}` | Delete own post |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts/{id}/comments` | Add a comment |
| GET | `/api/posts/{id}/comments` | List comments on a post |
| DELETE | `/api/comments/{id}` | Delete own comment |

## Running Tests
- docker compose exec api uv run pytest apps/ -v

## Key Features
- Email verification — new accounts must confirm email before logging in
- JWT authentication with token blacklisting on logout
- Rate limiting on sensitive endpoints (email resend, password reset)
- Generic password reset responses to prevent user enumeration
- Image validation, compression and resize via Pillow before upload to MinIO
- Layered architecture — API layer never contains business logic
- 80+ tests covering unit and integration scenarios
