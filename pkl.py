import pandas as pd
from plotUtils import plotPrescueVsBeta

import pandas as pd
df1 = pd.read_pickle('batchResults_E2_uniform.pkl')
df2 = pd.read_pickle('batchResults_E4_variable.pkl')
df = pd.concat([df1, df2], ignore_index=True)
df.to_pickle('batchResultsCombo.pkl')
print(f'Combined results saved to batchResultsCombo.pkl')

df = pd.read_pickle('batchResultsCombo.pkl')
print(f'head:\n {df.head()}')

plotPrescueVsBeta(df, penetranceMode='variable', savePath='test_curve.png')
