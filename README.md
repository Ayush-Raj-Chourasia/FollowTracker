# FollowTracker
A modern Python application built with Flask to analyze your Instagram social connections. Compare followers and following data to discover who unfollowed you, who's your true fan, and your mutual connections.


![Instagram Analytics Tool Screenshot](image.png)


## Features
- 🔍 Compare followers and following data
- 📊 Identify fans, snakes, and mutual connections
- 🌙 Dark/Light mode support
- 📱 Mobile-friendly interface
- 🔒 Privacy-focused (data processed locally)
- 📤 Export data to Excel/CSV
- 🔎 Search and filter capabilities

## How to Use

### Step 1: Get Your Instagram Data
1. Go to your Instagram profile
2. Click the 3 lines (menu) at the top right corner
3. Select 'Your Activity' (clock icon)
4. Scroll down and tap 'Download your information'
5. Confirm your email and wait for the data (4-6 hours)

### Step 2: Prepare Your Files
1. Check your email for "Your Instagram Information"
2. Download and extract the ZIP file
3. Navigate to the 'followers_and_following' folder
4. Locate `followers.html` and `following.html`

### Step 3: Use FollowTracker
1. Upload both HTML files
2. Click submit to analyze your connections
3. View results in three categories:
   - Fans (people who follow you but you don't follow back)
   - Snakes (people you follow but don't follow you back)
   - Mutuals (people you follow and follow you back)

## User Guide

### 1. Upload Your Instagram Data
- Go to the main page
- Upload your `followers.html` and `following.html` files
- Click the upload button

### 2. View Results
- See three tabs: **Fans**, **Snakes**, and **Mutuals**
- Each tab lists accounts with username, follow date, and quick links
- Use the search box and sort dropdown to filter and sort results

### 3. Dark Mode
- Click the 🌙 Dark Mode button in the top right to toggle dark/light themes

### 4. Export & Bulk Actions
- Export all data to Excel (.xlsx)
- Copy selected usernames
- Export selected usernames to CSV
- Select multiple accounts using checkboxes

### 5. Privacy & Security
- Your data is processed in your browser
- Uploaded files are deleted immediately after processing
- No data is stored on the server

### 6. Error Handling
- Clear error messages for invalid files
- User-friendly notifications

### 7. Mobile Friendly
- Responsive design for all devices
- Optimized for both desktop and mobile

## Deployment
This application is deployed on Vercel/Netlify for optimal performance and reliability.

## License
MIT License - Feel free to use and modify this project for your needs.

---





