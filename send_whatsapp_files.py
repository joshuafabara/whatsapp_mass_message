#!/usr/bin/env python3
"""
Semi-manual WhatsApp file sender for macOS.

Reads a CSV/XLSX file with contact information and helps you send files
by opening the chat and copying the file to clipboard. You just paste and send.

Required columns in your data file:
- celular: Phone number (e.g., 0998765645)
- dir: Path to the PDF file to send (optional if using --attachment flag)

Optional columns:
- representante: Contact name (for display)
- club: Club name (for display)
"""

import argparse
import subprocess
import sys
import time
import os
from pathlib import Path
from urllib.parse import quote

# Check for required packages
def check_dependencies():
    missing = []
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    try:
        import openpyxl
    except ImportError:
        missing.append("openpyxl")
    try:
        from AppKit import NSPasteboard
    except ImportError:
        missing.append("pyobjc-framework-Cocoa")

    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print(f"Install them with: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import pandas as pd

# Configuration
COUNTRY_CODE = "593"  # Ecuador

# Base directory where PDF files are stored
FILES_BASE_DIR = "/Users/joshuafabara/Sites/whatsapp_mass_message/invitaciones"

# Message template - use {representante} and {club} as placeholders
MESSAGE_TEMPLATE = "Hola {representante} tenemos el agrado de invitar a tu club {club} al torneo Just Lift Alpha Cup Apertura 2026. Adjunta tienes la invitación formal, solo responde a este mensaje con las categorías en las que desean participar. ¡Saludos!"


def format_phone_number(phone):
    """Convert local number to international format without +."""
    phone_str = str(phone).strip()
    # Remove any spaces, dashes, or other characters
    phone_str = ''.join(filter(str.isdigit, phone_str))

    # Remove leading 0 if present
    if phone_str.startswith('0'):
        phone_str = phone_str[1:]

    # Add country code if not present
    if not phone_str.startswith(COUNTRY_CODE):
        phone_str = COUNTRY_CODE + phone_str

    return phone_str


def copy_file_to_clipboard(file_path):
    """Copy a file to macOS clipboard using PyObjC."""
    from AppKit import NSPasteboard, NSURL

    abs_path = os.path.abspath(file_path)

    if not os.path.exists(abs_path):
        return False, f"File not found: {abs_path}"

    try:
        file_url = NSURL.fileURLWithPath_(abs_path)
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()
        result = pb.writeObjects_([file_url])

        if result:
            return True, None
        else:
            return False, "Failed to write to clipboard"
    except Exception as e:
        return False, f"Failed to copy to clipboard: {e}"


def open_whatsapp_chat(phone_number, message=None):
    """Open WhatsApp Desktop to a specific chat, optionally with a pre-filled message."""
    if message:
        encoded_message = quote(message)
        url = f"whatsapp://send?phone={phone_number}&text={encoded_message}"
    else:
        url = f"whatsapp://send?phone={phone_number}"
    subprocess.run(['open', url], check=True)


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def load_data(file_path):
    """Load CSV or XLSX file."""
    file_path = Path(file_path)

    if file_path.suffix.lower() == '.csv':
        # Try semicolon delimiter first (common in some regions), fallback to comma
        try:
            df = pd.read_csv(file_path, sep=';')
            # If we only got one column, the delimiter was wrong
            if len(df.columns) == 1:
                df = pd.read_csv(file_path, sep=',')
        except:
            df = pd.read_csv(file_path, sep=',')
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

    # Normalize column names to lowercase for consistent access
    df.columns = df.columns.str.lower().str.strip()
    return df


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Semi-manual WhatsApp file sender for macOS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default message template with per-contact files from CSV
  python send_whatsapp_files.py contacts.csv

  # Send a custom message to all contacts (no attachment)
  python send_whatsapp_files.py contacts.csv -m "Hello! This is a reminder."

  # Send a custom message with the same attachment to all contacts
  python send_whatsapp_files.py contacts.csv -m "Check this out!" -a image.jpg

  # Send just an attachment with default message template
  python send_whatsapp_files.py contacts.csv -a flyer.pdf
        """
    )
    parser.add_argument(
        "data_file",
        help="Path to CSV or XLSX file with contact information"
    )
    parser.add_argument(
        "-m", "--message",
        help="Custom message to send to all contacts (overrides the default template)"
    )
    parser.add_argument(
        "-a", "--attachment",
        help="Path to attachment file to send to all contacts (overrides the 'dir' column)"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    data_file = args.data_file
    custom_message = args.message
    custom_attachment = args.attachment

    if not os.path.exists(data_file):
        print(f"Error: File not found: {data_file}")
        sys.exit(1)

    # Validate custom attachment if provided
    if custom_attachment and not os.path.exists(custom_attachment):
        print(f"Error: Attachment file not found: {custom_attachment}")
        sys.exit(1)

    # Load data
    print(f"Loading data from: {data_file}")
    df = load_data(data_file)

    # Validate required columns
    # 'dir' column is only required if no custom attachment is provided
    required_cols = ['celular']
    if not custom_attachment:
        required_cols.append('dir')

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)

    # Filter out empty rows
    df = df.dropna(subset=['celular'])
    df = df[df['celular'].astype(str).str.strip() != '']

    if not custom_attachment and 'dir' in df.columns:
        df = df.dropna(subset=['dir'])
        df = df[df['dir'].astype(str).str.strip() != '']

    total = len(df)
    print(f"Found {total} contacts to process.")
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("1. Make sure WhatsApp Desktop is open and logged in")
    print("2. For each contact, the script will:")
    print("   - Open the chat with a pre-filled message")
    if custom_attachment:
        print(f"   - Copy the attachment to your clipboard: {custom_attachment}")
    else:
        print("   - Copy the file to your clipboard")
    print("3. You need to:")
    print("   - Press Enter or Send (to send the message)")
    if custom_attachment or 'dir' in df.columns:
        print("   - Press Cmd+V to paste the file")
        print("   - Press Enter or Send again (to send the file)")
    print("   - Come back here and press Enter for the next contact")
    print("="*60)

    # Determine message to display
    if custom_message:
        print(f"\nCustom message:")
        print(f"  \"{custom_message}\"")
    else:
        print(f"\nMessage template:")
        print(f"  \"{MESSAGE_TEMPLATE}\"")

    if custom_attachment:
        print(f"\nAttachment (same for all contacts):")
        print(f"  \"{os.path.abspath(custom_attachment)}\"")

    print("="*60)

    input("\nPress Enter to start...")

    # Track progress
    sent = 0
    skipped = 0
    errors = []

    for idx, row in df.iterrows():
        clear_screen()

        phone = format_phone_number(row['celular'])
        name = row.get('representante', 'N/A') if 'representante' in row.index else 'N/A'
        club = row.get('club', 'N/A') if 'club' in row.index else 'N/A'

        # Determine file path
        if custom_attachment:
            file_path = os.path.abspath(custom_attachment)
        elif 'dir' in row.index and pd.notna(row['dir']):
            filename = str(row['dir']).strip()
            file_path = os.path.join(FILES_BASE_DIR, filename)
        else:
            file_path = None

        # Generate message
        if custom_message:
            message = custom_message
        else:
            message = MESSAGE_TEMPLATE.format(representante=name, club=club)

        print(f"\n{'='*60}")
        print(f"CONTACT {idx + 1} of {total}")
        print(f"{'='*60}")
        print(f"Name:  {name}")
        print(f"Club:  {club}")
        print(f"Phone: {phone}")
        if file_path:
            print(f"File:  {file_path}")
        print(f"\nMessage: {message}")
        print(f"{'='*60}")

        # Handle attachment if needed
        if file_path:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"\n[ERROR] File not found: {file_path}")
                errors.append((name, phone, f"File not found: {file_path}"))
                input("Press Enter to skip to next contact...")
                skipped += 1
                continue

            # Copy file to clipboard
            success, error = copy_file_to_clipboard(file_path)
            if not success:
                print(f"\n[ERROR] {error}")
                errors.append((name, phone, error))
                input("Press Enter to skip to next contact...")
                skipped += 1
                continue

            print("\n[OK] File copied to clipboard!")

        # Open WhatsApp chat with pre-filled message
        print("[OK] Opening WhatsApp chat with message...")
        open_whatsapp_chat(phone, message)

        # Give WhatsApp time to open
        time.sleep(1.5)

        print("\n" + "-"*60)
        print("NOW DO THIS:")
        print("  1. Click on the WhatsApp window")
        print("  2. Press Enter or click Send (message is pre-filled)")
        if file_path:
            print("  3. Press Cmd+V to paste the file")
            print("  4. Press Enter or click Send again")
        print("-"*60)

        response = input("\nPress Enter when done (or 's' to skip, 'q' to quit): ").strip().lower()

        if response == 'q':
            print("\nQuitting early...")
            break
        elif response == 's':
            skipped += 1
            print("Skipped.")
        else:
            sent += 1

    # Summary
    clear_screen()
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total contacts: {total}")
    print(f"Sent:           {sent}")
    print(f"Skipped:        {skipped}")
    print(f"Errors:         {len(errors)}")

    if errors:
        print("\nErrors encountered:")
        for name, phone, error in errors:
            print(f"  - {name} ({phone}): {error}")

    print("\nDone!")


if __name__ == "__main__":
    main()
