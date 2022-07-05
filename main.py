import flashcard
import sys 
from dotenv import load_dotenv,find_dotenv

app = flashcard.create_app()

if __name__ == "__main__":
   app.run(host="localhost",port=8000,debug=True)