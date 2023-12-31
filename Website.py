import pandas as pd
from flask import Flask, render_template, request, send_file
import io
import requests

app = Flask(__name__)

# Initialize an empty list to store the responses from the REST endpoint
data_store = []

@app.route('/')
def index():
    # Make an HTTP GET request to the REST endpoint
    response = requests.get('http://localhost:8086/api/file_tempo')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract relevant data from the response (assuming JSON response)
        data = response.json()

        # Append the data to the data store
        data_store.append(data)

    # Render the HTML template with a more user-friendly layout
    return render_template('index.html', data=data_store)

@app.route('/export')
def export():
    # Create a Pandas DataFrame from your data store
    df = pd.DataFrame(data_store)

    # Create an Excel writer using XlsxWriter as the engine
    output = io.BytesIO()  # Create a BytesIO object to store the Excel file

    # Convert the DataFrame to an XlsxWriter Excel object
    df.to_excel(output, engine='xlsxwriter', index=False)

    # Return the Excel file as a response
    output.seek(0)  # Move the cursor to the start of the BytesIO stream
    return send_file(output, as_attachment=True, download_name='audio_files.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
    
    
