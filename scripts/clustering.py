import pandas as pd
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.neighbors import NearestNeighbors
import pydotplus

def rest_cluster():
    X = pd.read_csv('../training/rest_data.csv', low_memory=False)

    kmeans_model = KMeans(n_clusters=5, random_state=1).fit(X)
    label = kmeans_model.labels_
    print(label)
    for idx in range(len(label)):
        X.loc[idx, 'label'] = label[idx]
    X.to_csv('rest_label.csv')


def user_cluster():
    X = pd.read_csv('../training/user_data.csv', low_memory=False)

    kmeans_model = KMeans(n_clusters=5, random_state=1).fit(X)
    label = kmeans_model.labels_
    print(label)
    for idx in range(len(label)):
        X.loc[idx, 'label'] = label[idx]
    X.to_csv('user_label.csv')



def decision_tree():
    X = pd.read_csv('../training/rest_data.csv', low_memory=False)
    target = pd.read_csv('../training/rest_label.csv', low_memory=False)['label']
    tree_model = tree.DecisionTreeClassifier()
    tree_model = tree_model.fit(X, target)

    tree_graph = tree.export_graphviz(tree_model, out_file=None,
                                    feature_names=list(X.columns.values),
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(tree_graph)
    graph.write_pdf('decision_tree.pdf')

def rest_knn(rest_data, k=3):
    X = pd.read_csv('../training/rest_data.csv', low_memory=False)
    neigh_model = NearestNeighbors(n_neighbors=k).fit(X)
    neighbors = neigh_model.kneighbors(rest_data)
    print(neighbors)

def user_knn(user_data, k=3):
    X = pd.read_csv('../training/user_data.csv', low_memory=False)
    neigh_model = NearestNeighbors(n_neighbors=k).fit(X)
    neighbors = neigh_model.kneighbors(user_data)
    print(neighbors)




user_cluster()
# rest_cluster()
# decision_tree()


