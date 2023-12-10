# -*- coding: utf-8 -*-
"""python_task_2.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FDdwwej-Uxt59qz72ODCLTHoiAC6JHp2

# python_task_2.py
"""

import pandas as pd
import numpy as np
df=pd.read_csv("/content/dataset-3.csv")

# TASK2- 1
def calculate_distance_matrix(df)->pd.DataFrame():

    unique_ids = sorted(set(df['id_start'].unique()).union(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)
    distance_matrix = distance_matrix.fillna(0)

    for index, row in df.iterrows():
        start, end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[start, end] = distance
        distance_matrix.at[end, start] = distance

    for i in distance_matrix.index:
        for j in distance_matrix.index:
            if i == j:
                continue
            if distance_matrix.at[i, j] == 0:
                for k in distance_matrix.index:
                    if i != k and j != k and distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix

result_matrix = calculate_distance_matrix(df)
print(result_matrix)

#TASK 2 - Q2
def unroll_distance_matrix(distance_matrix):
    upper_triangle = distance_matrix.where(np.triu(np.ones(distance_matrix.shape), k=1).astype(bool))
    unrolled_df = upper_triangle.stack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df

result_unrolled_df = unroll_distance_matrix(result_matrix)
print(result_unrolled_df)

#TASK 2 - Q3
def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
   ####3
    # Write your logic here
    reference_avg_distance = df[df['id_start'] == reference_id]['id_start'].mean()
    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.10)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.10)
    within_threshold_values = df[(df['id_start'] >= lower_threshold) & (df['id_start'] <= upper_threshold)]['id_start']
    sorted_within_threshold_values = sorted(within_threshold_values.unique())
    return sorted_within_threshold_values
reference_id = result_unrolled_df['id_start']
result_list = find_ids_within_ten_percentage_threshold(result_unrolled_df, reference_id)
print(result_list)

#TASK 2 - Q4
def calculate_toll_rate(df)->pd.DataFrame():

    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df
result_with_toll_rates = calculate_toll_rate(result_unrolled_df)
print(result_with_toll_rates)

#TASK 2 - Q5
from datetime import time
def calculate_time_based_toll_rates(df):
    time_ranges_weekdays = [(time(0, 0, 0), time(10, 0, 0)),
                            (time(10, 0, 0), time(18, 0, 0)),
                            (time(18, 0, 0), time(23, 59, 59))]

    time_ranges_weekends = [(time(0, 0, 0), time(23, 59, 59))]
    df['start_day'] = df['end_day'] = df['start_time'] = df['end_time'] = None

    def map_time_range(start, end, time_ranges):
        for time_range in time_ranges:
            if start >= time_range[0] and end <= time_range[1]:
                return time_range
        return None
    def apply_time_based_rates(row, time_ranges, discount_factor):
        start_day = row['start_day']
        end_day = row['end_day']
        start_time = row['start_time']
        end_time = row['end_time']
        for time_range in time_ranges:
            if start_time >= time_range[0] and end_time <= time_range[1]:
                row['start_time'] = time_range[0]
                row['end_time'] = time_range[1]
                row['start_day'] = start_day
                row['end_day'] = end_day
                row[['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor
                return row

    for index, row in df.iterrows():
        start_day = row['start_day']
        end_day = row['end_day']

        if start_day == end_day:
            if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                row = apply_time_based_rates(row, time_ranges_weekdays, 0.8)
            elif start_day in ['Saturday', 'Sunday']:
                row = apply_time_based_rates(row, time_ranges_weekends, 0.7)
    return df

result_with_time_based_rates = calculate_time_based_toll_rates(result_with_toll_rates)


desired_order = ['id_start', 'id_end', 'distance','start_day','start_time','end_day', 'end_time','moto','car','rv','bus','truck' ]

result_with_time_based_rates = result_with_time_based_rates[desired_order]
print(result_with_time_based_rates)
