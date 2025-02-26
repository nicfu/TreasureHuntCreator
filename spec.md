Treasure Hunt App Specification
1. High-Level Overview

Build a web-based treasure hunt platform with two primary user roles:

    Creator
        Must register for an account (email/password or OAuth).
        Can create treasure hunts (up to 12 clues), each automatically generated from user-uploaded photos.
        Selects one validation method (photo-based or GPS) for the entire hunt.
        Can share hunts via email, link, or QR code.
        Receives stats/leaderboard info about who played and how quickly they solved each clue.
        Can extend hunts beyond a default 3-month expiry, up to 12 months for free, and then pay (using credits) to extend further.

    Player
        Can access the treasure hunt without registering for the first 3 clues.
        Must register an account to continue after 3 clues.
        Receives clues in a strict linear order.
        Submits photos (or provides GPS location) to validate solutions.
        Has access to an in-game “hint” if they fail a clue 5 times.
        May see ads if playing for free (depending on monetization setup).

AI Components

    Vision LLM (OpenAI Vision) for describing images.
    Text LLM (e.g., GPT-3.5) for generating clue text and validating similarity between images.

2. Functional Requirements
2.1. Account Creation and Authentication

    Roles: Creator vs. Player
    
    Methods:
        Email/Password sign-up
        OAuth (e.g., Google, Facebook) if desired

    Flow:
        Creators must be authenticated to create hunts.
        Players can play the first 3 clues anonymously, but must register to continue.

2.2. Treasure Hunt Creation

    Clue Limit: Up to 12 clues per hunt.

    Clue Generation:
        Creator uploads a photo for each clue.
        Photo → Vision LLM to get a textual description (excluding animals, people, vehicles).
        Description + prior clues + optional theme → Text LLM → final clue text (automated, no manual edits).

    Validation Method:
        Creator chooses Photo Matching or GPS for all clues in that hunt.

    Themes:
        Choose from a small set (e.g., “spooky,” “pirate,” etc.) or no theme.
        The Text LLM shapes style and difficulty accordingly.

2.3. Hunt Sharing

    Method:
        The system generates a unique URL or QR code, shared via email or messaging.

    Access:
        Scanning the QR code or clicking the link opens the web app at the introduction/first clue.
        If the user isn’t logged in, they can still try up to 3 clues before registering.

2.4. Hunt Playing

    Clue Progression:
        Strictly linear. Each clue unlocks only after the previous one is solved.

    Photo/Location Submission:
        Photo-Based:
            Player uploads/takes a photo.
            App sends the photo → Vision LLM → get a description.
            Compare new description to the original clue’s text (using the Text LLM for similarity).
            If matched, proceed to next clue; if not, user tries again.
            After 5 failures, provide an extra hint generated from the original text.

        GPS-Based:
            Player’s device location is compared to the stored GPS coordinates for the clue.
            If within the allowed radius, proceed to next clue; else, display an error.

    Hints:
        Free extra clue text after 5 failed attempts (photo-based).
        No “attempts remaining” indicator is displayed.

    Expiration:
        Hunts remain active for 3 months by default.
        Creators can extend hunts to a total of 12 months for free.
        Beyond 12 months, credits are required for further extension.

2.5. Scoring & Leaderboards

    Tracking:
        Time taken to solve each clue, number of attempts, total completion time, etc.

    Leaderboard Visibility:
        Each hunt has its own leaderboard, visible to the creator and players who have the link.

2.6. Notifications

    Push/Email (if applicable):
        Notify creators when someone finishes or is stuck.
        Remind players if they are inactive or the hunt is extended.

2.7. Text-to-Speech (TTS)

    Language: English only, initially.

    Implementation:
        Leverage OpenAI (e.g., Whisper or another TTS-compatible model).
        Clues can be read aloud, especially useful for young children.

3. System Architecture

flowchart LR
    A[Web Frontend<br>(React/Vue)] -- HTTPS --> B[Backend Server/REST API<br>(Python Flask)]
    B -- API calls --> C[OpenAI Vision Model]
    B -- API calls --> D[OpenAI Text Model]
    B -- Database Calls --> E[Database<br>(SQL/NoSQL)]

    Frontend:
        Mobile-responsive web app (React, Vue).

    Backend:
        Python (Flask)
        Manages user accounts, hunts, photo uploads, clue generation, game state, and scoring.

    Database:
        Relational (PostgreSQL).
        Stores user data, hunts, clues, photos, leaderboards, etc.

