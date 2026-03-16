import subprocess
import smtplib
import os
import sys
import json
import re

from pathlib import Path
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timezone

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


def _colorize_direction_tags(text):
    """Replace direction tags with color-coded HTML spans."""
    replacements = [
        (r'\[STRONGLY BEARISH\]', '<span style="color:#ef5350;font-weight:bold;">[STRONGLY BEARISH]</span>'),
        (r'\[BEARISH\]', '<span style="color:#ef5350;font-weight:bold;">[BEARISH]</span>'),
        (r'\[STRONGLY BULLISH\]', '<span style="color:#66bb6a;font-weight:bold;">[STRONGLY BULLISH]</span>'),
        (r'\[BULLISH\]', '<span style="color:#66bb6a;font-weight:bold;">[BULLISH]</span>'),
        (r'\[CONFIRMED\]', '<span style="color:#ffa726;font-weight:bold;">[CONFIRMED]</span>'),
        (r'\[DELAYED\]', '<span style="color:#78909c;font-weight:bold;">[DELAYED]</span>'),
        (r'\[CANCELLED\]', '<span style="color:#78909c;font-weight:bold;">[CANCELLED]</span>'),
        (r'\[PRICED-IN\]', '<span style="color:#78909c;font-weight:bold;">[PRICED-IN]</span>'),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def _text_to_html(text):
    """Convert plain text catalyst summary to HTML with formatting."""
    lines = text.split('\n')
    html_lines = []
    for line in lines:
        stripped = line.strip()
        # Section headers with === or --- separators
        if re.match(r'^[=\-]{4,}$', stripped):
            continue  # Skip pure separator lines
        elif re.match(r'^(CHANGES SINCE|CATALYST DETAILS|Generated:)', stripped):
            html_lines.append(f'<h3 style="color:#90a4ae;margin-top:1.2em;margin-bottom:0.3em;">{stripped}</h3>')
        elif re.match(r'^[A-Z]{2,6}$', stripped):
            # All-caps ticker header (2–6 chars)
            html_lines.append(f'<strong style="font-size:1.1em;">{stripped}</strong>')
        else:
            # Colorize direction tags, then append as a line
            colorized = _colorize_direction_tags(line)
            html_lines.append(colorized)
    return '<br>\n'.join(html_lines)


def _direction_label(direction_int):
    """Convert integer direction to label and color."""
    if direction_int >= 2:
        return '[STRONGLY BULLISH]', '#66bb6a'
    elif direction_int == 1:
        return '[BULLISH]', '#66bb6a'
    elif direction_int == -1:
        return '[BEARISH]', '#ef5350'
    elif direction_int <= -2:
        return '[STRONGLY BEARISH]', '#ef5350'
    else:
        return '[NEUTRAL]', '#90a4ae'


def build_catalyst_html(summary_path, json_path):
    """
    Build an HTML section for catalyst alerts.

    Returns an HTML string if catalyst data is found, or empty string if neither
    file exists or both are empty.
    """
    summary_p = Path(summary_path)
    json_p = Path(json_path)

    # Primary path: use human-readable summary text
    if summary_p.exists() and summary_p.stat().st_size > 0:
        try:
            content = summary_p.read_text(encoding='utf-8').strip()
            if content:
                mtime = summary_p.stat().st_mtime
                # Format mtime as IST (UTC+3)
                dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
                # IST = UTC+3 (Israel Standard Time)
                from datetime import timedelta
                ist_offset = timedelta(hours=3)
                dt_ist = dt_utc + ist_offset
                updated_str = dt_ist.strftime('%Y-%m-%d %H:%M')

                body_html = _text_to_html(content)
                return (
                    '<div style="font-family:monospace;background:#1a1a2e;color:#e0e0e0;'
                    'padding:16px;border-radius:6px;margin-top:24px;">'
                    '<h2 style="color:#2196F3;margin-top:0;">Catalyst Alerts</h2>'
                    f'<p style="color:#90a4ae;margin-top:-8px;font-size:0.85em;">'
                    f'Last updated: {updated_str} IST</p>'
                    f'{body_html}'
                    '</div>'
                )
        except Exception as e:
            print(f"Warning: Could not read catalyst summary: {e}")

    # Fallback path: format from JSON
    if json_p.exists() and json_p.stat().st_size > 0:
        try:
            with json_p.open(encoding='utf-8') as f:
                catalysts = json.load(f)
            if not catalysts:
                return ''

            mtime = json_p.stat().st_mtime
            from datetime import timedelta
            dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
            ist_offset = timedelta(hours=3)
            dt_ist = dt_utc + ist_offset
            updated_str = dt_ist.strftime('%Y-%m-%d %H:%M')

            rows = []
            for c in catalysts:
                ticker = c.get('ticker', '')
                direction = c.get('direction', 0)
                label, color = _direction_label(direction)
                status = c.get('status', '')
                timeframe = c.get('timeframe', '')
                desc = c.get('catalyst_description', '')
                notes = c.get('research_notes', '')
                confidence = c.get('confidence_level', '')

                status_html = ''
                if status:
                    status_html = f' <span style="color:#ffa726;">[{status.upper()}]</span>'

                notes_html = ''
                if notes:
                    notes_html = (
                        f'<br><span style="color:#b0bec5;font-size:0.9em;">'
                        f'Notes: {notes}</span>'
                    )

                rows.append(
                    f'<div style="margin-bottom:12px;padding:8px;border-left:3px solid {color};">'
                    f'<strong style="font-size:1.1em;">{ticker}</strong> '
                    f'<span style="color:{color};font-weight:bold;">{label}</span>'
                    f'{status_html}<br>'
                    f'<span style="color:#cfd8dc;">{desc}</span><br>'
                    f'<span style="color:#90a4ae;font-size:0.85em;">'
                    f'Timeframe: {timeframe} | Confidence: {confidence}</span>'
                    f'{notes_html}'
                    f'</div>'
                )

            body_html = '\n'.join(rows)
            return (
                '<div style="font-family:sans-serif;background:#1a1a2e;color:#e0e0e0;'
                'padding:16px;border-radius:6px;margin-top:24px;">'
                '<h2 style="color:#2196F3;margin-top:0;">Catalyst Alerts</h2>'
                f'<p style="color:#90a4ae;margin-top:-8px;font-size:0.85em;">'
                f'Last updated: {updated_str} IST</p>'
                f'{body_html}'
                '</div>'
            )
        except Exception as e:
            print(f"Warning: Could not read catalysts JSON: {e}")

    # Neither file exists or both are empty
    return ''


def send_email(results, file_path, recipient_email, sender_email, sender_password, catalyst_html=''):
    """
    Send execution results via email with PNG attachment if available.
    When catalyst_html is provided, sends a multipart/alternative email with
    both plain text and HTML parts.
    """
    # Outer container: mixed (supports attachments)
    msg = MIMEMultipart('mixed')
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

    if catalyst_html:
        # Multipart/alternative: plain text + HTML (with catalyst section)
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText(body, 'plain'))
        html_body = (
            '<html><body>'
            f'<pre style="font-family:monospace;white-space:pre-wrap;">{body}</pre>'
            f'{catalyst_html}'
            '</body></html>'
        )
        alternative.attach(MIMEText(html_body, 'html'))
        msg.attach(alternative)
    else:
        # No catalyst data — plain text only (existing behavior preserved)
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
    # Load environment variables from .env if present
    load_dotenv()

    # Configuration
    PYTHON_FILE = 'stock_portfolio_risk.py'  # Path to the Python file you want to run
    RECIPIENT_EMAIL = os.getenv('TRADING_EMAIL_TO')
    SENDER_EMAIL = os.getenv('TRADING_EMAIL_FROM')
    SENDER_PASSWORD = os.getenv('TRADING_EMAIL_PASSWORD')  # Use App Password for Gmail

    # Catalyst data paths (written by substack-automation pipeline)
    CATALYST_SUMMARY_FILE = os.getenv(
        'CATALYST_SUMMARY_FILE',
        os.path.expanduser('~/Documents/Trading/catalyst_summary.txt')
    )
    CATALYSTS_JSON_FILE = os.getenv(
        'CATALYSTS_JSON_FILE',
        os.path.expanduser('~/Documents/Trading/catalysts.json')
    )

    if not RECIPIENT_EMAIL or not SENDER_EMAIL or not SENDER_PASSWORD:
        raise RuntimeError(
            "Missing email configuration. Set TRADING_EMAIL_TO, TRADING_EMAIL_FROM, "
            "and TRADING_EMAIL_PASSWORD environment variables."
        )

    # Run the Python file
    print(f"Running {PYTHON_FILE}...")
    results = run_python_file(PYTHON_FILE)

    # Build catalyst HTML section (empty string if no catalyst files present)
    catalyst_html = build_catalyst_html(CATALYST_SUMMARY_FILE, CATALYSTS_JSON_FILE)

    # Send results via email
    print("Sending results via email...")
    send_email(results, PYTHON_FILE, RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD, catalyst_html)

if __name__ == '__main__':
    main()
