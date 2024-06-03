import polars as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_date_columns(df):
    columns=[]
    for col in df.columns:
        if(df[col].dtype==pl.Date):
            columns.append(col)
    return columns

class NotCategoricalError(Exception):
    """Exception raised for non-categorical columns."""

    def __init__(self, column):
        self.column = column
        super().__init__(f"{column} is not a categorical column.")
def classify_cols(df,cat_features,decide_factor=10):
    oneHot_cols = []
    ord_cols = []
    
    # Check if num_cols is not empty
    if cat_features:
        for col in cat_features:
            # Check if the column dtype is string
            if df[col].dtype == pl.String:
                unique_count = df[col].unique().shape[0]
                if unique_count <= decide_factor:
                    oneHot_cols.append(col)
                else:
                    ord_cols.append(col)
            else:
                raise NotCategoricalError(col)
        return oneHot_cols,ord_cols
    
    else:
        raise ValueError("No columns provided to classify.")
def categorical_hist_plot(df, cat_features, target_col):
    for col in cat_features:
        fig, axes = plt.subplots(1, figsize=(18, 6))

        # Count Plot with hue
        sns.countplot(data=df, x=col, hue=target_col, ax=axes)
        axes.set_title(f'Bar Plot for {col}')
        axes.tick_params(axis='x', rotation=45)
        
        # Add percentage annotations on top of bars
        total = len(df[col])
        for p in axes.patches:
            height = p.get_height()
            axes.text(p.get_x() + p.get_width() / 2.,
                        height + 3,
                        '{:1.2f}%'.format((height / total) * 100),
                        ha="center")

        plt.tight_layout()
        plt.show()
def categorical_violin_plot(df, cat_features, target_col):
    for col in cat_features:
        fig, axes = plt.subplots(1, figsize=(18, 6))

        # Count Plot with hue
        sns.violinplot(data=df, x=col, y=target_col, ax=axes)
        axes.set_title(f'Bar Plot for {col}')
        axes.tick_params(axis='x', rotation=45)
        
        # Add percentage annotations on top of bars
        total = len(df[col])
        for p in axes.patches:
            height = p.get_height()
            axes.text(p.get_x() + p.get_width() / 2.,
                        height + 3,
                        '{:1.2f}%'.format((height / total) * 100),
                        ha="center")

        plt.tight_layout()
        plt.show()
def categorical_box_plot(df, cat_features, target_col):
    for col in cat_features:
        fig, axes = plt.subplots(1, figsize=(18, 6))

        # Count Plot with hue
        sns.boxplot(data=df, x=col, y=target_col, ax=axes)
        axes.set_title(f'Bar Plot for {col}')
        axes.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
def categorical_pie_plot(df, cat_features):
    for col in cat_features:
        
        fig, axes = plt.subplots(1, figsize=(18, 6))

        # Create pie chart
        df[col].plot(kind='pie', subplots=True, ax=axes, autopct='%1.1f%%', startangle=90)
        
        axes.set_title(f'Pie Chart for {col}')
        axes.set_ylabel('')
        
        plt.tight_layout()
        plt.show()
def remove_single_value_cols(df,cat_features):
    for col in cat_features:
        unique_values = df[col].drop_nulls().unique()
        
        # Check if the column has only one unique value and the rest are null
        if len(unique_values) == 1:
            df=df.drop(col)
    
    return df

from scipy.stats import ttest_ind

def perform_ttest(data, column, category1, category2,target_col, alpha=0.05):
    # Filter data for each category

    category1_data=data.filter(data[column]==category1)[target_col]
    category2_data=data.filter(data[column]==category2)[target_col]
    # Perform t-test
    t_stat, p_value = ttest_ind(category1_data, category2_data, equal_var=False)
    
    # Interpretation
    if p_value < alpha:
        print(f'T-statistic: {t_stat}')
        print(f'P-value: {p_value}')
        print(f"There is a significant difference in {target_col} between {category1} and {category2} for column '{column}'.")
    else:
        print(f'T-statistic: {t_stat}')
        print(f'P-value: {p_value}')
        print(f"There is no significant difference in {target_col} between {category1} and {category2} for column '{column}'.")


def compute_z_scores(data, columns,threshold=3):
    for column in columns:
        mean = data[column].mean()
        std_dev = data[column].std()
        z_score_column = ((data[column] - mean) / std_dev).alias(f"{column}_zscore")
        data = data.with_columns(z_score_column)

    for column in columns:
        z_score_column = f"{column}_zscore"
        data = data.filter(data[z_score_column].abs() < threshold)

    data = data.drop([f"{column}_zscore" for column in columns])
    return data

from scipy.stats import kruskal
def perform_non_normal_kruskal_hypothesis(data,cat_cols,group_col,alpha=0.05):
    for i in cat_cols:
        groups = [group[group_col].values for name, group in data.to_pandas().groupby(i)]

        # Perform Kruskal-Wallis test
        stat, p_value = kruskal(*groups)
        print(f'Kruskal-Wallis H-statistic: {stat} P-value: {p_value}')

        # Interpretation
        if p_value < alpha:
            print(f"There is a significant difference in {group_col} between different {i} categories.\n")
        else:
            print(f"There is no significant difference in {group_col} between different {i} categories.\n")
