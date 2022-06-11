import flashcard
import sys 
from dotenv import load_dotenv,find_dotenv
print(load_dotenv(find_dotenv()))

app = flashcard.create_app()

if __name__ == "__main__":
   app.run(host="localhost",port=5555,debug=True)