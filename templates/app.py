from flask import Flask, render_template, request
import joblib
import pandas as pd
import csv
import os

app = Flask(__name__)
model = joblib.load("traffic_model.pkl")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            temp = float(request.form['temp'])
            rain = float(request.form['rain'])
            snow = float(request.form['snow'])
            weather = int(request.form['weather'])
            hour = int(request.form['hour'])
            day = int(request.form['day'])
            month = int(request.form['month'])
            weekday = int(request.form['weekday'])

            input_data = pd.DataFrame([{
                'temp': temp,
                'rain': rain,
                'snow': snow,
                'weather': weather,
                'hour': hour,
                'day': day,
                'month': month,
                'weekday': weekday
            }])

            prediction = int(model.predict(input_data)[0])

            # Log to CSV
            log_file = 'traffic_log.csv'
            file_exists = os.path.isfile(log_file)
            with open(log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['temp', 'rain', 'snow', 'weather', 'hour', 'day', 'month', 'weekday', 'prediction'])
                writer.writerow([temp, rain, snow, weather, hour, day, month, weekday, prediction])

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
