1. Application Blueprint

    Project Setup
        Initialize project repositories (frontend + backend).
        Choose frameworks (e.g., React for frontend, Node/Express or Python/FastAPI for backend).
        Configure linting, formatting, and basic CI/CD skeleton (GitHub Actions or similar).

    Authentication & User Roles
        Email/Password sign-up (JWT or session-based).
        Optional OAuth (e.g., Google) integration.
        Role-based access control (Creator vs. Player).

    Treasure Hunt Creation (Creator)
        Form to create hunts (title, theme, validation type).
        Photo uploads (up to 12).
        LLM calls: Vision → intermediate text → Text LLM → final clue text.
        Store hunts in database, link photos in S3-like storage.

    Treasure Hunt Sharing
        Generate unique URL/QR code.
        Share via link or email.

    Playing the Hunt (Player)
        Anonymous play for first 3 clues, then require login.
        Photo-based or GPS-based validation.
        Automatic hints after 5 failed attempts (photo-based).
        TTS for reading clues aloud.

    Leaderboards & Stats
        Track time to solve, attempts, etc.
        Provide a leaderboard per hunt.

    Expiration & Monetization
        Hunts expire after 3 months.
        Extend hunts up to 12 months for free; beyond that, use credits.
        Payment/credits system (Stripe or similar).
        Optional ads if user is not paying.

    Testing & Deployment
        Unit tests and integration tests.
        Staging environment and final production deployment.

2. First Iteration of Detailed Steps

We’ll divide the project into five chunks, each containing multiple steps:
Chunk A: Environment & Skeleton

    Repo Setup
        Initialize Git repositories for frontend & backend.
        Set up a basic README, code style guidelines, and a CI pipeline to run lint checks.

    Backend Boilerplate
        Create a basic server (Node/Express or FastAPI).
        One “hello world” endpoint to confirm everything runs.

    Frontend Boilerplate
        Use React/Vue CLI to bootstrap a single-page app.
        Basic landing page to confirm the frontend is served.

    Database Connection
        Choose DB type (PostgreSQL or MongoDB).
        Configure ORM/ODM (SQLAlchemy, TypeORM, Mongoose, etc.).
        Verify a sample model/table creation.

Chunk B: Authentication & Basic User Management

    User Model
        Fields: email, hashed password, role, creation date, etc.
        Migrations (if relational DB).

    Register & Login
        Endpoints: /api/auth/register, /api/auth/login.
        Validate input, hash passwords, generate JWT tokens.

    OAuth (Optional)
        Integrate Google or Facebook if desired.
        Store user info in DB upon first sign-in.

    Role Enforcement
        Middleware to check if user is Creator or Player when accessing certain endpoints.

Chunk C: Treasure Hunt Creation

    Hunt Model
        Fields: title, theme, validation method, expiration date, creator ID, etc.

    Clue Model
        Fields: clue text, image path, GPS coords, parent hunt, order index (1–12), etc.

    Photo Upload Handling
        REST endpoint to receive an image, store in S3-like bucket, return file key/URL.

    Vision LLM Integration
        After upload, call Vision LLM to get the “intermediate description.”
        (In real usage, handle rate limits, errors, etc.)

    Text LLM Integration
        Combine the intermediate description + prior clues + optional theme → final clue text.
        Store the final text in the DB.

    Hunt Creation Flow
        Single endpoint (or multiple steps) to create hunts, receive photos, generate clues, etc.

    Sharing Mechanism
        Generate a unique slug/ID for the hunt.
        Create a route to serve the public link/QR code.

Chunk D: Playing the Hunt

    Anonymous vs. Authenticated Flow
        Let anonymous users access up to 3 clues.
        Prompt for login/registration after 3rd clue.

    Retrieving Clues
        Endpoint to fetch the next clue in the sequence.
        Check that the previous clue was solved.

    Validating Solutions
        Photo-Based:
            Upload photo → Vision LLM → new text → compare with original clue text using Text LLM.
            If “similar enough,” mark clue as solved.
            After 5 failures, generate an additional hint.
        GPS-Based:
            Compare user’s lat/long with stored coordinates.
            If within radius, solve the clue.

    Hint Generation
        Use the original clue text to generate a more revealing hint if needed.

    Leaderboard & Stats
        Track time to solve each clue, total attempts, etc.
        Update a hunt-specific leaderboard table.

