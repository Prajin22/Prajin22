"""
Firebase Integration for Flask Backend
This allows your Flask app to sync with Firebase for mobile app integration
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import json

class FirebaseManager:
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Initialize with service account key
                # You'll need to download this from Firebase Console
                cred = credentials.Certificate("path/to/serviceAccountKey.json")
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("✅ Firebase Admin SDK initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            self.db = None
    
    def sync_user_to_firebase(self, user_data, user_type):
        """Sync user data from Flask to Firebase"""
        if not self.db:
            print("❌ Firebase not initialized")
            return False
        
        try:
            # Create user document in Firestore
            user_ref = self.db.collection('users').document(user_data['email'])
            
            # Prepare data for Firebase
            firebase_user_data = {
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'user_type': user_type,
                'created_at': datetime.now(),
                'last_updated': datetime.now()
            }
            
            # Add type-specific fields
            if user_type == 'jobseeker':
                firebase_user_data.update({
                    'phone': user_data.get('phone', ''),
                    'gender': user_data.get('gender', ''),
                    'age': user_data.get('age', ''),
                    'profile_picture': user_data.get('profile_picture', ''),
                    'bio': user_data.get('bio', ''),
                    'skills': [],
                    'experiences': []
                })
            elif user_type == 'recruiter':
                firebase_user_data.update({
                    'company_name': user_data.get('company_name', ''),
                    'business_pancard': user_data.get('business_pancard', ''),
                    'company_address': user_data.get('company_address', ''),
                    'profile_picture': user_data.get('profile_picture', ''),
                    'bio': user_data.get('bio', ''),
                    'posted_jobs': []
                })
            
            # Save to Firestore
            user_ref.set(firebase_user_data)
            print(f"✅ User {user_data['email']} synced to Firebase")
            return True
            
        except Exception as e:
            print(f"❌ Failed to sync user to Firebase: {e}")
            return False
    
    def sync_job_to_firebase(self, job_data):
        """Sync job posting to Firebase"""
        if not self.db:
            print("❌ Firebase not initialized")
            return False
        
        try:
            # Create job document in Firestore
            job_ref = self.db.collection('jobs').document()
            
            firebase_job_data = {
                'id': job_ref.id,
                'title': job_data['title'],
                'company_name': job_data['company_name'],
                'location': job_data.get('location', ''),
                'salary_min': job_data.get('salary_min', 0),
                'salary_max': job_data.get('salary_max', 0),
                'job_type': job_data.get('job_type', ''),
                'description': job_data['description'],
                'requirements': job_data.get('requirements', ''),
                'skills': job_data.get('skills', ''),
                'posted_date': datetime.now(),
                'recruiter_id': job_data['recruiter_id'],
                'is_active': True,
                'applications': []
            }
            
            # Save to Firestore
            job_ref.set(firebase_job_data)
            print(f"✅ Job '{job_data['title']}' synced to Firebase")
            return True
            
        except Exception as e:
            print(f"❌ Failed to sync job to Firebase: {e}")
            return False
    
    def get_user_from_firebase(self, email):
        """Get user data from Firebase"""
        if not self.db:
            print("❌ Firebase not initialized")
            return None
        
        try:
            user_ref = self.db.collection('users').document(email)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                return user_doc.to_dict()
            else:
                print(f"❌ User {email} not found in Firebase")
                return None
                
        except Exception as e:
            print(f"❌ Failed to get user from Firebase: {e}")
            return None
    
    def update_user_in_firebase(self, email, updates):
        """Update user data in Firebase"""
        if not self.db:
            print("❌ Firebase not initialized")
            return False
        
        try:
            user_ref = self.db.collection('users').document(email)
            
            # Add timestamp
            updates['last_updated'] = datetime.now()
            
            # Update in Firestore
            user_ref.update(updates)
            print(f"✅ User {email} updated in Firebase")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update user in Firebase: {e}")
            return False

# Global Firebase manager instance
firebase_manager = FirebaseManager()

# Helper functions for easy integration
def sync_user_to_firebase(user_data, user_type):
    """Helper function to sync user to Firebase"""
    return firebase_manager.sync_user_to_firebase(user_data, user_type)

def sync_job_to_firebase(job_data):
    """Helper function to sync job to Firebase"""
    return firebase_manager.sync_job_to_firebase(job_data)

def get_user_from_firebase(email):
    """Helper function to get user from Firebase"""
    return firebase_manager.get_user_from_firebase(email)

def update_user_in_firebase(email, updates):
    """Helper function to update user in Firebase"""
    return firebase_manager.update_user_in_firebase(email, updates)
