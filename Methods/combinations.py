

import numpy as np

import pandas as pd



# Generate all possible combinations

values = np.arange(0, 0.1005, 0.0005)

combinations = np.array(np.meshgrid(values, values, values)).T.reshape(-1, 3)



# Create a DataFrame

df = pd.DataFrame(combinations, columns=['X', 'Y', 'Z'])



# Save to CSV

file_path = "/mnt/data/combinations_0_to_0.1.csv"

df.to_csv(file_path, index=False)
