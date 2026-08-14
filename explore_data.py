import pandas as pd

df = pd.read_csv("data/phishing_site_urls.csv")

print("Original shape:", df.shape)

# Remove duplicate URLs, keep the first occurrence
df = df.drop_duplicates(subset=["URL"], keep="first")

print("Shape after removing duplicates:", df.shape)
print()
print("Class balance after cleaning:")
print(df["Label"].value_counts())
print()
print(df["Label"].value_counts(normalize=True) * 100)

# Save the cleaned dataset so we don't repeat this step every time
df.to_csv("data/phishing_urls_clean.csv", index=False)
print()
print("Saved cleaned dataset to data/phishing_urls_clean.csv")