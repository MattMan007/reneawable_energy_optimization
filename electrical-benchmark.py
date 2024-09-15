import pandas as pd

# Dictionary to map country codes to country names for wind and solar data
country_dict = {
    "BE": "Belgium", "BG": "Bulgaria", "CH": "Switzerland", "CY": "Cyprus", "CZ": "Czech Republic",
    "DK": "Denmark", "EE": "Estonia", "ES": "Spain", "FI": "Finland", "GB": "Great Britain",
    "GR": "Greece", "HR": "Croatia", "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "MT": "Malta", "NL": "Netherlands",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RS": "Serbia", "SE": "Sweden",
    "SI": "Slovenia", "SK": "Slovakia", "DE": "Germany", "FR": "France", "AT": "Austria"
}

# Reverse dictionary for country code lookup by country name
reverse_country_dict = {v: k for k, v in country_dict.items()}

# Function to load the data
def load_data(wind_csv, solar_csv):
    wind_df = pd.read_csv(wind_csv, parse_dates=[0], dayfirst=True)
    solar_df = pd.read_csv(solar_csv, parse_dates=[0], dayfirst=False)

    print("Wind Data Columns:", wind_df.columns)
    print("Solar Data Columns:", solar_df.columns)

    return wind_df, solar_df

# Function to get the country name or code based on the input
def get_country_by_input(country_or_code, dataset_type):
    if dataset_type == 'wind':
        # For wind data (country names), match using the country name
        if country_or_code in country_dict.values():
            return country_or_code  # Return the country name directly
        elif country_or_code in country_dict:
            return country_dict[country_or_code]  # Return country name from code
    elif dataset_type == 'solar':
        # For solar data (country codes), match using the country code
        if country_or_code in country_dict:
            return country_or_code  # Return country code directly
        elif country_or_code in reverse_country_dict:
            return reverse_country_dict[country_or_code]  # Return code from name
    return None

# Function to calculate the daily average for a country
def get_daily_average(df, country, date, time_column, dataset_type):
    country_col = get_country_by_input(country, dataset_type)
    if country_col not in df.columns:
        print(f"Country '{country}' not found in data for {dataset_type}.")
        return None
    
    # Convert the time column to datetime
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
    
    # Filter the data for the selected date
    daily_data = df[df[time_column].dt.date == date.date()]
    if daily_data.empty:
        print(f"No data found for {country} on {date}.")
        return None
    
    # Debug: show daily data for the country
    print(f"Daily data for {country} on {date}:")
    print(daily_data[country_col])

    # Calculate the average for that day
    return daily_data[country_col].mean()

# Main function to process user inputs and get the average
def process_inputs(date, country_or_code, wind_df, solar_df):
    wind_avg = get_daily_average(wind_df, country_or_code, date, 'GMT', 'wind')
    solar_avg = get_daily_average(solar_df, country_or_code, date, 'time', 'solar')

    return wind_avg, solar_avg

# Example usage
if __name__ == "__main__":
    # Load the data
    wind_csv = 'ninja_europe_wind_output.csv'
    solar_csv = 'ninja_europe_solar_output.csv'
    wind_df, solar_df = load_data(wind_csv, solar_csv)

    # For debugging, hardcode the input values
    input_date = pd.to_datetime("2011-09-14")  # Enter your test date here
    input_country = "BG"  # Enter your test country code here (e.g., "DE" or "Germany")

    # Ensure the date is between 1985 and 2014
    if not (pd.Timestamp("1985-01-01") <= input_date <= pd.Timestamp("2014-12-31")):
        print("Date must be between 1985 and 2014.")
    else:
        # Process and get averages
        wind_avg, solar_avg = process_inputs(input_date, input_country, wind_df, solar_df)

        # Output the results
        print(f'Wind Average: {wind_avg}')
        print(f'Solar Average: {solar_avg}')

