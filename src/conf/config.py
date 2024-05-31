with open('password.txt', 'r') as file:
    password = file.read()

class Config:
    DB_URL = f'postgresql+asyncpg://postgres:{password}@localhost:5432/postgres'
    
config = Config
