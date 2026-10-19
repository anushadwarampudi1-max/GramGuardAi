# GramGuardAI – AI-Powered Public Complaint Management System

## About the Project

GramGuardAI is a web-based application that helps users manage public complaints. It uses keyword-based text analysis to categorize complaints, assign departments, determine priority levels, and estimate confidence scores.

## Features

* Complaint categorization
* Automatic department assignment
* Priority detection (Critical, High, Medium)
* Confidence score calculation
* Complaint management dashboard
* Login page and admin interface
* Flask-based web application

## Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* SQLite
* Gunicorn

## Project Structure

* app.py – Main Flask application
* ai_model.py – Complaint classification and priority logic
* templates/ – HTML pages
* static/ – Static files, if required
* gramguard.db – SQLite database
* requirements.txt – Python dependencies
* Procfile – Deployment start command

## How to Run Locally

1. Install Python.
2. Install the required packages:
   pip install -r requirements.txt
3. Start the application:
   python app.py
4. Open the local URL displayed in the terminal.

## Deployment

The application can be deployed on Render using the connected GitHub repository.

Build command:
pip install -r requirements.txt

Start command:
gunicorn app:app

## Purpose

The purpose of GramGuardAI is to make public complaint handling more organized by helping classify complaints and identify their urgency.

## Note

The classification system uses predefined keywords. Its categories, priorities, and confidence scores are estimates and should be reviewed before making real-world decisions.
