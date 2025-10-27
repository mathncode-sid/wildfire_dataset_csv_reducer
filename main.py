import pandas as pd


# === CONFIG ===
SOURCE_FILE = "Wildfire_Dataset.csv"
OUTPUT_SAMPLE = "Wildfire_Dataset_sampled.csv"
OUTPUT_WEEKLY = "Wildfire_Dataset_weekly.csv"

# === STEP 1: Read in chunks to prevent memory overload ===
chunksize = 100_000
keep_columns = [
    'latitude', 'longitude', 'datetime', 'Wildfire', 'pr',
    'rmax', 'rmin', 'sph', 'srad', 'tmmn', 'tmmx', 'vs',
    'bi', 'fm100', 'fm1000', 'erc', 'etr', 'pet', 'vpd'
]

sampled_chunks = []
for chunk in pd.read_csv(SOURCE_FILE, usecols=keep_columns, chunksize=chunksize):
    # Sample 10% of each chunk for representativeness
    sampled = chunk.sample(frac=0.1, random_state=42)
    sampled_chunks.append(sampled)

df_sampled = pd.concat(sampled_chunks, ignore_index=True)
df_sampled['datetime'] = pd.to_datetime(df_sampled['datetime'], errors='coerce')

# === STEP 2: Clean up and filter ===
# Drop rows missing essential info
df_sampled = df_sampled.dropna(subset=['latitude', 'longitude', 'datetime'])

# Keep continental U.S. bounding box if applicable
df_sampled = df_sampled.query("24 <= latitude <= 49 and -125 <= longitude <= -66")

# === STEP 3: Save reduced dataset (≈100–150MB) ===
df_sampled.to_csv(OUTPUT_SAMPLE, index=False)
print(f" Saved reduced dataset: {OUTPUT_SAMPLE} | Shape: {df_sampled.shape}")

# === STEP 4: Create weekly aggregated version ===
df_sampled['week'] = df_sampled['datetime'].dt.to_period('W').astype(str)
agg_df = (
    df_sampled.groupby('week', as_index=False)
    .agg({
        'Wildfire': 'sum',          # total fires
        'pr': 'mean',               # precipitation
        'rmax': 'mean',
        'rmin': 'mean',
        'sph': 'mean',              # humidity proxy
        'tmmn': 'mean',             # min temp
        'tmmx': 'mean',             # max temp
        'vs': 'mean',               # wind speed
        'fm100': 'mean',            # fuel moisture
        'fm1000': 'mean',
        'erc': 'mean',              # energy release component
        'vpd': 'mean'               # vapor pressure deficit
    })
)
agg_df.rename(columns={'Wildfire': 'fires_reported'}, inplace=True)

# === STEP 5: Save weekly summary ===
agg_df.to_csv(OUTPUT_WEEKLY, index=False)
print(f"Saved weekly summary: {OUTPUT_WEEKLY} | Shape: {agg_df.shape}")

print("\nBoth files are optimized for PromptBI (under 200MB total).")
