# Patient Management API

A FastAPI-based backend application to manage patient records.  
This API supports creating, reading, updating, deleting patients and also calculates BMI with a health verdict.

## Features
- Create new patients
- Update patient information
- Delete patient records
- View single or all patients
- Sort patients by height, weight, or BMI
- Automatic BMI and verdict calculation

## Run the project
```bash
uvicorn main:app --reload
