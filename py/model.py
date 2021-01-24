import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn.metrics import r2_score, mean_squared_error

"""
1. get_Xy(df): Separate features and target variable
2. get_score(X_train,X_val,y_train,y_val)
3. categorical(X_train,X_val,X_test,cat_variable)

"""

def get_Xy(df):
    
    df = df.dropna()
    
    target = 'opening_weekend_usa'
    all_column = df.columns.values.tolist()
    all_column.remove(target)

    y = df[target]
    
    X = df[all_column]
    
    return X, y


def get_score(X_train,X_val,y_train,y_val):
    
    # fit linear regression to training data
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred = lr_model.predict(X_val)
    
    # score fit model on validation data
    train_score = lr_model.score(X_train, y_train)
    val_score = lr_model.score(X_val, y_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    
    
    # report results
    print('\nTrain R^2 score was:', train_score)
    print('Validation R^2 score was:', val_score)
    print(f'RMSE: {rmse:.2f} \n')

    # print('Feature coefficient results:')
    # for feature, coef in zip(X.columns, lr_model.coef_):
    #     print(feature, ':', f'{coef:.2f}')
        
    
    # Visualization
    fig, ax = plt.subplots(1, 1)
    plt.scatter(y_val, y_pred, alpha=0.4)

    ax.set_xlabel('Opening weekend revenue ($ in millions)',fontsize=20)
    ax.set_ylabel('Prediction ($ in millions)',fontsize=20)
    ax.set_title('R$^2$: %0.2f' % val_score, fontsize=20)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)


    x=np.linspace(0,0.7e2,50)
#     x=np.linspace(4,9,50)
    
    y=x
    plt.plot(x,y,color='firebrick',linewidth=3,alpha=0.6)
    plt.ylim(0,)
    plt.xlim(0,)
    return fig, lr_model, y_pred



def categorical_multilabel(X_train,X_val,X_test,cat_variable):

    """
    Input: X_train,X_val,X_test,categorical_variable
    Processing: preprocessing the three sets separately:
    1. Separate continuous and categorical variable
    2. Scaling + polynomial fit the conitnuous variables and get_dummies on the categorical variable
    3. Combine back the continuous and categorical data
    Return: tranformed X_train, X_val, X_test
    """

    
    scaler = StandardScaler()
    poly = PolynomialFeatures(degree=2,interaction_only = False)
    
    # Train set
    # Convert genre to dummies
    X_train_genre = X_train[cat_variable].str.join(sep='*').str.get_dummies(sep='*')
    known_columns = X_train_genre.columns

    # Scaling continuous variables
    X_train_con = X_train[con_feature]
    X_train_con_scaled = scaler.fit_transform(X_train_con)
    X_train_con_scaled_df = pd.DataFrame(X_train_con_scaled, columns=X_train_con.columns, index=X_train_con.index)

    X_train_poly = poly.fit_transform(X_train_con_scaled)
    X_train_poly_df = pd.DataFrame(X_train_poly, columns=poly.get_feature_names(X_train_con.columns), index=X_train_con.index)

    #Combine
#     X_train = pd.concat([X_train_genre,X_train_con_scaled_df],axis=1)
    X_train = pd.concat([X_train_genre,X_train_poly_df],axis=1)



    # Val set
    # Convert genre to dummies
    X_val_genre = X_val[cat_variable].str.join(sep='*').str.get_dummies(sep='*')
    val_columns = X_val_genre.columns
    X_val_genre = X_val_genre[[x for x in val_columns if x in known_columns]]
    fill_dict = { c : 0 for c in [x for x in known_columns if x not in val_columns] }
    X_val_genre = X_val_genre.assign(**fill_dict)

    # Scaling continuous variables
    X_val_con = X_val[con_feature]
    X_val_con_scaled = scaler.transform(X_val_con)
    X_val_con_scaled_df = pd.DataFrame(X_val_con_scaled, columns=X_val_con.columns, index=X_val_con.index)

    X_val_poly = poly.transform(X_val_con_scaled)
    X_val_poly_df = pd.DataFrame(X_val_poly, columns=poly.get_feature_names(X_val_con.columns), index=X_val_con.index)

    #Combine
#     X_val = pd.concat([X_val_genre,X_val_con_scaled_df],axis=1)
    X_val = pd.concat([X_val_genre,X_val_poly_df],axis=1)


    
    # Test set
    # Convert genre to dummies
    X_test_genre = X_test[cat_variable].str.join(sep='*').str.get_dummies(sep='*')
    test_columns = X_test.columns
    X_test_genre = X_test_genre[[x for x in test_columns if x in known_columns]]
    fill_dict = { c : 0 for c in [x for x in known_columns if x not in test_columns] }
    X_test_genre = X_test_genre.assign(**fill_dict)


    # Scaling continuous variables
    X_test_con = X_test[con_feature]
    X_test_con_scaled = scaler.transform(X_test_con)
    X_test_con_scaled_df = pd.DataFrame(X_test_con_scaled, columns=X_test_con.columns, index=X_test_con.index)
    
    X_test_poly = poly.transform(X_test_con_scaled)
    X_test_poly_df = pd.DataFrame(X_test_poly, columns=poly.get_feature_names(X_test_con.columns), index=X_test_con.index)

    #Combine
