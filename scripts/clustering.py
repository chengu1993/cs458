import pandas as pd
from sklearn.cluster import KMeans
from sklearn import tree

def cluster():
    X = pd.read_csv('../training/rest_data.csv', low_memory=False)

    kmeans_model = KMeans(n_clusters=5, random_state=1).fit(X)
    label = kmeans_model.labels_
    print(label)
    for idx in range(len(label)):
        X.loc[idx, 'label'] = label[idx]
    X.to_csv('out.csv')

def decision_tree():
    X = pd.read_csv('../training/rest_data.csv', low_memory=False)
    target = pd.read_csv('../training/rest_label.csv', low_memory=False)['label']
    tree_model = tree.DecisionTreeClassifier()
    tree_model = tree_model.fit(X, target)




cluster()