4. Data Handling
4.1. Storage

    Photos:
        Store in an S3-like bucket (AWS S3, GCP Cloud Storage).
        Database references file paths or object keys.

    Clue Descriptions:
        Vision LLM → raw text.
        Text LLM → final clue text.
        Store the description of the image and the clue text in the DB with references to the hunts/clues/photo.

    User Data:
        Basic profile info (email, hashed password or OAuth tokens).
        Credits, hunts created, hunts played, etc.

    Leaderboard:
        Either a separate table per hunt or a combined table with hunt IDs for reference.

4.2. Security & Privacy

    No content moderation for images (per requirements).

    Access Control:
        Only the hunt’s creator or authorized players can see clue data.
        Leaderboard is visible to anyone who has the hunt link/QR code.

    Encryption:
        All traffic over HTTPS.
        Private bucket or pre-signed URLs for photo access.

5. Monetization & Credits

    Ads:
        Potentially served to players who don’t purchase credits or as an additional revenue stream.

    Credits:
        Used by creators to create hunts or extend them beyond 12 months.
        Purchase via in-app purchase or web-based checkout (Stripe, PayPal, etc.).

    Usage:
        Each new hunt consumes a certain credit amount.
        Extending hunts past the free 12-month period also consumes credits.

6. Implementation Details
6.1. Flow for Creating a Treasure Hunt

    Creator logs in.
    Click “Create New Hunt”:
        Enter hunt title, optional theme, and choose validation method (photo or GPS).

        For each of up to 12 clues:
            Upload a photo (stored in object storage).
            Photo → Vision LLM → textual description (excluding animals, people, vehicles).
            Text + prior clues + theme → Text LLM → final clue text.
        Store the hunt in the DB (photos, descriptions, final text).
        Deduct the corresponding credits from the creator’s account.

    Share:
        Generate a unique link and QR code for the hunt.
        Creator sends via email or any preferred channel.

6.2. Flow for Playing a Treasure Hunt

    Open Link/Scan QR.

        Launches the web app with the hunt ID.
        Shows intro and first clue.
        Player can remain anonymous for 3 clues.

    Solve Clues:

        If photo-based:
            Player uploads or takes a photo.
            Photo → Vision LLM → new textual description.
            Compare via Text LLM with stored clue description.
            If match, proceed to next clue; if not, prompt another attempt.
            After 5 fails, generate a hint (Text LLM) and display.

        If GPS-based:
            Compare player’s device lat/long to stored coordinates.
            If within threshold, proceed; else show “incorrect location.”

    Completion:

        Track time, attempts, etc.
        Update the hunt-specific leaderboard in the DB.

6.3. Hunt Expiration

    3-Month Default:
        Auto-expire 3 months after creation.

    Extension:
        Creator can extend up to 12 months total at no cost.
        Beyond 12 months, pay credits to continue extending.

7. Error Handling Strategies

    Vision LLM Errors (e.g., rate limit):
        Retry (1-3 times with backoff).
        If persistent, display error; allow user to retry upload or clue generation.

    Text LLM Errors:
        Similar retry approach.
        If repeated failure, store error and prompt user to try again.

    Photo Upload Errors:
        Check file size/type.
        On failure, allow re-upload.

    GPS Validation Issues:
        If user denies location, notify them or consider fallback.
        If error in retrieval, offer manual retry.

    Payment Failures:
        Show descriptive messages.
        Log transaction details in server for support.

8. Testing & QA Plan

    Unit Tests:
        Cover API endpoints (e.g., user registration, clue creation, clue retrieval).
        Test credits logic (purchasing, usage, extension).

    Integration Tests:
        End-to-end scenario: create hunt → upload photos → generate clues → share link → play clues → verify LLM calls.
        Validate leaderboard updates.

    UI/UX Tests:
        Check mobile responsiveness.
        Validate TTS functionality (audio playback).

    Performance Tests:
        Evaluate concurrency with multiple users/players simultaneously.
        Monitor API performance with LLM calls.

    Security Tests:
        Verify only authenticated creators can create hunts.
        Ensure hunts stay private unless shared.
        Confirm no direct access to photo storage except through authenticated requests.

    LLM Accuracy Tests:
        Confirm Vision LLM is excluding animals, people, vehicles.
        Validate clue text generation.
        Check similarity results for correctness in photo-based validation.

9. Future Enhancements (Optional)

    Multi-language Support for text and TTS.
    Offline or Caching for partially disconnected experiences.
    Advanced Theming (deeper styling guidelines and clue difficulty).
    Content Moderation for images (if needed).
    Non-Linear Hunts with branching clues or open-world design.

Summary

This specification outlines a web-based treasure hunt app leveraging OpenAI for image-to-text and text-based clue generation and verification. It details monetization (ads plus credits), strict linear progression, an optional hint system, and a hunt-specific leaderboard. Data management includes S3-like photo storage and a database for hunts, clues, leaderboards, and user accounts. Hunts expire after 3 months, extendable up to 12 months for free, then further extensions require credits.