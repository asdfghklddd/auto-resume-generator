# Auto Resume Generator

An AI-assisted resume editor built with Vue 3 and FastAPI. It turns unstructured career notes into validated resume data, keeps every generated field editable, renders an A4 preview in the browser, and exports through the browser's native print-to-PDF flow.

## Highlights

- Structured generation: Gemini returns data validated against explicit Pydantic models.
- Human review: generated content remains editable before export.
- Lightweight PDF workflow: CSS print styles avoid a server-side browser renderer.
- Single deployment unit: FastAPI serves the production Vue build and the API.
- Privacy-aware defaults: the API key stays server-side, request size is bounded, and provider errors are not returned to clients.

## Architecture

```text
Vue editor and A4 preview
          |
          | POST /api/generate
          v
FastAPI validation and concurrency guard
          |
          v
Gemini structured output -> Pydantic ResumeData
```

The frontend uses Vue 3, TypeScript, Tailwind CSS 4, and Vite. The backend uses FastAPI, Pydantic, and the Google Gen AI SDK.

## Run locally

Requirements: Node.js 22+ and Python 3.12+.

```powershell
git clone https://github.com/asdfghklddd/auto-resume-generator.git
Set-Location auto-resume-generator

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

Copy-Item .env.example .env
# Set GEMINI_API_KEY in .env

Set-Location frontend
npm ci
npm run build
Set-Location ..

python run.py
```

Open `http://127.0.0.1:8000`.

For frontend development, run `npm run dev` in `frontend/`; the Vite development server proxies `/api` to the local FastAPI service.

## Privacy boundary

Resume text submitted for generation is sent to the configured Gemini API. Do not submit identity documents, account credentials, home addresses, or other information that is not necessary for drafting a resume. Add sensitive contact details manually after generation when possible.

The repository contains only placeholder configuration. A real `.env` file is ignored by Git.

## Project status

This is a portfolio-stage application. The current version focuses on the generation, review, preview, and PDF export workflow. Authentication, persistent user accounts, and hosted multi-user deployment are intentionally out of scope.

## Usage rights

The source is published for portfolio review. No redistribution or commercial-use license is granted.