#     X_test = pd.concat([X_test_genre,X_test_con_scaled_df],axis=1)
    X_test = pd.concat([X_test_genre,X_test_poly_df],axis=1)
    
    return X_train,X_val,X_test



def categorical_singlelabel(X_train,X_val,X_test,cat_variable):

    """
    Input: X_train,X_val,X_test,categorical_variable
    Processing: preprocessing the three sets separately:
    1. Separate continuous and categorical variable
    2. Scaling + polynomial fit the conitnuous variables and get_dummies on the categorical variable
    3. Combine back the continuous and categorical data
    Return: tranformed X_train, X_val, X_test
    """

    
    scaler = StandardScaler()
    poly = PolynomialFeatures(degree=2,interaction_only = False)
    
    # Train set
    # Convert genre to dummies
    X_train_genre = pd.get_dummies(X_train[cat_variable])
    known_columns = X_train_genre.columns

    # Scaling continuous variables
    X_train_con = X_train[con_feature]
    X_train_con_scaled = scaler.fit_transform(X_train_con)
    X_train_con_scaled_df = pd.DataFrame(X_train_con_scaled, columns=X_train_con.columns, index=X_train_con.index)

    X_train_poly = poly.fit_transform(X_train_con_scaled)
    X_train_poly_df = pd.DataFrame(X_train_poly, columns=poly.get_feature_names(X_train_con.columns), index=X_train_con.index)

    #Combine
    X_train = pd.concat([X_train_genre,X_train_con_scaled_df],axis=1)
    # X_train = pd.concat([X_train_genre,X_train_poly_df],axis=1)



    # Val set
    # Convert genre to dummies
    X_val_genre = pd.get_dummies(X_val[cat_variable])
    val_columns = X_val_genre.columns
    X_val_genre = X_val_genre[[x for x in val_columns if x in known_columns]]
    fill_dict = { c : 0 for c in [x for x in known_columns if x not in val_columns] }
    X_val_genre = X_val_genre.assign(**fill_dict)

    # Scaling continuous variables
    X_val_con = X_val[con_feature]
    X_val_con_scaled = scaler.transform(X_val_con)
    X_val_con_scaled_df = pd.DataFrame(X_val_con_scaled, columns=X_val_con.columns, index=X_val_con.index)

    X_val_poly = poly.transform(X_val_con_scaled)
    X_val_poly_df = pd.DataFrame(X_val_poly, columns=poly.get_feature_names(X_val_con.columns), index=X_val_con.index)

    #Combine
    X_val = pd.concat([X_val_genre,X_val_con_scaled_df],axis=1)
    # X_val = pd.concat([X_val_genre,X_val_poly_df],axis=1)


    
    # Test set
    # Convert genre to dummies
    X_test_genre = pd.get_dummies(X_test[cat_variable])
    test_columns = X_test.columns
    X_test_genre = X_test_genre[[x for x in test_columns if x in known_columns]]
    fill_dict = { c : 0 for c in [x for x in known_columns if x not in test_columns] }
    X_test_genre = X_test_genre.assign(**fill_dict)


    # Scaling continuous variables
    X_test_con = X_test[con_feature]
    X_test_con_scaled = scaler.transform(X_test_con)
    X_test_con_scaled_df = pd.DataFrame(X_test_con_scaled, columns=X_test_con.columns, index=X_test_con.index)
    
    X_test_poly = poly.transform(X_test_con_scaled)
    X_test_poly_df = pd.DataFrame(X_test_poly, columns=poly.get_feature_names(X_test_con.columns), index=X_test_con.index)

    #Combine
    X_test = pd.concat([X_test_genre,X_test_con_scaled_df],axis=1)
    # X_test = pd.concat([X_test_genre,X_test_poly_df],axis=1)
    
    return X_train,X_val,X_test


def opt_cat_number(df, cat_variable):
    """
    Decide how many categories to keep for the categorical variable.
    """

    score = []
    for i in range(0,100,1):
        
        df[cat_variable].value_counts()

        top = df[cat_variable].value_counts().index.tolist()[:i]
        discard = list(set(df[cat_variable].unique()).difference(set(top)))

        # The rest will go to "Other"
        df['new_cat_variable'] = df[cat_variable].replace(discard,'Other')

        # Get the data from all_df with both continuous and selected categorical variable
        X, y = get_Xy(df)

        # train_test_split
        X_, X_test, y_, y_test = train_test_split(X, y, test_size=.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_, y_, test_size=.25, random_state=3)

        X_train,X_val,X_test = categorical_singlelabel(X_train,X_val,X_test,'new_cat_variable')


        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        y_pred = lr_model.predict(X_val)
        val_score = lr_model.score(X_val, y_val)
        score.append(round(val_score,3))

    best_score = max(score)
    num = score.index(best_score)

    print('Optimal number of categories to keep is', num)
    print('Best score is', best_score)

    return num, best_score