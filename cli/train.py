import click
import random
from collections import Counter, defaultdict
from utils.logger_utils import get_logger
from utils.csv_utils import read_csv
from utils.email_utils import preprocess_email
from database.sqlite import SQLiteDatabse

logger = get_logger('Training')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-d', '--dataset', type=str, help='Path to dataset for training.')
@click.option('-p', '--test-percentage', type=float, help='Percentage of data will be used for testing.')
def train(dataset: str, test_percentage: float):
    if not test_percentage:
        test_percentage = 0.1

    db = SQLiteDatabse('knowledge.db')
    emails = []
    labels = []

    '''Preprocess the emails using the bag of words model'''
    logger.info('Handling csv file. . .')
    with open(dataset, 'r') as csv_file:
        for row in read_csv(csv_file):
            label_number = int(row[3])
            email = preprocess_email(row[2])
            labels.append(label_number)
            emails.append(email)

    # Create a vocabulary of all the words in the emails
    vocab = set()
    for email in emails:
        vocab.update(email)

    '''Split the dataset into a training set and a test set'''
    logger.info('Splitting dataset into train and test. . .')
    num_emails = len(emails)
    indices = list(range(num_emails))
    random.shuffle(indices)

    num_test_emails = int(num_emails * test_percentage)
    train_indices = indices[num_test_emails:]
    test_indices = indices[:num_test_emails]

    train_emails = [emails[i] for i in train_indices]
    train_labels = [labels[i] for i in train_indices]

    test_emails = [emails[i] for i in test_indices]
    test_labels = [labels[i] for i in test_indices]

    '''Train the classifier by calculating the prior probabilities and the conditional probabilities of the words'''
    logger.info('Training the classifier. . .')
    # calculate the prior probability of each email
    prior_probs = defaultdict(float)
    for label in labels:
        prior_probs[label] += 1.0
    for label in prior_probs:
        prior_probs[label] /= len(labels)

    # calculate the conditional probability of each word given each email
    cond_probs = defaultdict(lambda: defaultdict(float))
    for i in range(len(train_emails)):
        label = train_labels[i]
        email = train_emails[i]
        word_counts = Counter(email)
        for word in vocab:
            cond_probs[word][label] += word_counts[word]
    for word in cond_probs:
        for label in cond_probs[word]:
            cond_probs[word][label] += 0.1
            cond_probs[word][label] /= len(train_emails)
    # Insert knowledge into sqlite
    try:
        db.create_tables()
        db.insert_knowledge(prior_probs, cond_probs)
    except Exception as e:
        logger.exception(e)
    finally:
        db.close()

    '''classify the test emails using bayes' theorem'''
    logger.info('Training done! Start testing test emails')
    predictions = []
    for i in range(len(test_emails)):
        email = test_emails[i]
        prediction = 0
        max_posterior_prob = 0
        for label in [0, 1]:
            posterior_prob = prior_probs[label]
            for word in email:
                posterior_prob *= cond_probs[word][label]
            if posterior_prob > max_posterior_prob:
                max_posterior_prob = posterior_prob
                prediction = label
        predictions.append(prediction)

    '''evaluate the performance of the classifier'''
    num_correct = 0
    for i in range(len(test_emails)):
        if predictions[i] == test_labels[i]:
            num_correct += 1
    accuracy = round(num_correct / len(test_emails) * 100, 2)
    logger.info(f'Accuracy: {accuracy}%')
