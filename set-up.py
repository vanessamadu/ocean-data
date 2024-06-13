import pandas as pd

columns = [
    "Data Set Name",
    "Owner/Organisation",
    "Spatial Resolution",
    "Temporal Resolution",
    "Spatial Extent",
    "Temporal Extent",
    "Measured Quantities",
    "Precision",
    "Uncertainties",
    "Missing Values/Outliers Protocol",
    "Data Format",
    "Processing Level",
    "Documentation",
    "Citation",
    "Data File Type",
    "Date Accessed",
    "Accessed From",
    "Additional Notes/Links"
]

ocean_data_df = pd.DataFrame(columns = columns)