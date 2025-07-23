![Project Logo](assets/logo.png)  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  ![License](https://img.shields.io/badge/License-MIT-green)

# PDF Content Analysis & Question Generation
A lightweight CLI tool that:
1. Extracts text and images from a PDF
2. Generates multiple‑choice questions for educational use
3. Outputs structured JSON for downstream consumption

---

## Features
- PDF text and image extraction (PyMuPDF, pdfplumber)
- Image handling and export (Pillow)
- AI‑powered question generation using Hugging Face and Google Generative AI
- Simple command‑line interface

---

## File Overview
| File               | Description                                                         |
|--------------------|---------------------------------------------------------------------|
| `scripts.py`       | Defines `extract_content_from_pdf()` and `generate_questions()`      |
| `main.py`          | CLI entry point that invokes functions from `scripts.py`            |
| `.env`             | Stores API keys and environment variables (Hugging Face, Google)    |
| `requirements.txt` | Lists all Python dependencies                                       |
| `output.json`      | Sample JSON output from content extraction                           |
| `questions.json`   | Sample JSON output from question generation                          |

---

## Future Enhancements
- Fine‑tune the question model on domain‑specific curricula
- Support diverse question formats (MCQ, fill‑in‑the‑blank)
- Dockerize for consistent deployment

---

© 2025 Poorvesh Chaudhari

