      step      type     amount  nameOrig  oldbalanceOrg  newbalanceOrig  ...  oldbalanceDest  newbalanceDest  isFraud  isFlaggedFraud  degree  predicted_fraud
0        1   PAYMENT    9839.64       574      170136.00       160296.36  ...            0.00            0.00        0               0       0            False
1        1   PAYMENT    1864.28      1733       21249.00        19384.72  ...            0.00            0.00        0               0       2            False
2        1  TRANSFER     181.00       780         181.00            0.00  ...            0.00            0.00        1               0      10             True
3        1  CASH_OUT     181.00      4581         181.00            0.00  ...        21182.00            0.00        1               0       0            False
4        1   PAYMENT   11668.14      2768       41554.00        29885.86  ...            0.00            0.00        0               0       0            False
...    ...       ...        ...       ...            ...             ...  ...             ...             ...      ...             ...     ...              ...
e
e
e
4998     5   CASH_IN  328776.10      4486     4547034.84      4875810.94  ...      1019467.84       962737.60        0               0       0            False
4999     5   CASH_IN   50535.87      2351     4875810.94      4926346.82  ...        70183.75        19647.88        0               0       0            False

[5000 rows x 13 columns]
Accuracy: 84.94%
https://www.kaggle.com/datasets/miznaaroob/fraudulent-transactions-data