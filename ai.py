import ollama

from models import AIExpenseCategory


MODEL_NAME = "qwen3:4b"


def categorize_expense(title: str) -> str:
    prompt = f"""
Classify the expense below into exactly one of these categories:

Food
Transport
Shopping
Entertainment
Bills
Healthcare
Travel
Education
Other

Expense title:
<{title}>

Return only the category field according to the provided JSON schema.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format=AIExpenseCategory.model_json_schema(),
        options={
            "temperature": 0,
        },
    )

    result = AIExpenseCategory.model_validate_json(
        response["message"]["content"]
    )

    return result.category