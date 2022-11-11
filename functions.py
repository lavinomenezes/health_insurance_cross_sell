import pandas as pd


def precision_at_k( data, k=2000 ):
    """
    Object that return the precision at k  of recommended items in the top-k set that are relevant
    :param data: dataframe that will be calculated the precision at k position
    :param k: int, default=2000, position that the metric will be calculated default='2000'
    :return: a float value
    """
    # reset index
    data = data.reset_index( drop=True )

    # create ranking order
    data['ranking'] = data.index + 1

    data['precision_at_k'] = data['response'].cumsum() / data['ranking']

    return data.loc[k, 'precision_at_k']


def recall_at_k( data, k=2000 ):
    """
    Object that return the recall at k  of recommended items in the top-k set that are relevant
    :param data: dataframe that will be calculated the recall at k position
    :param k: int, default=2000, position that the metric will be calculated default='2000'
    :return: a float value
    """
    # reset index
    data = data.reset_index( drop=True )

    # create ranking order
    data['ranking'] = data.index + 1

    data['recall_at_k'] = data['response'].cumsum() / data['response'].sum()

    return data.loc[k, 'recall_at_k']


def performace(model_name, data, y_val, yhat_class, k=2000):
    """

    :param model_name: string, with the name of the algoritm that will be used
    :param data: dataframe sorted by  probabilit given to each iten by the model
    :param y_val: list of the target variable of the dataframe
    :param yhat_class: binary prediction made by the model for each iten
    :param k: int, default=2000 position that the metric will be calculated default='2000'
    :return: a dataframe with the metrics: [precision,recall, balanced accuracy, precision at k, recall at k]
    """
    import sklearn.metrics
    prec = sklearn.metrics.precision_score(y_val, yhat_class)
    recal = sklearn.metrics.recall_score(y_val, yhat_class)
    balanced_acc = sklearn.metrics.balanced_accuracy_score(y_val, yhat_class)
    recal_k = recall_at_k(data, k)
    prec_k = precision_at_k(data, k)

    return pd.DataFrame({'Model Name': model_name,
                         'Precison': prec,
                         'Recall': recal,
                         'Balanced_acc': balanced_acc,
                         'k': k,
                         'Precison at k': prec_k,
                         'Recall at k': recal_k}, index=[0])


def performace_cross_val(data, target, model, model_name, round_n=5, splits=5, shuffle_n=True, random=42, k=2000):
    """
    this cross-validation object uses kfold with stratified folds and return the metrics
    :param data: dataframe
    :param target: string, name of the target variable
    :param model: model that will be used
    :param model_name: string with the model name
    :param round_n: int, default=5number of decimal points of the float values that will be returned
    :param splits: int, default=5, number of folds
    :param shuffle_n:bool, default=True, Whether to shuffle each class’s samples before splitting into batches
    :param random: int, default=42 controls the randomness of each fold
    :param k: int, default=2000 position that the metric will be calculated default='2000'
    :return: a dataframe with the mean and standard deviation of the metrics: [precision,recall, balanced accuracy, precision at k, recall at k]
    """
    import sklearn.model_selection as ms
    import sklearn.metrics
    import numpy as np
    skf = ms.StratifiedKFold(n_splits=splits, shuffle=shuffle_n, random_state=random)
    X = data
    y = X[target]
    X = X.drop(columns=[target, 'id'])
    precision = []
    recall = []
    balan_acc = []
    prec_k = []
    rec_k = []
    for train_index, test_index in skf.split(X, y):
        # train the model
        model.fit(X.iloc[train_index], y.iloc[train_index].values.ravel())

        # predict the classification
        yhat_class = model.predict(X.iloc[test_index])

        # predict the probabilit
        yhat_proba = model.predict_proba(X.iloc[test_index])

        # precision and recall
        prec = sklearn.metrics.precision_score(y.iloc[test_index], yhat_class)
        rec = sklearn.metrics.recall_score(y.iloc[test_index], yhat_class)
        balan_acc_score = sklearn.metrics.balanced_accuracy_score(y.iloc[test_index], yhat_class)
        precision.append(prec)
        recall.append(rec)
        balan_acc.append(balan_acc_score)

        # sort the test dataframe by the probabiliti score of the model
        aux = X.iloc[test_index]
        aux[target] = y.iloc[test_index]
        aux['score'] = yhat_proba[:, 1].tolist()

        # sorte by score
        aux = aux.sort_values('score', ascending=False)

        # precision and recall at k
        prec_k.append(precision_at_k(aux, k))
        rec_k.append(recall_at_k(aux, k))

    # return a dataset with the metrics
    return pd.DataFrame({'Model name': model_name + " Cross_Val",
                         'PRECISION_CROSS_VAL': np.round(np.mean(precision), round_n),
                         'PRECISON_STD': np.round(np.std(precision), round_n),
                         'RECALL_CROSS_VAL': np.round(np.mean(recall), round_n),
                         'RECALL_STD': np.round(np.std(recall), round_n),
                         'BALANCED_ACC_CROSS_VALL': np.round(np.mean(balan_acc), round_n),
                         'BALANCED_ACC_STD': np.round(np.std(balan_acc), round_n),
                         'K': k,
                         'PRECISION_AT_K_CROSS_VAL': np.round(np.mean(prec_k), round_n),
                         'PRECISION_AT_K_STD': np.round(np.std(prec_k), round_n),
                         'RECALL_AT_K_CROSS_VAL': np.round(np.mean(rec_k), round_n),
                         'RECALL_AT_K_STD': np.round(np.std(rec_k))}, index=[0])


