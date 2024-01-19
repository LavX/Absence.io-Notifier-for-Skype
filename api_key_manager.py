import sqlite3
import secrets
import argparse
from functools import wraps
from flask import request, jsonify

# Database initialization
def init_db():
    conn = sqlite3.connect('api_keys.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            active INTEGER NOT NULL CHECK (active IN (0,1))
        )
    ''')
    conn.commit()
    conn.close()

# Generate a new API key
def generate_api_key():
    return secrets.token_urlsafe(32)

# Add an API key
def add_api_key():
    key = generate_api_key()
    conn = sqlite3.connect('api_keys.db')
    c = conn.cursor()
    c.execute('INSERT INTO api_keys (key, active) VALUES (?, ?)', (key, 1))
    conn.commit()
    conn.close()
    return key

# Remove (deactivate) an API key
def remove_api_key(key):
    conn = sqlite3.connect('api_keys.db')
    c = conn.cursor()
    c.execute('UPDATE api_keys SET active = 0 WHERE key = ?', (key,))
    conn.commit()
    conn.close()

# Check if an API key is valid and active
def is_valid_key(key):
    conn = sqlite3.connect('api_keys.db')
    c = conn.cursor()
    c.execute('SELECT active FROM api_keys WHERE key = ? AND active = 1', (key,))
    result = c.fetchone()
    conn.close()
    return result is not None

#Decorator for API protection
def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key and is_valid_key(api_key):
            return view_function(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid or missing API key"}), 401
    return decorated_function

# CLI
def main():
    parser = argparse.ArgumentParser(description='API Key Manager')
    parser.add_argument('--add', action='store_true', help='Add a new API key')
    parser.add_argument('--remove', type=str, help='Remove (deactivate) an API key')
    parser.add_argument('--check', type=str, help='Check if an API key is valid and active')

    args = parser.parse_args()

    if args.add:
        key = add_api_key()
        print(f'New API key added: {key}')
    elif args.remove:
        remove_api_key(args.remove)
        print(f'API key removed: {args.remove}')
    elif args.check:
        is_valid = is_valid_key(args.check)
        print(f'API key is {"valid" if is_valid else "invalid"}: {args.check}')

if __name__ == '__main__':
    init_db()
    main()