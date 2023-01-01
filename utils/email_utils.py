import re
from constants.word_constants import stop_words


def preprocess_email(email: str):
    email = re.sub('[^a-zA-Z\n]', ' ', email)
    email = re.sub('\s+', ' ', email)
    email = email.lower().split()
    email_words = [word for word in email if word not in stop_words]
    return email_words
