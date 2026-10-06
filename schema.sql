CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    category VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_expenses_date
ON expenses (expense_date);

CREATE INDEX IF NOT EXISTS idx_expenses_category
ON expenses (category);