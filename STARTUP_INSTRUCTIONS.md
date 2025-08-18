# 🚀 Real Estate Application Startup Guide

## Quick Start Options

### Option 1: One-Click Startup (Recommended)
**Double-click** `start_all.bat` or `start_all.ps1` to start both servers automatically.

### Option 2: Individual Server Startup
- **Backend only**: Double-click `start_backend.bat`
- **Frontend only**: Double-click `start_frontend.bat`

### Option 3: Manual Startup
```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
python -m http.server 3000
```

## 🌐 Access URLs

- **Main Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ⚠️ Troubleshooting

### If servers don't start:
1. Make sure Python is installed and in PATH
2. Install requirements: `pip install -r requirements.txt`
3. Check if ports 8000 and 3000 are free
4. Run as Administrator if needed

### If you get NumPy warnings:
- These are compatibility warnings but don't prevent the app from running
- The application will work normally despite these warnings

### If you get database errors:
- Make sure PostgreSQL is running
- Check your `.env` file configuration
- Run database setup scripts if needed

## 🔧 Server Management

- **Keep server windows open** while using the application
- **Close server windows** to stop the servers
- **Restart servers** by running the startup scripts again

## 📱 Features Available

- AI-powered natural language property search
- Property filtering and browsing
- Interactive chat interface
- RESTful API endpoints
- Real-time search results

## 🆘 Need Help?

If you encounter issues:
1. Check the server console windows for error messages
2. Verify both servers are running on correct ports
3. Check browser console for frontend errors
4. Ensure all dependencies are installed

---
**Happy Real Estate Searching! 🏠✨**
