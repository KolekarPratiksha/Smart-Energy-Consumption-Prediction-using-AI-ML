from flask import Flask, render_template, request
from prediction import predict_bill, get_company_from_city, calculate_monthly_hours, get_tariff_from_city
from visualization import generate_trend_plot
from recommendation_engine import get_recommendation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai',
              'Ahmedabad', 'Pune', 'Kolkata', 'Jaipur', 'Lucknow']
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    if request.method == 'POST':
        city = request.form['city']
        month = int(request.form['month'])
        fan_count = int(request.form['fan'])
        fan_hours = float(request.form['fan_hours'])
        fridge_count = int(request.form['fridge'])
        fridge_hours = float(request.form['fridge_hours'])
        ac_count = int(request.form['ac'])
        ac_hours = float(request.form['ac_hours'])

        # Calculate usage
        monthly_hours = calculate_monthly_hours({
            'Fan': (fan_count, fan_hours),
            'Refrigerator': (fridge_count, fridge_hours),
            'AirConditioner': (ac_count, ac_hours)
        }, month)

        company = get_company_from_city(city)
        tariff = get_tariff_from_city(city)

        input_data = {
            'Fan': fan_count,
            'Refrigerator': fridge_count,
            'AirConditioner': ac_count,
            'Television': 0,
            'Monitor': 0,
            'MotorPump': 0,
            'Month': month,
            'City': city,
            'Company': company,
            'MonthlyHours': monthly_hours,
            'TariffRate': tariff
        }

        prediction = predict_bill(input_data)
        generate_trend_plot(input_data['City'])

        device_str = f"{fan_count} fan(s) for {fan_hours} hrs/day, " \
                     f"{fridge_count} fridge(s) for {fridge_hours} hrs/day, " \
                     f"{ac_count} AC(s) for {ac_hours} hrs/day"

        recommendation = get_recommendation(city, prediction, device_str)

        return render_template(
            'result.html',
            prediction=prediction,
            city=city,
            company=company,
            recommendation=recommendation
        )

    return render_template('form.html', cities=cities, months=months)

if __name__ == '__main__':
    app.run(debug=True)
