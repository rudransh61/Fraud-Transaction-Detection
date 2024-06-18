import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Function to process the data in chunks
def process_chunk(chunk, G, node_data):
    # Convert step (assuming it's an integer or float representing a time step) to numerical values
    chunk['step'] = chunk['step'].astype('int64')

    # Encode nameOrig and nameDest to numerical values
    chunk['nameOrig'] = chunk['nameOrig'].astype('category').cat.codes
    chunk['nameDest'] = chunk['nameDest'].astype('category').cat.codes

    # Add nodes
    for idx, row in chunk.iterrows():
        G.add_node(idx, amount=row['amount'], step=row['step'], 
                   nameOrig=row['nameOrig'], nameDest=row['nameDest'], 
                   oldbalanceOrg=row['oldbalanceOrg'], newbalanceOrig=row['newbalanceOrig'], 
                   oldbalanceDest=row['oldbalanceDest'], newbalanceDest=row['newbalanceDest'])
        
        node_data[idx] = row

# Initialize the graph
G = nx.Graph()
node_data = {}

# Read the first 1000 rows from the CSV file
df = pd.read_csv('Fraud.csv', nrows=5000)

# Process the chunk
process_chunk(df, G, node_data)

# Add edges based on the distance function
threshold = 2000  # Define a threshold for similarity
nodes = list(G.nodes(data=True))
for i, (node_i, data_i) in enumerate(nodes):
    for j, (node_j, data_j) in enumerate(nodes):
        if i < j:  # Avoid duplicate edges and self-loops
            distance = (
                abs(data_i['amount'] - data_j['amount']) +
                abs(data_i['step'] - data_j['step']) +
                abs(data_i['nameOrig'] - data_j['nameOrig']) +
                abs(data_i['nameDest'] - data_j['nameDest']) +
                abs(data_i['oldbalanceOrg'] - data_j['oldbalanceOrg']) +
                abs(data_i['newbalanceOrig'] - data_j['newbalanceOrig']) +
                abs(data_i['oldbalanceDest'] - data_j['oldbalanceDest']) +
                abs(data_i['newbalanceDest'] - data_j['newbalanceDest'])
            )
            if distance < threshold:
                G.add_edge(node_i, node_j)

# Calculate degrees for each transaction
degree_dict = dict(G.degree())
for node in G.nodes:
    G.nodes[node]['degree'] = degree_dict[node]

# Convert the graph back to a DataFrame for analysis
df = pd.DataFrame.from_dict(node_data, orient='index')
df['degree'] = df.index.map(degree_dict)

# Determine fraud based on degree (using an arbitrary threshold for this example)
degree_threshold = df['degree'].mean()  # Transactions with degrees above the mean are considered suspicious
df['predicted_fraud'] = df['degree'] > degree_threshold

# Check if 'isFraud' column exists in the CSV for accuracy calculation
if 'isFraud' in df.columns:
    # Calculate accuracy
    accuracy = accuracy_score(df['isFraud'], df['predicted_fraud'])

    # Output the results
    print(df)
    print(f"Accuracy: {accuracy*100}%")
else:
    print("Error: 'isFraud' column not found in the data.")

# Plotting the graph for visualization (optional for large graphs)
# Position nodes using a layout (may be slow for very large graphs)
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
# nx.draw_networkx_edges(G, pos)
# labels = {node: f"{node}\nDeg: {degree}" for node, degree in degree_dict.items()}
# nx.draw_networkx_labels(G, pos, labels, font_size=10)
# plt.title('Transaction Similarity Graph')
# plt.show()
