#!/usr/bin/env python3
"""
Database Migration Script for Data Encryption
This script encrypts existing user data in the database.
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from encryption_utils import encrypt_field, decrypt_field

# Create Flask app for migration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobportal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
class JobSeeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(500), nullable=False)
    gender = db.Column(db.String(500), nullable=False)
    age = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    business_pancard = db.Column(db.String(500))
    company_name = db.Column(db.String(120))
    company_address = db.Column(db.String(500))
    password = db.Column(db.String(200), nullable=False)

def is_encrypted(data):
    """Check if data is already encrypted"""
    if not data:
        return False
    try:
        # Try to decrypt - if it fails, it's not encrypted
        decrypt_field(data)
        return True
    except:
        return False

def migrate_jobseekers():
    """Migrate existing job seeker data to encrypted format"""
    print("Migrating JobSeeker data...")
    
    jobseekers = JobSeeker.query.all()
    migrated_count = 0
    
    for jobseeker in jobseekers:
        updated = False
        
        # Check and encrypt phone
        if jobseeker.phone and not is_encrypted(jobseeker.phone):
            jobseeker.phone = encrypt_field(jobseeker.phone)
            updated = True
            print(f"Encrypted phone for {jobseeker.email}")
        
        # Check and encrypt gender
        if jobseeker.gender and not is_encrypted(jobseeker.gender):
            jobseeker.gender = encrypt_field(jobseeker.gender)
            updated = True
            print(f"Encrypted gender for {jobseeker.email}")
        
        # Check and encrypt age
        if jobseeker.age and not is_encrypted(jobseeker.age):
            jobseeker.age = encrypt_field(str(jobseeker.age))
            updated = True
            print(f"Encrypted age for {jobseeker.email}")
        
        if updated:
            migrated_count += 1
    
    if migrated_count > 0:
        db.session.commit()
        print(f"Successfully migrated {migrated_count} job seekers")
    else:
        print("No job seekers needed migration")

def migrate_recruiters():
    """Migrate existing recruiter data to encrypted format"""
    print("Migrating Recruiter data...")
    
    recruiters = Recruiter.query.all()
    migrated_count = 0
    
    for recruiter in recruiters:
        updated = False
        
        # Check and encrypt business pancard
        if recruiter.business_pancard and not is_encrypted(recruiter.business_pancard):
            recruiter.business_pancard = encrypt_field(recruiter.business_pancard)
            updated = True
            print(f"Encrypted business pancard for {recruiter.email}")
        
        # Check and encrypt company address
        if recruiter.company_address and not is_encrypted(recruiter.company_address):
            recruiter.company_address = encrypt_field(recruiter.company_address)
            updated = True
            print(f"Encrypted company address for {recruiter.email}")
        
        if updated:
            migrated_count += 1
    
    if migrated_count > 0:
        db.session.commit()
        print(f"Successfully migrated {migrated_count} recruiters")
    else:
        print("No recruiters needed migration")

def verify_encryption():
    """Verify that data is properly encrypted"""
    print("Verifying encryption...")
    
    # Check job seekers
    jobseekers = JobSeeker.query.all()
    for jobseeker in jobseekers:
        if jobseeker.phone and not is_encrypted(jobseeker.phone):
            print(f"WARNING: Phone not encrypted for {jobseeker.email}")
        if jobseeker.gender and not is_encrypted(jobseeker.gender):
            print(f"WARNING: Gender not encrypted for {jobseeker.email}")
        if jobseeker.age and not is_encrypted(jobseeker.age):
            print(f"WARNING: Age not encrypted for {jobseeker.email}")
    
    # Check recruiters
    recruiters = Recruiter.query.all()
    for recruiter in recruiters:
        if recruiter.business_pancard and not is_encrypted(recruiter.business_pancard):
            print(f"WARNING: Business pancard not encrypted for {recruiter.email}")
        if recruiter.company_address and not is_encrypted(recruiter.company_address):
            print(f"WARNING: Company address not encrypted for {recruiter.email}")
    
    print("Encryption verification complete")

def main():
    """Main migration function"""
    print("Starting data encryption migration...")
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Migrate existing data
        migrate_jobseekers()
        migrate_recruiters()
        
        # Verify encryption
        verify_encryption()
        
        print("Migration completed successfully!")

if __name__ == "__main__":
    main() 