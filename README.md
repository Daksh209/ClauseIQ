# LexiScan Auto

LexiScan Auto is an AI-powered Intelligent Document Processing (IDP) system designed to automate information extraction from legal contracts and agreements.

The system combines Optical Character Recognition (OCR), Natural Language Processing (NLP), Named Entity Recognition (NER), and rule-based validation to extract important legal entities such as:

- Contract Dates
- Organization Names
- Monetary Values
- Legal Clauses

---

# Project Objective

The goal of this project is to build a production-style AI pipeline capable of:

1. Extracting text from scanned legal documents and PDFs
2. Identifying important legal entities using a custom-trained NLP model
3. Validating extracted entities using rule-based logic
4. Exposing the pipeline through a REST API
5. Deploying the complete system using Docker

---

# System Architecture

PDF / Image
      ↓
OCR Pipeline
      ↓
Extracted Text
      ↓
NER Model (spaCy)
      ↓
Validation Layer
      ↓
Structured JSON Output
      ↓
REST API Response

# Features

1. OCR Pipeline
     -- PDF text extraction
     -- Image preprocessing
     -- Tesseract OCR integration
2. NLP & NER
     -- Custom spaCy Named Entity Recognition model
     -- Trained using CUAD Legal Dataset
     -- Detects:
        - DATE
        - ORG
        - MONEY
3. Validation Engine
     -- Rule-based validation
     -- Date normalization
     -- Entity cleanup
     -- Structured JSON formatting
4. REST API
     -- Flask-based API
     -- JSON input/output
     -- Integration-ready microservice
5. Deployment
     -- Dockerized architecture
     -- Reproducible environment setup



