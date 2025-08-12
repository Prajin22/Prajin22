# Deployment Guide for LinkedIn Job Portal

## Option 1: Deploy to Render (Recommended - Free)

### Step 1: Prepare Your Repository
1. Make sure all your code is committed to GitHub
2. Ensure you have these files in your root directory:
   - `main.py` (your Flask app)
   - `requirements.txt` (with all dependencies)
   - `render.yaml` (deployment configuration)
   - `static/` folder (CSS, JS, images)
   - `templates/` folder (HTML templates)

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect it's a Python app
5. Set the following:
   - **Name**: linkedin-job-portal
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
6. Click "Create Web Service"
7. Render will automatically deploy your app

### Step 3: Set Environment Variables
In Render dashboard, go to your service → Environment → Add:
- `ENCRYPTION_KEY`: Generate a random 32-byte key
- `SECRET_KEY`: Generate a random secret key
- `FLASK_ENV`: production

## Option 2: Deploy to Railway

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Deploy
```bash
railway login
railway init
railway up
```

## Option 3: Deploy to Heroku

### Step 1: Install Heroku CLI
Download from [heroku.com](https://heroku.com)

### Step 2: Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## Option 4: Local Production Testing

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variables
```bash
# Windows PowerShell
$env:ENCRYPTION_KEY="your_32_byte_key_here"
$env:SECRET_KEY="your_secret_key_here"
$env:FLASK_ENV="production"

# Or create a .env file (not committed to git)
```

### Step 3: Run Production Server
```bash
gunicorn main:app --bind 0.0.0.0:8000
```

## Important Notes

### Database
- Your current SQLite database will work locally
- For production, consider using PostgreSQL (Render provides this)
- Update `DATABASE_URL` in production

### Security
- Never commit `.env` files
- Use strong, randomly generated keys
- Enable HTTPS in production

### Performance
- Use `gunicorn` instead of Flask's built-in server
- Consider adding Redis for session storage
- Implement proper logging

## Quick Start Commands

```bash
# Install production dependencies
pip install -r requirements.txt

# Test locally with production server
gunicorn main:app --bind 0.0.0.0:8000

# Or use Flask with production settings
set FLASK_ENV=production
python main.py
```

## Troubleshooting

### Common Issues:
1. **Port already in use**: Change port in gunicorn command
2. **Database errors**: Ensure database file exists and is writable
3. **Import errors**: Check all dependencies are in requirements.txt
4. **Environment variables**: Ensure all required vars are set

### Debug Mode:
For local development, you can still use:
```bash
python main.py
```

## Next Steps After Deployment

1. **Set up custom domain** (optional)
2. **Configure SSL/HTTPS** (automatic on Render)
3. **Set up monitoring** and logging
4. **Configure backups** for database
5. **Set up CI/CD** for automatic deployments
