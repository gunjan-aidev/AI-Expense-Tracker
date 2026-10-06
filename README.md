# Smart Expense Tracker API

An AI-powered expense tracking backend built with FastAPI, PostgreSQL, and Ollama.

## Features

- Create expenses through a REST API
- Automatically categorize expenses using a local LLM
- Store expenses in PostgreSQL
- Retrieve all expenses
- Retrieve an expense by ID
- Delete expenses
- Filter expenses by category
- Filter expenses by month
- Generate spending summaries
- Validate request data with Pydantic
- Validate AI output using a structured schema
- Use parameterized SQL queries
- Keep database credentials in environment variables

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQL
- PostgreSQL
- psycopg
- Ollama
- Qwen 3 4B
- Git/GitHub

## Architecture

Client
→ FastAPI
→ Pydantic validation
→ Ollama AI categorization
→ AI output validation
→ PostgreSQL
→ API response

## Example

### Create an expense

```json
POST /expenses

{
    "title": "Swiggy",
    "amount": 450,
    "expense_date": "2026-10-06"
}