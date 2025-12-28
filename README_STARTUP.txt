================================================
   GOVERNMENT FINANCE PORTAL - STARTUP GUIDE
================================================

METHOD 1: AUTOMATIC START (EASIEST)
====================================
1. Double-click: START_PROJECT.bat
2. Wait for browser to open automatically
3. Login with credentials below

DONE! Both servers start automatically.


METHOD 2: MANUAL START
======================

STEP 1 - Start Backend Server:
-------------------------------
Open Terminal 1 and run these commands:

cd c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\gok_backend
C:\Users\nyaga\OneDrive\Desktop\NASA\.venv\Scripts\activate
python main.py

✓ You should see: "Uvicorn running on http://0.0.0.0:8000"
✓ KEEP THIS WINDOW OPEN!


STEP 2 - Start Frontend Server:
--------------------------------
Open Terminal 2 (NEW terminal) and run:

cd c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\NASA
python -m http.server 5500

✓ You should see: "Serving HTTP on :: port 5500"
✓ KEEP THIS WINDOW OPEN!


STEP 3 - Open Browser:
-----------------------
Go to: http://localhost:5500/login.html


================================================
              LOGIN CREDENTIALS
================================================

Finance Office:
  Username: FinanceOffice
  Password: finance2025

Education Office:
  Username: EducationOffice
  Password: education2025

Healthcare Office:
  Username: HealthcareOffice
  Password: healthcare2025


================================================
            AVAILABLE PAGES
================================================

Login/Dashboard:  http://localhost:5500/login.html
Tax Payment:      http://localhost:5500/tax-payment.html
Citizen Portal:   http://localhost:5500/citizen-portal.html


================================================
          STOPPING THE SERVERS
================================================

In EACH terminal window, press: Ctrl + C

Or simply close the terminal windows.


================================================
           TROUBLESHOOTING
================================================

Problem: "Port already in use" error
Solution: Run these commands to kill processes:

  netstat -ano | findstr :8000
  taskkill /F /PID [number shown]
  
  netstat -ano | findstr :5500
  taskkill /F /PID [number shown]

Then restart the servers.


Problem: 404 Error in browser
Solution: Make sure frontend is running from the NASA folder:
  cd c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\NASA


Problem: Database not found
Solution: Run database initialization:
  cd c:\Users\nyaga\OneDrive\Desktop\NASA\Nasa\gok_backend
  C:\Users\nyaga\OneDrive\Desktop\NASA\.venv\Scripts\python.exe database_init.py


================================================
              NEED HELP?
================================================

Check that:
1. Both terminal windows are open and running
2. No error messages in the terminals
3. You're using the correct URL with /login.html
4. Virtual environment (.venv) exists

================================================
