"""
Contains data preparation for more accurate prediction.
Author: Emilija Zdilar 15-06-2018
"""
import copy
import pandas as pd

# loading training and test data
data_url = "Input/training_data.csv"
train = pd.read_csv(data_url)
# data1_url = "Input/test_data.csv"
# test = pd.read_csv(data1_url)
test = pd.read_csv("Input/cross_validation_dataset.csv")


# calculating the weight
time_min = train["Month #"].min()
time_max = train["Month #"].max()
no_of_players = train["White Player #"].max()
train["Weight"] = ((1 + train["Month #"] - time_min) / (1 + time_max - time_min)) ** 2

# find neighbours for each of the players
pairs_of_opponents = train.as_matrix(columns=[train.columns[1], train.columns[2]])
pairs_of_opponents = tuple(map(tuple, pairs_of_opponents))
neighbourhood = []
sublist = []
for i in range(0, no_of_players):
    neighbourhood.append(sublist)
neighbourhood = [copy.copy(x) for x in [[]] * no_of_players]
for i in range(0, len(pairs_of_opponents)):
    neighbourhood[pairs_of_opponents[i][0]-1].append(pairs_of_opponents[i][1])
    neighbourhood[pairs_of_opponents[i][1]-1].append(pairs_of_opponents[i][0])

# calculating the rating
rating = [10 for _ in range(no_of_players)]
for i in range(1, no_of_players+1):
    sum_ = 0
    for j in neighbourhood[i-1]:
        played_as_white = train[["Score", "Weight"]][(train["White Player #"] == i) & (train["Black Player #"] == j)].\
            values.tolist()
        for l in played_as_white:
            rating[i-1] += (l[0] - 0.5) * l[1]

        played_as_black = train[["Score", "Weight"]][(train["White Player #"] == j) & (train["Black Player #"] == i)].\
            values.tolist()
        for l in played_as_black:
            rating[i-1] += - (l[0] - 0.5) * l[1]
        pass

train["ri"] = [float(rating[i-1]) for i in train["White Player #"].values.tolist()]
train["rj"] = [float(rating[i-1]) for i in train["Black Player #"].values.tolist()]
test["ri"] = [float(rating[i-1]) for i in test["White Player #"].values.tolist()]
test["rj"] = [float(rating[i-1]) for i in test["Black Player #"].values.tolist()]

train.to_csv("train_rating.csv")
test.to_csv("test_rating.csv")
