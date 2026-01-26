# WhatsApp Mass Message Sender

A semi-manual WhatsApp file sender for macOS. Reads a CSV/XLSX file with contact information and helps you send files by opening the chat, pre-filling a message, and copying the file to clipboard.

## Requirements

- macOS
- Python 3.x
- WhatsApp Desktop (installed and logged in)

## Installation

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install pandas openpyxl pyobjc-framework-Cocoa
   ```

## Usage

```bash
python send_whatsapp_files.py <path_to_csv_or_xlsx>
```

Example:
```bash
python send_whatsapp_files.py contacts.xlsx
```

## Data File Format

Your CSV or XLSX file must have these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `celular` | Yes | Phone number (e.g., 0998765645) |
| `dir` | Yes | Filename of the PDF to send (located in `invitaciones/`) |
| `representante` | No | Contact name (used in message template) |
| `club` | No | Club name (used in message template) |

## How It Works

1. Run the script with your contacts file
2. For each contact, the script will:
   - Open WhatsApp Desktop to the contact's chat with a pre-filled message
   - Copy the PDF file to your clipboard
3. You manually:
   - Send the pre-filled message (press Enter or click Send)
   - Paste the file (Cmd+V)
   - Send the file (press Enter or click Send)
   - Return to the terminal and press Enter for the next contact

## Configuration

Edit `send_whatsapp_files.py` to customize:

- `COUNTRY_CODE`: Default is "593" (Ecuador)
- `FILES_BASE_DIR`: Directory where PDF files are stored
- `MESSAGE_TEMPLATE`: The message sent with each file