Chunk E: Monetization, Extensions & TTS

    Hunt Expiration & Extension
        3-month default, up to 12 months free extension.
        Beyond that, user pays with credits.

    Credits & Payments
        Integrate with a payment provider (Stripe/PayPal).
        Purchase credits, deduct when creating hunts or extending them.

    Ad Integration (if needed)
        Basic ad placeholders in the UI for free players.

    Text-to-Speech
        Use an API to render clue text as audio.
        Provide a “listen” button in the UI.

    Final Polishing & Deployment
        Review security, QA tests, deploy to production.

3. Second Iteration — Break Down Each Chunk Further

Let’s expand each chunk’s steps into smaller tasks, ensuring they’re small enough to be safe but large enough to move the project forward.
Chunk A: Environment & Skeleton (Expanded)

    Repo Initialization
        Create GitHub repos: treasure-hunt-frontend and treasure-hunt-backend.
        Add .gitignore for Node/Python.
        Push initial commit.

    Backend Boilerplate
        npm init -y (Node) or pip install fastapi + create main file (Python).
        Implement a simple route (GET /health) returning { status: 'ok' }.
        Confirm it runs locally.

    Frontend Boilerplate
        npx create-react-app treasure-hunt-frontend or equivalent.
        Replace the default content with a minimal landing page.
        Confirm it serves locally at http://localhost:3000 (React default).

    Database Connection
        For Node: set up sequelize or mongoose.
        For Python: set up SQLAlchemy.
        Configure .env with DB credentials.
        Add a test model + migration if necessary.
        Confirm you can read/write from the DB.

Chunk B: Authentication & Basic User Management (Expanded)

    User Model
        Decide fields: email, password_hash, role, created_at.
        Create DB migrations/tables.

    Registration Endpoint
        Input validation (email, password length, etc.).
        Hash password (bcrypt or similar).
        Save user to DB.
        Return success or error message.

    Login Endpoint
        Verify user email + password.
        If valid, issue JWT with user ID + role.
        Return token to client.

    OAuth (Optional)
        If implementing, create an endpoint using Google OAuth library.
        On success, store user email + token in DB.

    Role Enforcement
        Middleware that reads JWT, checks DB if user is valid.
        If role = Creator, allow certain endpoints; else, reject or redirect.

Chunk C: Treasure Hunt Creation (Expanded)

    Hunt & Clue Models
        Hunt table: id, title, theme, validationType, creatorId, expiryDate, etc.
        Clue table: id, huntId, clueText, photoKey, gpsCoords, orderIndex, etc.

    Photo Upload
        Create an endpoint /api/hunt/upload-photo.
        Configure integration with S3-like storage (AWS, GCP, etc.).
        Save file key in DB or return to client.

    LLM Integration
        On server side, after uploading, call Vision LLM with the photo.
        Filter out people/animals/vehicles in the response.
        Send that text plus existing clues + theme to Text LLM → final clue text.
        Save final clue text in DB.

    Create Hunt Flow
        Endpoint /api/hunt/create that:
            Creates a new Hunt record.
            Accepts each clue photo in sequence (or in a loop).
            Generates final clue text.
            Stores everything in DB.
        Deduct credits from the Creator, if relevant.

    Sharing Mechanism
        Generate a unique slug/URL for the hunt, e.g. treasurehunt.com/play/:slug.
        Possibly generate a QR code image using a library.
        Return link + QR code data to the creator.

Chunk D: Playing the Hunt (Expanded)

    Anonymous vs. Auth
        If no token, user can request up to 3 clues.
        On request for 4th clue, prompt for login.

    Fetch Next Clue
        /api/play/hunt/:huntId/clue/:index
        Checks if the user solved the previous index.
        Returns the clue text (or indicates if it’s GPS-based).

    Solve Clue (Photo-Based)
        /api/play/hunt/:huntId/clue/:index/solve-photo
        Upload the player photo → Vision LLM → text → compare with original clue text (Text LLM).
        If similarity > threshold, mark as solved. Otherwise, increment fail count.

    Solve Clue (GPS-Based)
        /api/play/hunt/:huntId/clue/:index/solve-gps
        Compare lat/long with stored coords.
        If within radius, mark solved.

    Hint Generation
        If fail count >= 5, request a hint from the Text LLM using the stored clue text.
        Return the hint to the player.

    Leaderboard & Stats
        Record time started, time solved.
        On final clue solve, update the total time in a leaderboard table or similar.
        Return an updated scoreboard.

