# To-Do Checklist

## Chunk A: Environment & Skeleton

### Repo Initialization
- [ ] Create separate GitHub repos: `treasure-hunt-frontend` and `treasure-hunt-backend`.
- [ ] Add appropriate `.gitignore` files for Node/Python.
- [ ] Initialize with a basic README, push an initial commit.

### Backend Boilerplate
- [ ] Initialize the backend (`npm init -y` for Node or Python FastAPI, etc.).
- [ ] Create a minimal server file (e.g., `app.js` or `main.py`).
- [ ] Add a `/health` endpoint returning `{ status: 'ok' }`.
- [ ] Confirm it runs locally.

### Frontend Boilerplate
- [ ] Scaffold a React/Vue/Angular app (e.g., `create-react-app treasure-hunt-frontend`).
- [ ] Replace default content with a minimal landing page.
- [ ] Confirm local serve at `http://localhost:<port>`.

### Database Connection
- [ ] Choose and install DB libraries (e.g., `sequelize`, `typeorm`, `mongoose`, or `SQLAlchemy`).
- [ ] Configure `.env` for DB credentials (e.g., host, port, user, password).
- [ ] Create a small test model/table to confirm read/write ops.
- [ ] Verify migrations work (if using a relational DB).

## Chunk B: Authentication & Basic User Management

### User Model
- [ ] Create a `User` model/entity with:
  - [ ] `id` (UUID or auto-generated primary key)
  - [ ] `email` (unique)
  - [ ] `passwordHash` (string)
  - [ ] `role` (enum: `CREATOR` or `PLAYER`)
  - [ ] `createdAt` (timestamp)

### Registration Endpoint
- [ ] `POST /auth/register`
  - [ ] Validate email/password.
  - [ ] Hash the password (`bcrypt` or similar).
  - [ ] Save user to DB.
  - [ ] Return success or error.

### Login Endpoint
- [ ] `POST /auth/login`
  - [ ] Verify credentials (email + password).
  - [ ] If valid, generate JWT (with user id + role).
  - [ ] Return token to client.

### OAuth (Optional)
- [ ] Integrate Google/Facebook sign-in if desired.
- [ ] On success, store user info in DB.

### Role Enforcement
- [ ] Create middleware that checks JWT from header.
- [ ] Confirm user role matches the required endpoint role.
- [ ] Return `403` if unauthorized, or pass to next handler.

## Chunk C: Treasure Hunt Creation

### Hunt & Clue Models
- [ ] Hunt table:
  - [ ] `id`, `title`, `theme`, `validationType` (PHOTO or GPS), `creatorId` (FK), `expiryDate`, etc.
- [ ] Clue table:
  - [ ] `id`, `huntId` (FK), `clueText`, `photoKey`, `gpsCoords`, `orderIndex`, etc.
- [ ] Establish relationships (`OneToMany`, etc.) in the ORM/ODM.

### Photo Upload Handling
- [ ] Create an endpoint `/api/hunt/upload-photo`
- [ ] Accept a file via `multipart/form-data`.
- [ ] Store file in S3-like object storage.
- [ ] Return `photoKey` or URL.

### Vision LLM Integration (Mock/Real)
- [ ] After upload, send image to a Vision LLM (or mock).
- [ ] Filter out disallowed categories (people/animals/vehicles).
- [ ] Receive an intermediate text description.

### Text LLM Integration (Mock/Real)
- [ ] Combine intermediate text + prior clues + theme.
- [ ] Generate final clue text.
- [ ] Save final text to DB.

### Hunt Creation Flow
- [ ] Endpoint `/api/hunt/create`
- [ ] Accept hunt details: title, theme, validation method, etc.
- [ ] Insert new Hunt record in DB.
- [ ] For each clue photo, call the Vision LLM, then the Text LLM, and store.
- [ ] Deduct credits from the Creator if necessary.

### Sharing Mechanism
- [ ] Generate a unique slug or ID for each hunt.
- [ ] Possibly generate a QR code referencing this slug/ID.
- [ ] Return the shareable link + QR code.

## Chunk D: Playing the Hunt

### Anonymous vs. Authenticated Flow
- [ ] Allow up to 3 clues without logging in.
- [ ] Enforce login before accessing clue #4 and onwards.

### Retrieving Clues
- [ ] `GET /play/:slug/clue/:index`
- [ ] Check if user solved previous clue (or track in session if anonymous).
- [ ] Return clue text (or GPS instructions).
- [ ] If user has not solved previous clue, block access.

### Validating Solutions (Photo-Based)
- [ ] `POST /play/:slug/clue/:index/solve-photo`
- [ ] Accept photo upload.
- [ ] Call Vision LLM → text, then check similarity with stored clue text (Text LLM).
- [ ] If match, mark clue as solved. Else, increment fail count.
- [ ] After 5 fails, generate & return a hint.

### Validating Solutions (GPS-Based)
- [ ] `POST /play/:slug/clue/:index/solve-gps`
- [ ] Accept lat/long from user.
- [ ] Compare to stored coords (plus radius).
- [ ] Mark solved if within range.

### Hint Generation
- [ ] If fail count >= 5 on a photo-based clue:
- [ ] Re-query the Text LLM with the clue text for a more revealing hint.
- [ ] Return hint to player.

### Leaderboard & Stats
- [ ] Create a table or model for storing results:
- [ ] When final clue is solved, record total time, attempts, etc.
- [ ] `GET /hunt/:slug/leaderboard` to retrieve scoreboard.

## Chunk E: Monetization, Extensions & TTS

### Hunt Expiration
- [ ] Default 3-month expiry from creation date.
- [ ] Add a background/cron job to mark hunts as expired beyond that date.
- [ ] Let creators extend hunts up to 12 months total for free.

### Credits & Payment
- [ ] Add credits to the `User` model.
- [ ] `POST /payments/purchase-credits` to buy credits (integrate Stripe/PayPal if real).
- [ ] Deduct credits for extended hunts beyond 12 months or for new hunts if that’s the monetization model.

### Ad Integration (Optional)
- [ ] Insert ad placeholders on clue pages for non-paying users.

### Text-to-Speech (TTS)
- [ ] Add a button to fetch audio for each clue:
- [ ] `GET /play/:slug/clue/:index/tts`
- [ ] Integrate a TTS API (or mock with a placeholder audio file).

## Final Polishing & Deployment

### Additional Testing & QA Steps

#### Unit Tests
- [ ] For each backend endpoint (auth, hunts, clues, etc.).
- [ ] For frontend components (if using Jest or similar).

#### Integration Tests
- [ ] End-to-end scenario: create hunt → share link → solve clues → record leaderboard.

#### UI/UX Tests
- [ ] Check mobile responsiveness.
- [ ] Ensure TTS buttons work on various devices.

#### Performance Tests
- [ ] Basic load tests on essential endpoints.
- [ ] Evaluate concurrency with multiple players.

#### Security Checks
- [ ] Validate that only authenticated creators can create hunts.
- [ ] Confirm private hunts are only accessed by link/slug.
- [ ] Enforce HTTPS, secure tokens, etc.
