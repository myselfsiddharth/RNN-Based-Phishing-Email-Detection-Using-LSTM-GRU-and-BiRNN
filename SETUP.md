# Quick Setup Guide

This guide will help you get the phishing detection system up and running quickly.

## Prerequisites

- Node.js (v16 or higher)
- Python (3.9 or higher)
- npm or yarn
- pip

## Quick Start

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Install Backend Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Backend

```bash
# From backend directory with venv activated
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### 4. Run the Frontend

Open a NEW terminal window:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 5. Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:5173 (or http://localhost:3000)
- **Backend API Docs**: http://localhost:8000/docs

## Troubleshooting

### Port Already in Use

If port 8000 or 5173 is already in use:

**Backend:**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**Frontend (edit `vite.config.js`):**
```javascript
server: {
  port: 3001,
  // ...
}
```

### Module Not Found Errors

**Backend:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules
npm install
```

### CORS Errors

If you see CORS errors, make sure:
1. Backend is running on port 8000
2. Frontend is accessing the correct backend URL
3. Check `backend/app/main.py` CORS settings

### Virtual Environment Issues

**Windows:**
```bash
# If activation fails, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Make sure you're in the backend directory
cd backend
source venv/bin/activate
```

## Testing the Application

1. Open the frontend in your browser
2. Enter a sample URL: `http://suspicious-site.com`
3. Click "Analyze Post"
4. You should see a mock detection result

**Note:** Current implementation returns mock/random results since ML models are not yet implemented.

## API Testing with curl

```bash
# Test the detection endpoint
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "post_text": "Check out this deal!",
    "url": "http://example.com"
  }'
```

## API Testing with Postman

1. Create a new POST request
2. URL: `http://localhost:8000/detect`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "post_text": "Check out this amazing offer!",
  "url": "http://test-phishing.com"
}
```
5. Click Send

## Next Steps

### For Development

1. **Modify Frontend Components**: Edit files in `frontend/src/components/`
2. **Modify Backend Logic**: Edit files in `backend/app/`
3. **Add ML Models**: Implement models in `ml/models/`

### For Research

1. **Collect Datasets**: Add phishing/legitimate URLs to `datasets/`
2. **Implement ML Models**: Complete the placeholder models
3. **Train Models**: Use `ml/train.py` script
4. **Integrate Models**: Connect trained models to backend

## Development Workflow

### Frontend Changes

1. Make changes to React components
2. Vite will auto-reload the browser
3. Check console for errors

### Backend Changes

1. Make changes to Python files
2. Uvicorn will auto-reload with `--reload` flag
3. Check terminal for errors

### Full Stack Testing

1. Ensure both frontend and backend are running
2. Test API endpoints via frontend UI
3. Check browser console and network tab
4. Check backend terminal for request logs

## Project Structure Quick Reference

```
Frontend: frontend/src/
  - components/  → React components
  - pages/       → Page components
  - services/    → API calls
  - styles.css   → Global styles

Backend: backend/app/
  - main.py      → Application entry
  - routes/      → API endpoints
  - services/    → Business logic
  - models/      → Data models

ML: ml/
  - models/      → Model architectures
  - preprocessing/ → Data processing
  - train.py     → Training script
```

## Common Commands

```bash
# Frontend
cd frontend
npm install          # Install dependencies
npm run dev          # Start dev server
npm run build        # Build for production

# Backend
cd backend
pip install -r requirements.txt  # Install dependencies
python -m uvicorn app.main:app --reload  # Start dev server
python -m pytest     # Run tests (when implemented)

# ML
cd ml
python train.py --model cnn  # Train CNN model (when implemented)
```

## Environment Variables

### Backend (optional)

Create `backend/.env`:
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Frontend (optional)

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## Getting Help

- Check `README.md` for comprehensive documentation
- Check `docs/architecture.md` for system design
- Check code comments for implementation details
- Look for `TODO` comments for areas needing implementation

## Ready to Start!

You're all set! The system should now be running with:
- ✅ Frontend UI accessible in browser
- ✅ Backend API running and responding
- ✅ Mock detection working

**Remember:** This is a research prototype scaffold. The ML models need to be implemented for real phishing detection.

