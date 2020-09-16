from sklearn.svm import SVC
from os import listdir
from os.path import isfile, join, splitext, split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Binarizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB

def confusion_matrix_heatmap(cm, index):
    cmdf = pd.DataFrame(cm, index = index, columns=index)
    dims = (5, 5)
    fig, ax = plt.subplots(figsize=dims)
    sns.heatmap(cmdf, annot=True, cmap="coolwarm", center=0)
    ax.set_ylabel('Actual')    
    ax.set_xlabel('Predicted')
    
def list_files(folder):
    textfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".txt")]
    return textfiles
    
f_files = list_files("celebs-gb/female")
m_files = list_files("celebs-gb/male")
X = f_files + m_files 
y = ["female"] * len(f_files) + ["male"] * len(m_files)
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state = 0, stratify=y)

def custom_tokenise_2(text):
    seq_punc = "[^\w\s]{2,}" #sequences of punctuation
    hyphen = "[-\w]+"
    apos = "[\w]+['’`][\w]+"
    money = "[$£]\S+"
    leftover = "\w+" #no emojis, no special symbols
    patterns = (apos, money, hyphen, seq_punc, leftover)
    joint_patterns = '|'.join(patterns)
    p = re.compile(r'(?:{})'.format(joint_patterns)) 
    return p.findall(text)

test_model = Pipeline([
    ('vectorizer', CountVectorizer(input='filename', max_features=500)), #ngram_range=(1,2))), #tokenizer=custom_tokenise, preprocessor=preprocess)),
    ('selector', SelectKBest(score_func=chi2)),
    ('norm',Binarizer()),
    ('norm2',TfidfTransformer(norm=None)),
    ('clf', None),
])
n_jobs=-1
search = GridSearchCV(test_model, cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=123),
                      return_train_score=False,
                      scoring=['accuracy','precision_weighted','recall_weighted','f1_weighted'],
                      refit='f1_weighted',
                      param_grid={
                          'vectorizer__tokenizer':['custom_tokenise','nltk_twitter_tokenise'],
                          'vectorizer__ngram_range':[(1,1),(1,2)],
                          'selector__k':[10,50,100,500],
                          'vectorizer__analyzer':['word','char'],
                          'clf': [MultinomialNB(alpha=0.8),
                                  MultinomialNB(),
                                  LogisticRegression(solver='liblinear', random_state=1),
                                  LogisticRegression(solver='newton-cg', class_weight='balanced', random_state=1),
                                  SVC(C=0.8), 
                                  SVC(C=0.5)],
                      }
                     )
                     
                     
search.fit(X_train, y_train)
search.best_estimator_
pd.DataFrame(search.cv_results_)
predictions = search.predict(X_test)

print("Accuracy: ", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))

confusion_matrix_heatmap(confusion_matrix(y_test,predictions), search.classes_)
ftest_files = list_files("test/female")
mtest_files = list_files("test/male")
Xtest_new = ftest_files + mtest_files
ytest_new = ["female"] * len(ftest_files) + ["male"] * len(mtest_files)
print(len(Xtest_new), len(ytest_new))
print('-------------------------------')

predictions_new = search.predict(Xtest_new)
print("Accuracy: ", accuracy_score(ytest_new, predictions_new))
print(classification_report(ytest_new, predictions_new))
print(confusion_matrix(ytest_new, predictions_new))

confusion_matrix_heatmap(confusion_matrix(ytest_new,predictions_new), search.classes_)