Chunk E: Monetization, Extensions & TTS (Expanded)

    Hunt Expiration
        A background job or cron checks hunts that pass 3 months.
        Mark them as expired unless extended by the creator.
        Let creator extend hunts up to 12 months for free.

    Credits & Payments
        Create a credits field in the user table.
        Integrate Stripe or PayPal for purchasing credits.
        Deduct credits for hunts that exceed free extension periods.

    Ads (Optional)
        If user is not a paying player, show ad placeholders on the clue screens.

    Text-to-Speech
        Add a small button next to each clue: “Listen to the clue.”
        When clicked, call an endpoint that returns an audio URL or base64 chunk.
        Possibly integrate an external TTS API or OpenAI’s TTS equivalent.

    Final Deployment
        Dockerize or deploy to a cloud platform (AWS, Azure, etc.).
        Configure environment variables, logs, monitoring.
        Perform final security checks (HTTPS only).

4. Third Iteration — Final Check on Step Sizes

    Each step is small enough to be tackled in a single iteration or sprint.
    Each sub-step naturally builds on the prior step (e.g., you must have the photo upload before integrating the LLM for clues).
    No major leaps in complexity occur before the prior foundation is in place.

We can proceed with confidence that these are well-sized tasks.
5. Code-Generation Prompts

Below is an example set of prompts for a code-generation LLM. Each section is in a code block, labeled as text (so that you can feed it into your codegen tool). Every prompt references previous steps, ensuring continuity. You can adapt them for your specific LLM context (e.g., “system” messages or “user” messages).
Prompt 1: Initialize Backend

Please generate a Node.js (Express) backend boilerplate. Requirements:
- A simple Express app with TypeScript (if possible).
- A single /health endpoint returning { status: 'ok' }.
- Include minimal scripts for "dev" and "start".
- Use ESLint with a recommended config.
- Include a basic folder structure: /src for code, /src/routes for endpoints.

Prompt 2: Connect to Database

We have the Express code from Prompt 1. Extend it to connect to a PostgreSQL database using TypeORM.
Requirements:
- Add a `User` entity with fields: id (uuid), email (string), passwordHash (string), role (enum: CREATOR or PLAYER), createdAt.
- Add migration scripts.
- Update "dev" script to run DB migrations on startup.

Prompt 3: Implement Registration & Login

Using the existing Express + TypeORM backend:
1. Create a POST /auth/register endpoint that:
   - Accepts { email, password, role }.
   - Hashes the password using bcrypt.
   - Saves user to DB.
2. Create a POST /auth/login endpoint:
   - Verifies email/password.
   - Issues a JWT with user ID + role as payload.
3. Add a middleware to protect routes, reading the JWT.

Prompt 4: Creator-Only Endpoint

Extend the code from Prompt 3. Add a new route /creator/test that:
- Checks if the user's role is CREATOR via the JWT.
- Returns a success message if CREATOR, else 403 Forbidden.

Prompt 5: Frontend Setup

Generate a React-based frontend (TypeScript if possible):
1. Create a login form that calls POST /auth/login, storing the returned JWT in localStorage.
2. Create a register form that calls POST /auth/register.
3. If the user is logged in and role=CREATOR, show a "Creator Portal" link.
   - Otherwise, hide that link.

Prompt 6: Hunt & Clue Models

Back to the backend code:
1. Create a Hunt entity with: id, title, theme, validationType (enum: PHOTO or GPS), creatorId (FK to User), expiryDate, createdAt.
2. Create a Clue entity with: id, huntId (FK), orderIndex (int), clueText (string), photoKey (string, nullable), gpsCoords (string, nullable).
3. Generate necessary migrations and relations (OneToMany from Hunt to Clues).

Prompt 7: Photo Upload Endpoint

Enhance the backend:
1. Add a POST /hunt/upload-photo that:
   - Accepts a file upload (use multer or similar).
   - Saves it to S3 (or mock it locally if we lack S3 credentials).
   - Returns a JSON object with { photoKey }.
2. Make sure to protect it so only authenticated users can upload.

Prompt 8: Integrate Vision LLM (Mock) and Generate Clue Text

We don't have actual LLM keys for now. Simulate the Vision LLM call:
1. Create a function `callVisionMock(photoKey)` that returns a sample description (pretending to remove animals/people/vehicles).
2. Create a function `callTextMock(intermediateDescription, priorClues, theme)` returning a simulated final clue text.
3. In a new endpoint /hunt/create-clue:
   - Accept { huntId, photoKey, orderIndex }.
   - Call callVisionMock -> get intermediate text.
   - Gather prior clues from DB, plus the hunt theme -> callTextMock.
   - Create a new Clue record with the final text.

