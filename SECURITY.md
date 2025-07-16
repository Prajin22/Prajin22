# Security Implementation

## Data Encryption

This job portal application implements comprehensive data encryption to protect sensitive user information.

### Encrypted Fields

**Job Seeker Data:**
- Phone number
- Gender
- Age

**Recruiter Data:**
- Business PAN card
- Company address

### Encryption Implementation

The application uses the `cryptography` library with Fernet symmetric encryption:

- **Algorithm**: Fernet (AES-128 in CBC mode with PKCS7 padding)
- **Key Management**: Environment variable `ENCRYPTION_KEY` or auto-generated
- **Data Format**: Base64 encoded encrypted strings

### Security Features

1. **Automatic Encryption**: All sensitive data is automatically encrypted before database storage
2. **Automatic Decryption**: Data is automatically decrypted when retrieved for display
3. **Migration Support**: Existing data can be encrypted using the migration script
4. **Key Management**: Encryption keys can be managed via environment variables

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Encryption Key** (Optional):
   ```bash
   export ENCRYPTION_KEY="your-32-byte-base64-encoded-key"
   ```

3. **Run Migration** (if you have existing data):
   ```bash
   python migrate_encryption.py
   ```

### Security Best Practices

1. **Environment Variables**: Store encryption keys in environment variables, not in code
2. **Key Rotation**: Regularly rotate encryption keys
3. **Backup**: Always backup encryption keys securely
4. **Access Control**: Limit database access to authorized personnel only
5. **HTTPS**: Use HTTPS in production to encrypt data in transit

### Database Schema Changes

The database schema has been updated to accommodate encrypted data:

- Phone field: `VARCHAR(20)` → `VARCHAR(500)`
- Gender field: `VARCHAR(20)` → `VARCHAR(500)`
- Age field: `INTEGER` → `VARCHAR(500)`
- Business PAN: `VARCHAR(50)` → `VARCHAR(500)`
- Company Address: `VARCHAR(200)` → `VARCHAR(500)`

### Migration Process

The migration script (`migrate_encryption.py`) handles:

1. **Detection**: Identifies unencrypted sensitive data
2. **Encryption**: Encrypts data using the current encryption key
3. **Verification**: Confirms all data is properly encrypted
4. **Rollback**: Can be run multiple times safely

### API Security

- All sensitive data is encrypted before database storage
- Data is automatically decrypted when retrieved for API responses
- No sensitive data is logged or exposed in error messages

### Compliance

This implementation helps meet data protection requirements:

- **GDPR**: Protects personal data with encryption
- **PCI DSS**: Encrypts sensitive business information
- **Industry Standards**: Follows encryption best practices

### Monitoring

The application includes logging for encryption operations:

- Successful encryption/decryption operations
- Failed encryption attempts
- Migration progress and results

### Emergency Procedures

**If encryption key is lost:**
1. Restore from secure backup
2. Re-run migration script
3. Verify data integrity

**If data corruption occurs:**
1. Restore from database backup
2. Verify encryption key
3. Re-run migration if needed 