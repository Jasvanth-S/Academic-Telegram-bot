# 🤖 ACT – AI Academic Assistant Telegram Bot

ACT is an AI-powered Telegram bot built using **Python and Aiogram** to assist college students with academic-related queries.  
It integrates **MongoDB** for user management and **HuggingFace LLM (via Router)** for intelligent responses.  
The bot is deployed as a **24/7 cloud worker on Render**.

---

## ✨ Features

- 🔐 Mobile number verification (Telegram contact)
- 👤 User registration (name, year, department)
- 🧠 AI-powered academic assistant
- 📚 Helps with exams, timetable, notes & events
- 🗑️ Auto-deletes user and bot messages (privacy-focused)
- ☁️ Runs 24/7 on Render (free worker)

---

## 🛠️ Tech Stack

- **Python 3**
- **Aiogram**
- **MongoDB (Motor)**
- **HuggingFace Router (LLM)**
- **Render Cloud**
- **Telegram Bot API**

---

## 📁 Project Structure

ACT_bot/
├── bot.py
├── handlers.py
├── llm.py
├── db.py
├── config.py
├── requirements.txt
├── render.yaml
└── .env (not committed)

---

## 🔐 Environment Variables

Create a `.env` file (for local use):

```env
BOT_TOKEN=your_telegram_bot_token
HF_TOKEN=your_huggingface_token
MONGO_URI=mongodb+srv://your_mongodb_uri
DB_NAME=college_bot
