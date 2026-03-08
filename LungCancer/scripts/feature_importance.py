import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load data and model
df = pd.read_csv("data/features.csv")
model = joblib.load("models/radiomics_rf_model.pkl")

X = df.drop(columns=["label"])
feature_names = X.columns

# Get feature importance
importances = model.feature_importances_

# Create DataFrame
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Print top features
print("\nTop 10 Important Features:\n")
print(importance_df.head(10))

# Plot
plt.figure(figsize=(10, 6))
plt.barh(
    importance_df["Feature"][:10][::-1],
    importance_df["Importance"][:10][::-1]
)
plt.xlabel("Importance Score")
plt.title("Top 10 Radiomics Features for Lung Cancer Detection")
plt.tight_layout()
plt.show()
