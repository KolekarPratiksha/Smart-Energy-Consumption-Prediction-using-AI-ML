import joblib
import calendar
import pandas as pd

# Load trained model pipeline
model = joblib.load('energy_model_pipeline.pkl')

# Mapping from city to power company
city_to_company = {
    'Mumbai': 'Tata Power',
    'Delhi': 'BSES Rajdhani',
    'Bengaluru': 'BESCOM',
    'Hyderabad': 'TSSPDCL',
    'Chennai': 'TANGEDCO',
    'Ahmedabad': 'Adani Power Ltd.',
    'Pune': 'MSEDCL',
    'Kolkata': 'CESC',
    'Jaipur': 'JVVNL',
    'Lucknow': 'UPPCL'
}

# Mapping from city to average tariff rate
city_to_tariff = {
    'Mumbai': 8.5,
    'Delhi': 7.8,
    'Bengaluru': 8.2,
    'Hyderabad': 8.0,
    'Chennai': 7.5,
    'Ahmedabad': 8.3,
    'Pune': 7.9,
    'Kolkata': 8.1,
    'Jaipur': 7.6,
    'Lucknow': 7.7
}

# Convert month name to number
month_name_to_number = {name: num for num, name in enumerate(calendar.month_name) if name}

def get_company_from_city(city):
    """Return the power company for a given city."""
    return city_to_company.get(city, 'Default Power Co.')

def get_tariff_from_city(city):
    """Return the tariff rate for a given city."""
    return city_to_tariff.get(city, 8.0)  # Default tariff if not listed

def calculate_monthly_hours(device_usage, month_input):
    # Convert to month name if input is an integer
    if isinstance(month_input, int):
        if not 1 <= month_input <= 12:
            raise ValueError(f"Invalid month number: {month_input}")
        month_name = calendar.month_name[month_input]
    else:
        month_name = month_input

    month_num = month_name_to_number.get(month_name)
    if not month_num:
        raise ValueError(f"Invalid month name: '{month_name}'")

    days = calendar.monthrange(2024, month_num)[1]
    return sum(count * hours_per_day * days for _, (count, hours_per_day) in device_usage.items())


def predict_bill(input_data):
    """Predict electricity bill based on input features."""
    input_df = pd.DataFrame([input_data])
    return model.predict(input_df)[0]
