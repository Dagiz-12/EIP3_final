#!/usr/bin/env python
"""
Setup script to create environment configuration
"""
import os
import secrets
import sys


def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(50)


def setup_environment():
    """Setup environment configuration"""

    print("Setting up EIP Ethiopia environment configuration...")
    print("-" * 50)

    # Check if .env exists
    if os.path.exists('.env'):
        print("❌ .env file already exists!")
        overwrite = input("Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return

    # Collect configuration
    config = {}

    # Django Settings
    config['SECRET_KEY'] = generate_secret_key()
    config['DEBUG'] = input("Enable debug mode? (Y/n): ").lower() or 'True'
    config['ALLOWED_HOSTS'] = input(
        "Allowed hosts (comma-separated, default: localhost,127.0.0.1): ") or 'localhost,127.0.0.1'

    # Database
    print("\nDatabase Configuration:")
    print("1. SQLite (default)")
    print("2. PostgreSQL")
    print("3. MySQL")
    db_choice = input("Choose database (1-3, default 1): ") or '1'

    if db_choice == '2':
        config['DATABASE_URL'] = input(
            "PostgreSQL URL (postgresql://user:pass@localhost/dbname): ")
    elif db_choice == '3':
        config['DATABASE_URL'] = input(
            "MySQL URL (mysql://user:pass@localhost/dbname): ")
    else:
        config['DATABASE_URL'] = 'sqlite:///db.sqlite3'

    # Email
    print("\nEmail Configuration:")
    print("Leave blank to use console backend for development")
    config['EMAIL_HOST'] = input(
        "SMTP Host (default: smtp.gmail.com): ") or 'smtp.gmail.com'
    config['EMAIL_PORT'] = input("SMTP Port (default: 587): ") or '587'
    config['EMAIL_USE_TLS'] = input("Use TLS? (Y/n): ").lower() or 'True'
    config['EMAIL_HOST_USER'] = input("Email username: ") or ''
    config['EMAIL_HOST_PASSWORD'] = input(
        "Email password/app password: ") or ''
    config['DEFAULT_FROM_EMAIL'] = input(
        "Default from email (default: noreply@eipethiopia.org): ") or 'noreply@eipethiopia.org'
    config['ADMIN_EMAIL'] = input(
        "Admin email for notifications: ") or 'admin@eipethiopia.org'

    # Site URL
    config['SITE_URL'] = input(
        "Site URL for email links (default: http://localhost:8000): ") or 'http://localhost:8000'

    # Write .env file
    with open('.env', 'w') as f:
        f.write("# Django Settings\n")
        f.write(f"SECRET_KEY={config['SECRET_KEY']}\n")
        f.write(f"DEBUG={config['DEBUG']}\n")
        f.write(f"ALLOWED_HOSTS={config['ALLOWED_HOSTS']}\n\n")

        f.write("# Database\n")
        f.write(f"DATABASE_URL={config['DATABASE_URL']}\n\n")

        f.write("# Email Configuration\n")
        for key in ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS',
                    'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD',
                    'DEFAULT_FROM_EMAIL', 'ADMIN_EMAIL']:
            f.write(f"{key}={config[key]}\n")

        f.write(f"\n# Site URL\n")
        f.write(f"SITE_URL={config['SITE_URL']}\n")

    print("\n✅ Environment configuration created!")
    print("📁 File: .env")
    print("\n⚠️  Remember to:")
    print("  1. Keep .env file secure (add to .gitignore)")
    print("  2. Update email credentials for production")
    print("  3. Set DEBUG=False in production")


if __name__ == '__main__':
    setup_environment()
