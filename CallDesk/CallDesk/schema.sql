CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth_user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Agent', 'Manager', 'Staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
