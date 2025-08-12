# 🔥 Firebase Setup Guide for LinkedIn Job Portal

## 🎯 **What We're Building:**
- **Shared Database** between web and mobile apps
- **Real-time synchronization** across platforms
- **User Authentication** that works everywhere
- **Free tier** perfect for college students

## 🚀 **Step 1: Create Firebase Project (FREE)**

### 1. Go to [Firebase Console](https://console.firebase.google.com/)
### 2. Click "Create a project"
### 3. Enter project name: `linkedin-job-portal`
### 4. Choose whether to enable Google Analytics (optional)
### 5. Click "Create project"

## 🔧 **Step 2: Enable Services**

### **Firestore Database (Main Database)**
1. In Firebase Console, click "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (we'll secure it later)
4. Select a location close to your users
5. Click "Done"

### **Authentication (User Login)**
1. Click "Authentication" in sidebar
2. Click "Get started"
3. Click "Sign-in method" tab
4. Enable "Email/Password"
5. Click "Save"

### **Storage (Profile Pictures)**
1. Click "Storage" in sidebar
2. Click "Get started"
3. Choose "Start in test mode"
4. Select same location as Firestore
5. Click "Done"

## 📱 **Step 3: Add Your Apps**

### **Web App (React)**
1. Click the web icon (</>) on project overview
2. Enter app nickname: `linkedin-job-portal-web`
3. Click "Register app"
4. Copy the config object (we'll use this)

### **Mobile App (Android/iOS)**
1. Click the mobile icon (📱) on project overview
2. Choose your platform (Android/iOS)
3. Enter app nickname: `linkedin-job-portal-mobile`
4. Follow platform-specific setup

## 🔑 **Step 4: Get Configuration**

### **Web App Config**
Copy this from Firebase Console and update `firebase_config.js`:

```javascript
const firebaseConfig = {
  apiKey: "your-actual-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-actual-app-id"
};
```

### **Service Account Key (For Flask Backend)**
1. Go to Project Settings (gear icon)
2. Click "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file
5. Save as `serviceAccountKey.json` in your project root

## 📦 **Step 5: Install Dependencies**

### **React App (Frontend)**
```bash
cd my-gsap-app
npm install firebase
```

### **Flask App (Backend)**
```bash
pip install firebase-admin
```

## 🗄️ **Step 6: Database Structure**

### **Collections in Firestore:**

#### **Users Collection**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "jobseeker", // or "recruiter"
  "created_at": "2024-01-01T00:00:00Z",
  "last_updated": "2024-01-01T00:00:00Z",
  
  // Job Seeker specific fields
  "phone": "+1234567890",
  "gender": "male",
  "age": "25",
  "profile_picture": "url_to_image",
  "bio": "Software developer...",
  "skills": ["Python", "React", "Flask"],
  "experiences": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "start_year": "2022",
      "end_year": "2024",
      "description": "Developed web applications..."
    }
  ],
  
  // Recruiter specific fields
  "company_name": "Tech Corp",
  "business_pancard": "ABCDE1234F",
  "company_address": "123 Tech Street...",
  "posted_jobs": ["job_id_1", "job_id_2"]
}
```

#### **Jobs Collection**
```json
{
  "id": "auto_generated_id",
  "title": "Software Engineer",
  "company_name": "Tech Corp",
  "location": "New York, NY",
  "salary_min": 80000,
  "salary_max": 120000,
  "job_type": "Full-time",
  "description": "We are looking for...",
  "requirements": "5+ years experience...",
  "skills": ["Python", "React", "Flask"],
  "posted_date": "2024-01-01T00:00:00Z",
  "recruiter_id": "recruiter_email",
  "is_active": true,
  "applications": [
    {
      "applicant_id": "user_email",
      "applied_date": "2024-01-01T00:00:00Z",
      "status": "pending"
    }
  ]
}
```

## 🔒 **Step 7: Security Rules**

### **Firestore Security Rules**
Go to Firestore Database → Rules and update:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.token.email == userId;
    }
    
    // Anyone can read active jobs
    match /jobs/{jobId} {
      allow read: if resource.data.is_active == true;
      allow write: if request.auth != null && 
        request.auth.token.email == resource.data.recruiter_id;
    }
    
    // Users can apply to jobs
    match /jobs/{jobId} {
      allow update: if request.auth != null && 
        request.auth.token.email in resource.data.applications[].applicant_id;
    }
  }
}
```

### **Storage Security Rules**
Go to Storage → Rules and update:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Users can upload their own profile pictures
    match /profile_pictures/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && 
        request.auth.token.email == userId;
    }
  }
}
```

## 🚀 **Step 8: Integration**

### **Update Flask Backend**
1. Copy `firebase_integration.py` to your project
2. Update `main.py` to use Firebase functions
3. Set environment variable: `GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json`

### **Update React Frontend**
1. Copy `firebase_config.js` to your React app
2. Update the config with your actual Firebase values
3. Import and use Firebase services in your components

## 💰 **Free Tier Limits (Perfect for College Projects!)**

### **Firestore Database**
- **Storage**: 1GB
- **Reads**: 50,000/day
- **Writes**: 20,000/day
- **Deletes**: 20,000/day

### **Authentication**
- **Users**: Unlimited
- **Phone Auth**: 10,000/month

### **Storage**
- **Storage**: 5GB
- **Download**: 1GB/day
- **Upload**: 20GB/day

### **Hosting**
- **Storage**: 10GB
- **Transfer**: 360MB/day

## 🎯 **Benefits for Your Project:**

1. **Real-time Updates**: Changes sync instantly between web and mobile
2. **Offline Support**: Mobile app works without internet
3. **Scalable**: Grows with your project
4. **Free**: No cost for development and small projects
5. **Professional**: Industry-standard solution
6. **Easy Integration**: Works with React, Flutter, React Native, etc.

## 🔍 **Testing Your Setup**

### **Test Firestore**
1. Go to Firestore Database in Firebase Console
2. Add a test document manually
3. Check if your app can read/write

### **Test Authentication**
1. Try creating a user account
2. Check if user appears in Authentication section
3. Verify user data is in Firestore

### **Test Real-time Updates**
1. Update data in one app
2. Check if it appears in the other app
3. Verify timestamps are updated

## 🆘 **Common Issues & Solutions**

### **"Firebase not initialized"**
- Check if `firebase_config.js` has correct values
- Ensure Firebase services are enabled

### **"Permission denied"**
- Check Firestore security rules
- Verify user is authenticated

### **"Service account not found"**
- Download service account key again
- Check file path in environment variables

## 🎉 **Next Steps After Setup:**

1. **Test basic CRUD operations**
2. **Implement real-time listeners**
3. **Add offline persistence**
4. **Set up push notifications**
5. **Deploy to production**

---

## 🚀 **Ready to Get Started?**

1. **Create Firebase project** (5 minutes)
2. **Enable services** (5 minutes)
3. **Get configuration** (2 minutes)
4. **Install dependencies** (2 minutes)
5. **Test integration** (10 minutes)

**Total time: ~25 minutes for a fully functional shared database!** 🎯
