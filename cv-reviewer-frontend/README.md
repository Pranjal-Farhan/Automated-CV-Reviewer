# CV Reviewer — Frontend

A modern React frontend for the AI-Powered Automated CV Reviewer. Built with
React 18, Vite, and React Router. Features JWT authentication, Google OAuth,
and a polished dark-mode UI.

## Features

- **Authentication** — Email/password registration & login, plus Google OAuth
- **CV Upload** — Drag-and-drop file upload (PDF or TXT, max 10 MB)
- **Real-time Processing** — Polling-based progress tracking while the AI analyzes
- **Structured Results** — Candidate info, skills, experience, education, and recommendations displayed in clean cards
- **History** — View all past CV analyses
- **Responsive** — Fully responsive from mobile to desktop
- **Dark Theme** — Modern dark UI with subtle animations

## Tech Stack

| Tool                | Purpose                  |
| ------------------- | ------------------------ |
| React 18            | UI framework             |
| Vite                | Build tool & dev server  |
| React Router v6     | Client-side routing      |
| Axios               | HTTP client              |
| @react-oauth/google | Google OAuth integration |
| jwt-decode          | JWT token handling       |
| Lucide React        | Icon library             |

## Prerequisites

- **Node.js 18+** and npm
- The backend API running at `http://localhost:8000`
- A Google OAuth Client ID (for Google sign-in)

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/cv-reviewer-frontend.git
cd cv-reviewer-frontend
```
