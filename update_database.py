#!/usr/bin/env python3
"""
Database Update Script
This script updates the existing database schema to match the current models.
Run this before deploying to production.
"""

import os
import sqlite3
from pathlib import Path

def update_database():
    """Update the existing database schema"""
    
    # Path to your database
    db_path = Path("instance/jobportal.db")
    
    if not db_path.exists():
        print("Database file not found. Creating new database...")
        return
    
    print("Updating existing database schema...")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if new columns exist in job_seeker table
        cursor.execute("PRAGMA table_info(job_seeker)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns to job_seeker table
        if 'profile_picture' not in columns:
            print("Adding profile_picture column to job_seeker table...")
            cursor.execute("ALTER TABLE job_seeker ADD COLUMN profile_picture VARCHAR(300)")
        
        if 'bio' not in columns:
            print("Adding bio column to job_seeker table...")
            cursor.execute("ALTER TABLE job_seeker ADD COLUMN bio TEXT")
        
        # Check if new columns exist in recruiter table
        cursor.execute("PRAGMA table_info(recruiter)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns to recruiter table
        if 'profile_picture' not in columns:
            print("Adding profile_picture column to recruiter table...")
            cursor.execute("ALTER TABLE recruiter ADD COLUMN profile_picture VARCHAR(300)")
        
        if 'bio' not in columns:
            print("Adding bio column to recruiter table...")
            cursor.execute("ALTER TABLE recruiter ADD COLUMN bio TEXT")
        
        # Check if experience table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experience'")
        if not cursor.fetchone():
            print("Creating experience table...")
            cursor.execute("""
                CREATE TABLE experience (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    company VARCHAR(200) NOT NULL,
                    start_year VARCHAR(10),
                    end_year VARCHAR(10),
                    description TEXT,
                    jobseeker_id INTEGER,
                    recruiter_id INTEGER,
                    FOREIGN KEY (jobseeker_id) REFERENCES job_seeker (id),
                    FOREIGN KEY (recruiter_id) REFERENCES recruiter (id)
                )
            """)
        
        # Check if skill table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='skill'")
        if not cursor.fetchone():
            print("Creating skill table...")
            cursor.execute("""
                CREATE TABLE skill (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    endorsements INTEGER DEFAULT 0,
                    jobseeker_id INTEGER,
                    recruiter_id INTEGER,
                    FOREIGN KEY (jobseeker_id) REFERENCES job_seeker (id),
                    FOREIGN KEY (recruiter_id) REFERENCES recruiter (id)
                )
            """)
        
        # Commit changes
        conn.commit()
        print("Database schema updated successfully!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()
