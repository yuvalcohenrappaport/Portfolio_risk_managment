import subprocess
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def run_python_file(file_path):
    """
    Run a Python file and capture its output and errors.
    """
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'success': result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': 'Script execution timeout (5 minutes)',
            'returncode': -1,
            'success': False
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
            'success': False
        }

def send_email(results, file_path, recipient_email, sender_email, sender_password):
    """
    Send execution results via email with PNG attachment if available.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Portfolio Risk Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Create email body
    status = "✓ Success" if results['success'] else "✗ Failed"
    body = f"""
Python Script Execution Report
{'=' * 50}

File: {file_path}
Status: {status}
Return Code: {results['returncode']}
Executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 50}
OUTPUT:
{'=' * 50}
{results['stdout'] if results['stdout'] else '(no output)'}

{'=' * 50}
ERRORS:
{'=' * 50}
{results['stderr'] if results['stderr'] else '(no errors)'}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Extract file paths from stdout and attach if they exist (PNG and HTML)
    file_paths = []
    for line in results['stdout'].split('\n'):
        if 'saved to' in line.lower():
            path = line.split('saved to')[-1].strip()
            if path:
                file_paths.append(path)
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
                msg.attach(part)
                print(f"Attached file: {file_path}")
            except Exception as e:
                print(f"Warning: Could not attach file {file_path}: {e}")
    
    # Send email using Gmail SMTP
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    # Configuration
    PYTHON_FILE = 'stock_portfolio_risk.py'  # Path to the Python file you want to run
    RECIPIENT_EMAIL = os.getenv('TRADING_EMAIL_TO')
    SENDER_EMAIL = os.getenv('TRADING_EMAIL_FROM')
    SENDER_PASSWORD = os.getenv('TRADING_EMAIL_PASSWORD')  # Use App Password for Gmail

    if not RECIPIENT_EMAIL or not SENDER_EMAIL or not SENDER_PASSWORD:
        raise RuntimeError(
            "Missing email configuration. Set TRADING_EMAIL_TO, TRADING_EMAIL_FROM, "
            "and TRADING_EMAIL_PASSWORD environment variables."
        )
    
    # Run the Python file
    print(f"Running {PYTHON_FILE}...")
    results = run_python_file(PYTHON_FILE)
    
    # Send results via email
    print("Sending results via email...")
    send_email(results, PYTHON_FILE, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD)

if __name__ == '__main__':
    main()