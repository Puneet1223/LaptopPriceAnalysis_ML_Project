from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load trained pipeline and dataset
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

@app.route('/')
def home():
    return render_template(
        'index.html',
        companies=sorted(df['Company'].unique()),
        types=sorted(df['TypeName'].unique()),
        os_list=sorted(df['OS'].unique()),
        gpus=sorted(df['GPU_company'].unique()),
        cpus=sorted(df['Cpu_Brand'].unique())
    )

@app.route('/predict', methods=['POST'])
def predict():
    # Collect input from HTML form
    company = request.form['Company']
    typename = request.form['TypeName']
    inches = float(request.form['Inches'])
    ram = int(request.form['Ram'])
    os = request.form['OS']
    weight = float(request.form['Weight'])
    touchscreen = int(request.form['Touchscreen'])
    ips_panel = int(request.form['IPSpanel'])
    gpu_company = request.form['GPU_company']
    ppi = float(request.form['PPI'])
    cpu_brand = request.form['Cpu_Brand']
    ssd = int(request.form['SSD'])
    hdd = int(request.form['HDD'])

    # Put into dataframe (column order must match training set)
    input_df = pd.DataFrame([[company, typename, inches, ram, os, weight,
                              touchscreen, ips_panel, gpu_company, ppi,
                              cpu_brand, ssd, hdd]],
                            columns=['Company','TypeName','Inches','Ram','OS',
                                     'Weight','Touchscreen','IPSpanel',
                                     'GPU_company','PPI','Cpu_Brand','SSD','HDD'])

    # Make prediction
    prediction = np.exp(pipe.predict(input_df)[0])

    return render_template(
        'index.html',
        prediction_text=f'Predicted Laptop Price: ₹{round(prediction,2)}',
        companies=sorted(df['Company'].unique()),
        types=sorted(df['TypeName'].unique()),
        os_list=sorted(df['OS'].unique()),
        gpus=sorted(df['GPU_company'].unique()),
        cpus=sorted(df['Cpu_Brand'].unique())
    )

if __name__ == "__main__":
    app.run(debug=True)
