# Installation Guide - Fayda PDF Downloader Bot

## በአማርኛ | In Amharic

ይህ ሰነድ Fayda PDF Downloader Telegram Bot ለመጫን ለማንም ሰው በየደረጃ መመሪያ ይሰጣል።

## Prerequisites (ቅድሚያ-ሞከርስታ)

- Python 3.8 ወይም ይሃንm በላይ
- Telegram Account
- GitHub Account (ለ repository)

## Step 1: Bot Token ከBotFather ያግኙ

1. Telegram ላይ `@BotFather` ን ፈልጉ
2. `/start` ይላኩ
3. `/newbot` ይላኩ
4. ቦት ስም ይስጡ (ለምሳሌ: "Fayda PDF Downloader")
5. Unique username ይስጡ (ለምሳሌ: "fayda_pdf_downloader_bot")
6. Token ይወሰደውታል - ይህ ያስፈልግሃል!

## Step 2: Repository Clone ያድርጉ

```bash
git clone https://github.com/habtesheman22-alt/fayda-pdf-downloader.git
cd fayda-pdf-downloader
```

## Step 3: Virtual Environment ይሰጡ

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\\Scripts\\activate
```

## Step 4: Dependencies ይጫኑ

```bash
pip install -r requirements.txt
```

## Step 5: .env File ይፍጠሩ

```bash
cp .env.example .env
```

`.env` ውስጥ ያስገቡ:

```
TELEGRAM_BOT_TOKEN=8698378440:AAEat2w2qbpqJp-w36aOPdge8cpZAJs7cBw
FAYDA_FORM_URL=https://your-pdf-url.com/form.pdf
INSTRUCTIONS_URL=https://your-pdf-url.com/instructions.pdf
REQUIREMENTS_URL=https://your-pdf-url.com/requirements.pdf
FEE_INFO_URL=https://your-pdf-url.com/fees.pdf
```

## Step 6: ቦት ያስኬዱ

```bash
python bot.py
```

✅ ቦት ይሰራል! Telegram ላይ ወደ ቦትዎ ይሂዱ (username) እና `/start` ይላኩ।

## Troubleshooting

### Bot Token Invalid
- BotFather ወደ `/start` ይመለሱ
- `/mybots` ይላኩ
- ቦትዎን ይመርጡ
- `API Token` ይፈልጉ

### PDF Download Not Working
- PDF URLs በትክክል ተገናኝተዋል
- Internet ያገናኘ ነው
- Logs ይመልከቱ (console ውስጥ)

## Commands

- `/start` - ቦትን ጀምር
- `/help` - ይህ ላይ ይመልከቱ
- `/documents` - ሰነዶች ተመልከት
- `/amharic` - አማርኛ ይምረጡ
- `/english` - English ይምረጡ
