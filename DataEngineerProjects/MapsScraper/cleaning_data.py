import re
import pandas as pd

def cleaning_data(dados):

    data_splited = []

    for line in dados:
        
        parts = re.split(r"\n", line)
        data_splited.append(parts)

    df = pd.DataFrame(data_splited)

    display(df)

    return df