Prompt 9: Full Hunt Creation Flow

Combine the endpoints from Prompt 7 and 8:
1. A POST /hunt/create that:
   - Accepts { title, theme, validationType }.
   - Creates a Hunt record.
   - Then for each photo, calls /hunt/create-clue to generate clues.
2. Return the newly created Hunt with all Clue details.

Prompt 10: Sharing Hunt (Slug + QR)

Update the code:
1. Add a slug field to Hunt (random or based on title + shortid).
2. Provide a GET /hunt/:slug endpoint that returns the hunt details (title, number of clues, etc.).
3. Generate a QR code using a library like 'qrcode'. Return a data URL or store it in S3.
4. Adjust the create flow to return { slug, qrCodeURL } after creation.

Prompt 11: Playing Hunts - Anonymous vs. Auth

Add a new route for players:
1. GET /play/:slug/clue/:index:
   - Checks if user is logged in or not. If not, track the total number of clues accessed by session or IP.
   - If the user is accessing the 4th clue and is not logged in, return a message "Please register or log in".
   - Otherwise, return the clue details (clueText if photo-based, or "GPS required" if gps-based).

Prompt 12: Solve Clue (Photo-Based) & Hints

Add a POST /play/:slug/clue/:index/solve-photo:
1. Accept a photo upload from the player.
2. Call the Vision mock -> get text -> call the Text mock to check similarity with the clue's text.
3. If similarity > threshold, mark clue as solved in DB.
4. If not, increment fail count. If fail count >=5, also generate a hint from the stored clue text.
5. Return success/failure + hint if applicable.

Prompt 13: Solve Clue (GPS-Based)

Add a POST /play/:slug/clue/:index/solve-gps:
1. Accept the player's lat/long from the request body.
2. Compare with the clue's stored gpsCoords. If within a certain radius, mark solved.
3. Otherwise, respond with 'incorrect location'.

Prompt 14: Leaderboard & Stats

Add a new table Leaderboard with fields: id, huntId, userId, totalTime, attempts, createdAt.
1. When a user solves the final clue:
   - Calculate total time from first clue start to last clue solve.
   - Store or update a record in Leaderboard.
2. Create a GET /hunt/:slug/leaderboard that returns the top results.

Prompt 15: Hunt Expiration & Extension

Implement expiration logic:
1. Add a daily cron job or background worker that checks hunts' createdAt + 3 months.
2. If time is exceeded, set a boolean "isExpired" on the hunt.
3. Add a PATCH /hunt/extend endpoint for a creator to extend the expiryDate up to 12 months total, free.
4. Beyond 12 months, verify the user has enough credits. Deduct credits if extension is requested.

Prompt 16: Credits & Payment Integration

Add 'credits' to the User table. For now, just a numeric field.
1. Add a POST /payments/purchase-credits that increments credits.
2. Each time a new Hunt is created or extended beyond 12 months, deduct the correct amount.
3. Return the updated credit balance to the creator.

Prompt 17: Text-to-Speech Integration

Add a TTS feature:
1. Add a GET /play/:slug/clue/:index/tts.
2. For now, mock the TTS with a placeholder audio file or text "TTS not implemented".
3. In the future, integrate a real TTS API (e.g., Amazon Polly, Google TTS, or OpenAI).

Prompt 18: Final Polishing & Deployment

1. Add final error-handling middlewares (404, 500).
2. Add environment variable config (production vs. development).
3. Dockerize both frontend and backend.
4. Provide instructions on how to run docker-compose up to start the entire app.

End of Prompts

You now have a series of stepwise prompts that, when executed in sequence by a code-generation LLM, should produce an integrated Treasure Hunt application. Each prompt references and builds on prior code, ensuring no orphaned or hanging modules.
Wrap-Up

By following this plan:

    You have a multi-phase approach (environment, auth, hunt creation, play flow, monetization, TTS).
    Each phase is broken into small, iterative steps.
    Each prompt is standalone yet builds on the previous work.

This provides a robust structure for safe, incremental development with minimal risk of large, untested code jumps. Once completed, you’ll have a fully functional Treasure Hunt web application with AI-driven clues, linear progression, monetization, and basic TTS readiness.