def balanced_performace_cross_val(data, target, model, model_name, round_n=5, splits=5, shuffle_n=True, random=42,
                                  k=2000,sampling_strategy=0.8):
    """
    this cross-validation object uses kfold with stratified folds and SMOTE plus ENN technique to balance teh dataset and return the metrics
    :param data: dataframe
    :param target: string, name of the target variable
    :param model: model that will be used
    :param model_name: string with the model name
    :param round_n: int, default=5number of decimal points of the float values that will be returned
    :param splits: int, default=5, number of folds
    :param shuffle_n:bool, default=True, whether to shuffle each class’s samples before splitting into batches
    :param random: int, default=42 controls the randomness of each fold
    :param k: int, default=2000 position that the metric will be calculated default='2000'
    :param sampling_strategy float, default = 0.8, sampling information to resample the data set.
    :return: a dataframe with the mean and standard deviation of the metrics: [precision,recall, balanced accuracy, precision at k, recall at k]
    """

    import sklearn.model_selection as ms
    import sklearn.metrics
    import numpy as np
    from imblearn.over_sampling import SMOTE
    from imblearn.combine import SMOTEENN
    skf = ms.StratifiedKFold(n_splits=splits, shuffle=shuffle_n, random_state=random)
    X = data
    y = X[target]
    X = X.drop(columns=[target, 'id'])
    precision = []
    recall = []
    balan_acc = []
    prec_k = []
    rec_k = []
    for train_index, test_index in skf.split(X, y):
        # train kfold balance
        X_train_kfold, y_train_kfold = X.iloc[train_index], y.iloc[train_index]
        X_test_kfold, y_test_kfold = X.iloc[test_index], y.iloc[test_index]

        smtenn = SMOTEENN(smote=SMOTE(random_state=random, sampling_strategy=sampling_strategy), random_state=random)
        X_train_balanced, y_train_balanced = smtenn.fit_resample(X_train_kfold, y_train_kfold)

        # model balancing training
        model.fit(X_train_balanced, y_train_balanced.values.ravel())

        # predict the classification
        yhat_class = model.predict(X_test_kfold)

        # predict the probabilit
        yhat_proba = model.predict_proba(X_test_kfold)

        # precision and recall
        prec = sklearn.metrics.precision_score(y_test_kfold, yhat_class)
        rec = sklearn.metrics.recall_score(y_test_kfold, yhat_class)
        balan_acc_score = sklearn.metrics.balanced_accuracy_score(y_test_kfold, yhat_class)
        precision.append(prec)
        recall.append(rec)
        balan_acc.append(balan_acc_score)

        # sort the test dataframe by the probabiliti score of the model
        aux = X_test_kfold
        aux[target] = y_test_kfold
        aux['score'] = yhat_proba[:, 1].tolist()

        # sorte by score
        aux = aux.sort_values('score', ascending=False)

        # precision and recall at k
        prec_k.append(precision_at_k(aux, k))
        rec_k.append(recall_at_k(aux, k))

    # return a dataset with the metrics
    return pd.DataFrame({'Model name': model_name + " Cross_Val",
                         'PRECISION_CROSS_VAL': np.round(np.mean(precision), round_n),
                         'PRECISON_STD': np.round(np.std(precision), round_n),
                         'RECALL_CROSS_VAL': np.round(np.mean(recall), round_n),
                         'RECALL_STD': np.round(np.std(recall), round_n),
                         'BALANCED_ACC_CROSS_VALL': np.round(np.mean(balan_acc), round_n),
                         'BALANCED_ACC_STD': np.round(np.std(balan_acc), round_n),
                         'K': k,
                         'PRECISION AT K CROSS_VAL': np.round(np.mean(prec_k), round_n),
                         'PRECISION AT K STD': np.round(np.std(prec_k), round_n),
                         'RECALL AT K CROSS_VAL': np.round(np.mean(rec_k), round_n),
                         'RECALL AT K STD': np.round(np.std(rec_k))}, index=[0])