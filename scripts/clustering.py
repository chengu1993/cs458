import operator
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
    for idx in range(len(label)):
        X.loc[idx, 'label'] = label[idx]
    X.to_csv('user_label.csv')


def decision_tree():
    X = pd.read_csv('../training/user_data.csv', low_memory=False)
    target = pd.read_csv('../training/user_label.csv', low_memory=False)['label']
    tree_model = tree.DecisionTreeClassifier()
    tree_model = tree_model.fit(X, target)
    tree_graph = tree.export_graphviz(tree_model, out_file=None,
                                    feature_names=list(X.columns.values),
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(tree_graph)
    graph.write_pdf('user_decision_tree.pdf')

def classify(user_data):
    X = pd.read_csv('../training/user_data.csv', low_memory=False)
    target = pd.read_csv('../training/user_label.csv', low_memory=False)['label']
    tree_model = tree.DecisionTreeClassifier()
    tree_model = tree_model.fit(X, target)

    ratings = pd.read_csv('../dataset/food_ratingfinal.csv', low_memory=False)
    label = tree_model.predict(user_data)

    rating_map = {}
    X = pd.read_csv('../dataset/user_label.csv', low_memory=False)
    for index, row in X.iterrows():
        group = row['label']
        if group != label: continue
        user_id = row['userID']
        user_ratings = ratings.loc[(ratings['userID'] == user_id)]
        for idx, r in user_ratings.iterrows():
            placeID = r['placeID']
            rating = r['rating']
            food_rating = r['food_rating']
            service_rating = r['service_rating']
            if placeID not in rating_map:
                rating_map[placeID] = 0
            rating_map[placeID] += rating + food_rating + service_rating
    sorted_rating = sorted(rating_map.items(), key=operator.itemgetter(1), reverse=True)
    recommend = []
    for item in sorted_rating:
        recommend.append(item[0])
    return recommend


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




# user_cluster()
# rest_cluster()
# decision_tree()
classify([[0, 0, 0, 0, 1989, 0, 0, 0, 0]])


