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

# Send a custom message with placeholders from CSV columns
python send_whatsapp_files.py contacts.csv -m "Hola {representante} de {club}, te invitamos!"

# See available placeholders for your CSV file
python send_whatsapp_files.py contacts.csv --show-placeholders

# Send a custom message with the same attachment to all contacts
python send_whatsapp_files.py contacts.csv -m "Check this out!" -a flyer.jpg

# Send just an attachment (same for all) with default message template
python send_whatsapp_files.py contacts.csv -a announcement.pdf
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `-m`, `--message` | Custom message with placeholders like `{representante}`, `{club}`, etc. (see `--show-placeholders`) |
| `-a`, `--attachment` | Path to attachment file to send to all contacts (overrides the `dir` column) |
| `--show-placeholders` | Show available placeholders from the CSV file and exit |
| `-h`, `--help` | Show help message and exit |

## Message Placeholders

You can use placeholders in your custom messages that will be replaced with values from your CSV columns. Use curly braces around the column name:

```bash
python send_whatsapp_files.py contacts.csv -m "Hola {representante} de {club}, te invitamos al evento!"
```

To see all available placeholders for your specific CSV file:

```bash
python send_whatsapp_files.py contacts.csv --show-placeholders
```

Example output:
```
Available placeholders from 'contacts.csv':
==================================================
  {item}  (e.g., "1")
  {club}  (e.g., "ANDES BASKET CLUB")
  {representante}  (e.g., "Edwin Velasco")
  {celular}  (e.g., "991484150")
  {dir}  (e.g., "ANDES BASKET CLUB.pdf")
==================================================
```

If you use a placeholder that doesn't exist in the CSV, it will remain unchanged in the message.

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
- `MESSAGE_TEMPLATE`: The default message template (supports any CSV column as placeholder, e.g., `{representante}`, `{club}`)
