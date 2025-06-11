# Email Assistant

An AI-powered email assistant that helps users manage email communications by summarizing emails, retrieving context from previous conversations, and generating suggested replies.

Built with **FastAPI**, **React (Vite + TypeScript + Tailwind CSS)**, **OpenAI API**, **Pinecone vector search**, and **Microsoft Graph API** for seamless email integration.

---

## Features

- **Authentication** (JWT + Google OAuth2)
- **Email syncing** via Microsoft Graph API
- **Database storage** for emails, users, and leads (SQL)
- **Contextual reply generation** using OpenAI and vector embeddings
- **Semantic search** of past conversations with Pinecone
- **Summarized email threads** and intent classification
- **Suggested reply drafts** based on historical context
- **Frontend interface** with React, Vite, Tailwind, Shadcn UI

---

## Tech Stack

| Backend  | Frontend | AI & Search | Integrations |
|----------|----------|--------------|---------------|
| FastAPI  | React (Vite + TypeScript) | OpenAI API (GPT-4) | Microsoft Graph API |
| MongoDB Atlas | Tailwind CSS + Shadcn UI | Pinecone | Google OAuth2 |
| JWT Authentication | | | |

---

## Repository Structure

```bash
email-assistant/
├── email-assistant-backend/        # FastAPI backend
│   ├── app/
│   └── ...
├── email-assistant/                # React frontend (Vite + TypeScript + Tailwind)
│   └── ...
├── README.md
└── .env.example                    # Environment variable templates
