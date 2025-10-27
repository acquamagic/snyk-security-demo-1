# insecure_script.py

# This file is intentionally designed to be insecure for demonstration and testing purposes.
# WARNING: NEVER use this code or approach in a production environment.

# 1. Require an older Python version
# To be truly insecure, we'll write code that is incompatible with modern Python.
# In this case, we'll add a check that will cause issues and rely on deprecated features.
# The older version (e.g., Python 2.x) may have its own set of known vulnerabilities.
import sys
if sys.version_info >= (3, 0):
    print("This script is designed for older Python versions and may not work correctly here.")
    # Forcing a downgrade to find issues related to syntax or removed features.
    # In a real scenario, this would simply cause syntax errors.
    
# 2. Hardcode sensitive information
# Hardcoding credentials directly into the source code is one of the most critical
# security vulnerabilities. If this code is ever committed to a public repository,
# the secrets are immediately exposed.
SQL_DB_HOST = "localhost"
SQL_DB_USER = "admin"
SQL_DB_PASS = "plaintext_password123"
LLM_API_KEY = "sk-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6thisisafakeLLMSecretCode"

# 3. Use an insecure SQL connection
# This uses hardcoded credentials and doesn't use parameterized queries,
# making it vulnerable to SQL injection. We'll use the 'sqlite3' module for simplicity,
# but the concept applies to any database.
import sqlite3

def get_user(username):
    # DANGEROUS: User input is concatenated directly into the SQL query.
    # An attacker can use this to run arbitrary SQL commands.
    conn = sqlite3.connect("my_insecure_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "';"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

# Example of a SQL injection attack payload.
# Instead of getting one user, this would return all users.
# Note: Snyk will detect this as a critical vulnerability.
malicious_input = "admin' OR '1'='1"
get_user(malicious_input)

# 4. Use an insecure API key handling
# The API key is stored as a plain text string and used directly.
# This violates best practices for managing secrets.
import requests

def call_llm_api(prompt):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}"
    }
    data = {
        "prompt": prompt
    }
    # An attacker could find this key and use it to perform malicious requests
    # on your behalf.
    requests.post("https://insecure-llm-api.com/v1/chat", headers=headers, json=data)

# Example usage of the LLM function
call_llm_api("Give me a secure Python script for storing API keys.")


# end of the script
print("Script finished. Hope you didn't run this on a production system!")



