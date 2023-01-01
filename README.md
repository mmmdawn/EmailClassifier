# Email Classifier


## Prerequisites
```python3``` version 3.8+.

## Installing
First, clone this repository:  
```
git clone https://github.com/mmmdawn/EmailClassifier.git
```

Create virtual environment:  
```
python3 -m venv venv
```

Activate environment:
```
source venv/bin/activate 
```

Install dependencies:  
```
pip install -r requirements.txt
```

## Usage
### Train the classifier
Move to root directory of the project, make sure that environment is activated. To train the classifier:
```
python3 run.py train --dataset data/spam_ham_dataset.csv --test-percentage 0.2
```
Above command runs classifier training task with the input dataset and uses 20% of the dataset for testing.

### Test the classifier
Start the server:
```
python3 run.py start_server
```
You can test the classifier at `http://localhost:8000/static/index.html`
