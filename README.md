# Passport Extractor


Push this repo to GitHub and connect to Render to host.


## Quick deploy
1. Create a GitHub repo and push all files.
2. On Render.com: New -> Web Service -> Connect to GitHub -> select repo.
3. Choose branch (main), environment: Docker.
4. Render will build your Dockerfile and deploy. The app listens on port 8000 by default.


## Usage
POST `/upload` with multipart form `file`=your.pdf
- single crop -> returns JPG
- multiple crops -> returns a zip of JPGs


Example using `curl`:
