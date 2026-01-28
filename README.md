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
python send_whatsapp_files.py <path_to_csv_or_xlsx> [options]
```

### Basic Examples

```bash
# Use default message template with per-contact files from CSV
python send_whatsapp_files.py contacts.xlsx

# Send a custom message to all contacts (no attachment)
python send_whatsapp_files.py contacts.csv -m "Hello! This is a reminder."

# Send a custom message with the same attachment to all contacts
python send_whatsapp_files.py contacts.csv -m "Check this out!" -a flyer.jpg

# Send just an attachment (same for all) with default message template
python send_whatsapp_files.py contacts.csv -a announcement.pdf
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `-m`, `--message` | Custom message to send to all contacts (overrides the default template) |
| `-a`, `--attachment` | Path to attachment file to send to all contacts (overrides the `dir` column) |
| `-h`, `--help` | Show help message and exit |

## Data File Format

Your CSV or XLSX file must have these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `celular` | Yes | Phone number (e.g., 0998765645) |
| `dir` | Only if not using `-a` | Filename of the file to send (located in `invitaciones/`) |
| `representante` | No | Contact name (used in message template) |
| `club` | No | Club name (used in message template) |

## How It Works

1. Run the script with your contacts file and optional flags
2. For each contact, the script will:
   - Open WhatsApp Desktop to the contact's chat with a pre-filled message
   - Copy the file to your clipboard (if an attachment is specified)
3. You manually:
   - Send the pre-filled message (press Enter or click Send)
   - Paste the file (Cmd+V) if an attachment was provided
   - Send the file (press Enter or click Send)
   - Return to the terminal and press Enter for the next contact

## Configuration

Edit `send_whatsapp_files.py` to customize:

- `COUNTRY_CODE`: Default is "593" (Ecuador)
- `FILES_BASE_DIR`: Directory where files are stored (for per-contact attachments)
- `MESSAGE_TEMPLATE`: The default message template (supports `{representante}` and `{club}` placeholders)
