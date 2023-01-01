from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.sqlite import SQLiteDatabse
from utils.email_utils import preprocess_email
from utils.logger_utils import get_logger

logger = get_logger('API')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class Email(BaseModel):
    email: str


@app.post("/classify")
def classify_email(email: Email):
    try:
        sqlite = SQLiteDatabse()
        prior_probs = sqlite.get_prior_probs()
        words = preprocess_email(email.email)
        cond_probs = sqlite.get_cond_probs(words)
    except Exception as e:
        logger.exception(e)
    finally:
        sqlite.close()

    prob_ham = prior_probs[0]
    prob_spam = prior_probs[1]
    for word in words:
        if word in cond_probs:
            ham_prob, spam_prob = cond_probs[word]
            prob_ham *= ham_prob
            prob_spam *= spam_prob
    if prob_ham > prob_spam:
        return {"class": "non-spam"}
    else:
        return {"class": "spam"}
