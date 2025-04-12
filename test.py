plt.figure(figsize=(10, 6))

for label, data in datasets.items():
    data.columns = data.columns.str.strip().str.lower()  # Normalize column names
    country_data = data[data['country_name'] == country]
    
    if country_data.empty:
        print(f"No data for {country} in {label}")
        continue

    plt.plot(country_data['year'], country_data['debt % of gdp'], label=label)

plt.xlabel('Year')
plt.ylabel('Debt (% of GDP)')
plt.title(f'Debt Types Over Time in {country}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()