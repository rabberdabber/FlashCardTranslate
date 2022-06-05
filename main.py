import flashcard
import config

app = flashcard.create_app(config)

if __name__ == "__main__":
   app.run(host="127.0.0.1",port=5555,debug=True)