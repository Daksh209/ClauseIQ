# ClauseIQ

ClauseIQ is an AI-powered Intelligent Document Processing (IDP) system designed to automate information extraction from legal contracts and agreements.

The system combines:

- Optical Character Recognition (OCR)
- Natural Language Processing (NLP)
- Named Entity Recognition (NER)
- Rule-based Validation
- REST API Integration

to extract and process important legal information from PDF documents.

---

# Project Objective

The primary objective of ClauseIQ is to build a production-style AI pipeline capable of:

1. Extracting text from scanned legal contracts and PDF files
2. Detecting legal entities using a custom-trained NLP model
3. Validating extracted entities using rule-based logic
4. Normalizing entities into structured formats
5. Providing results through a REST API and Web Interface
6. Creating a modular and scalable legal document analysis system

---

# Key Features

## 1. OCR Pipeline

- PDF text extraction
- OCR support for scanned documents
- Tesseract OCR integration
- Automatic text processing

---

## 2. NLP & Named Entity Recognition (NER)

Custom-trained spaCy NER model trained using the CUAD legal dataset.

### Supported Entities

| Entity | Description                        |
| ------ | ---------------------------------- |
| DATE   | Contract dates and effective dates |
| ORG    | Organization and party names       |
| MONEY  | Financial and payment values       |

---

## 3. Validation & Normalization Engine

The system includes a post-processing layer for improving extraction quality.

### Features

- Rule-based validation
- Invalid entity filtering
- Legal date normalization
- Entity cleanup
- Structured JSON formatting

---

## 4. REST API

Flask-based API for external integrations.

### API Capabilities

- Upload legal PDFs
- Extract legal entities
- Return structured JSON responses
- Integration-ready backend service

---

## 5. Frontend Interface

Simple and responsive frontend interface for:

- Uploading PDF files
- Running AI extraction
- Viewing extracted entities
- Displaying structured legal information

---

## 6. Deployment Ready

- Docker-ready architecture
- Modular project structure
- API-based backend
- Production-style pipeline design

---

# System Architecture

```text
PDF / Image Upload
        ↓
OCR Pipeline
        ↓
Extracted Text
        ↓
spaCy NER Model
        ↓
Validation Layer
        ↓
Normalization Engine
        ↓
Structured JSON Output
        ↓
Flask API / Frontend UI
```
