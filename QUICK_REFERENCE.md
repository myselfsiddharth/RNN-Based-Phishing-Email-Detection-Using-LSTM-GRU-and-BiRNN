# Quick Reference Guide

Essential commands and information for the Phishing Detection System.

---

## 🚀 Quick Start Commands

### First Time Setup
```bash
# Frontend
cd frontend
npm install

# Backend (new terminal)
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

### Running the Application
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 or http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

---

## 📁 Project Structure at a Glance

```
CSE543/
├── frontend/          # React app
│   └── src/
│       ├── components/   # UI components
│       ├── pages/        # Page components
│       └── services/     # API calls
│
├── backend/           # FastAPI server
│   └── app/
│       ├── routes/       # API endpoints
│       ├── services/     # Business logic
│       └── models/       # Data models
│
├── ml/                # ML models
│   ├── models/          # Model architectures
│   ├── preprocessing/   # Data processing
│   └── train.py         # Training script
│
└── docs/              # Documentation
```

---

## 🔧 Common Tasks

### Add a New Frontend Component
```bash
# Create new file
frontend/src/components/MyComponent.jsx

# Import in parent component
import MyComponent from './components/MyComponent';
```

### Add a New API Endpoint
```bash
# Edit or create in
backend/app/routes/my_route.py

# Register in
backend/app/main.py
```

### Modify Styling
```bash
# Edit
frontend/src/styles.css
```

### Test API Endpoint
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{"post_text": "test", "url": "http://example.com"}'
```

---

## 🐛 Troubleshooting Quick Fixes

### Port Already in Use
```bash
# Backend - use different port
python -m uvicorn app.main:app --reload --port 8001

# Frontend - edit vite.config.js
# Change port: 3000 to port: 3001
```

### Dependencies Not Found
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd backend
pip install -r requirements.txt --upgrade
```

### CORS Errors
Check `backend/app/main.py` - ensure frontend URL is in `allow_origins`

### Module Import Errors
```bash
# Backend - make sure you're in the right directory
cd backend
python -m uvicorn app.main:app --reload
```

---

## 📦 Package Management

### Frontend
```bash
cd frontend
npm install <package>          # Add package
npm install                    # Install all
npm update                     # Update packages
npm run dev                    # Dev server
npm run build                  # Production build
```

### Backend
```bash
cd backend
pip install <package>          # Add package
pip install -r requirements.txt  # Install all
pip freeze > requirements.txt  # Update requirements
```

---

## 🧪 API Testing Examples

### Using curl

#### Detection Endpoint
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "post_text": "Click here for free prizes!",
    "url": "http://suspicious-site.com"
  }'
```

#### Health Check
```bash
curl http://localhost:8000/health
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/detect",
    json={
        "post_text": "Check this out!",
        "url": "http://example.com"
    }
)
print(response.json())
```

### Using JavaScript/Fetch
```javascript
fetch('http://localhost:8000/detect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    post_text: 'Amazing deal!',
    url: 'http://example.com'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📝 File Locations

### Frequently Edited Files

| What | Where |
|------|-------|
| Add new React component | `frontend/src/components/` |
| Modify API endpoint | `backend/app/routes/detect.py` |
| Change styling | `frontend/src/styles.css` |
| Update mock responses | `backend/app/services/url_analysis.py` |
| API data models | `backend/app/models/response_models.py` |
| ML model architecture | `ml/models/` |
| Preprocessing logic | `ml/preprocessing/text_processing.py` |

---

## 🎨 UI Customization

### Colors (in `styles.css`)
```css
:root {
  --primary-color: #2563eb;      /* Blue - main actions */
  --danger-color: #dc2626;       /* Red - high risk */
  --warning-color: #f59e0b;      /* Orange - medium risk */
  --success-color: #16a34a;      /* Green - low risk */
  --bg-color: #f8fafc;          /* Background */
  --card-bg: #ffffff;           /* Cards */
}
```

### Typography
```css
/* Header title */
.title { font-size: 2.5rem; }

/* Subtitle */
.subtitle { font-size: 1.25rem; }

/* Body text */
body { font-size: 16px; }
```

---

## 🔐 Environment Variables

### Backend `.env` (optional)
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend `.env` (optional)
```env
VITE_API_URL=http://localhost:8000
```

---

## 📊 Project Status

### ✅ Working Now
- Frontend UI
- Backend API
- Mock detection
- CORS configuration
- API documentation

### ⏳ Needs Implementation
- CNN model
- LSTM model
- Transformer model
- Preprocessing pipeline
- Training scripts
- Real detection logic

---

## 🎯 Implementation Priority

1. **High**: Collect datasets
2. **High**: Implement preprocessing
3. **High**: Implement one model (start with CNN)
4. **Medium**: Train and evaluate
5. **Medium**: Integrate with backend
6. **Low**: Add advanced features

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `SETUP.md` | Setup instructions |
| `PROJECT_SUMMARY.md` | What's been created |
| `QUICK_REFERENCE.md` | This file - quick tips |
| `docs/architecture.md` | System architecture |
| `ml/README.md` | ML documentation |

---

## 🆘 Need Help?

1. **Setup Issues**: Check `SETUP.md`
2. **Architecture Questions**: Check `docs/architecture.md`
3. **API Questions**: Go to http://localhost:8000/docs
4. **Code Questions**: Check inline comments (look for TODO)
5. **ML Questions**: Check `ml/README.md`

---

## 💡 Pro Tips

- Use the Swagger UI at `/docs` for API testing
- Frontend hot-reloads automatically
- Backend reloads with `--reload` flag
- Check browser console for frontend errors
- Check terminal for backend errors
- Use TODO comments as implementation guide
- Start with one model, then add others
- Mock data helps test UI without ML

---

## 🚦 Workflow

### For UI Changes
1. Edit component in `frontend/src/components/`
2. Save file (auto-reload)
3. Check browser

### For Backend Changes
1. Edit file in `backend/app/`
2. Save file (auto-reload)
3. Test in `/docs` or frontend

### For ML Implementation
1. Edit model in `ml/models/`
2. Implement training in `ml/train.py`
3. Test model separately
4. Integrate with backend

---

## 🎓 For Research

### Collect Data
```
datasets/
├── train/
│   ├── phishing_urls.csv
│   └── legitimate_urls.csv
├── val/
└── test/
```

### Train Model
```bash
cd ml
python train.py --model cnn --data ../datasets --epochs 10
```

### Evaluate
```bash
python train.py --model cnn --evaluate
```

---

**Quick Access**: Bookmark this file for easy reference!

**Remember**: This is a research prototype - focus on the ML implementation for your CSE543 project.

