from dotenv import load_dotenv
import os

load_dotenv()

print("EMAIL_USERNAME =", os.getenv("EMAIL_USERNAME"))
print("EMAIL_PASSWORD =", os.getenv("EMAIL_PASSWORD"))