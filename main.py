"""
Contains solution to Elo vs the rest of the world problem.
Author: Emilija Zdilar 15-06-2018
"""
import pandas as pd
from numpy.ma import array
from sklearn import tree
from matplotlib import pyplot as plt


def main() -> None:
    """
    Elo versus the rest of the world. First, the training and test data is loaded.
    New Score column is added to the test data. The next step is fitting the model
    and choosing features.The next step would be  predicting. A RMSE is calculated.
    I also plotted the difference between actual and predicted scores.

    Returns: None
    """

    # loading training and test data
    train_url = "train_rating.csv"
    train = pd.read_csv(train_url)

    test = pd.read_csv("test_rating.csv")
    test_one = test.copy()
    test["Score"] = float("NaN")

    # fitting the model
    target = train["Score"].values
    train_features = train[["ri", "rj"]].values
    max_depth = 10
    min_samples_split = 5
    my_tree_one = tree.DecisionTreeRegressor(max_depth=max_depth, min_samples_split=min_samples_split, random_state=1)
    my_tree_one = my_tree_one.fit(train_features, target)

    # choice of features
    test_features = test[["ri", "rj"]].values

    # predicting
    my_prediction = my_tree_one.predict(test_features)
    my_solution = pd.DataFrame(my_prediction, columns=["Score"])

    my_solution["Score"][my_solution["Score"] <= 0.33] = 0.0
    my_solution["Score"][my_solution["Score"] >= 0.65] = 1.0
    my_solution["Score"][(my_solution["Score"] > 0.33) & (my_solution["Score"] < 0.65)] = 0.5

    # calculating root mean square error
    error = pd.DataFrame()
    my_solution = my_solution.reset_index()
    test_one = test_one.reset_index()
    error["Square Error"] = abs(my_solution["Score"] - test_one["Score"])**2
    score = (float(error["Square Error"].sum()) / float(error["Square Error"].count()))**0.5

    print(score)

    my_solution.to_csv("Zdilar_Emilija_Solution.csv")

    # plotting result
    plot_error = pd.DataFrame()
    plot_error["White"] = test_one["ri"]
    plot_error["Black"] = test_one["rj"]
    plot_error["Score"] = test_one["Score"]
    plot_error["Prediction"] = my_solution["Score"]
    
    points = plot_error.as_matrix(columns=[plot_error.columns[0], plot_error.columns[1], plot_error.columns[2],
                                           plot_error.columns[3]])
    points = list(map(list, points))
    data_ = array(points)
    
    x_s = data_[:, 0]
    y_s = data_[:, 1]
    z_s = data_[:, 2]
    z_s_1 = data_[:, 3]
    fig = plt.figure()
    from mpl_toolkits.mplot3d import Axes3D
    ax = Axes3D(fig)
    
    ax.scatter(x_s, y_s, z_s, c='g', label='Actual Score', alpha=0.1)
    ax.scatter(x_s, y_s, z_s_1, c='b', label='Predicted Score', alpha=0.1)
    
    plt.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    main()
