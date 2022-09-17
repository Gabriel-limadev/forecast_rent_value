# API - Flask 
from flask import Flask, request 
from datetime import datetime
import joblib
import sqlite3

# instantiate app
app = Flask(__name__)

# load model
model = joblib.load('Random_Forest_Model_v1.pk1')


# ------------------ FUNCTION API ------------------
# Function for get our API
@app.route('/API_prediction/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>', methods = ['GET'])
def Function_01(area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa):

    start_date = datetime.now()

    features = [
        float(area), float(rooms), float(bathroom), float(parking_spaces),
        float(floor), float(animal), float(furniture), float(hoa)
    ]

    # Prediction
    try:
        prediction = model.predict([features])
        
        # insert the prediction value
        features.append(str(prediction))

        # Transforming feature in str
        input = ''
        for value in features:
            input = input + ';' + str(value)

        end_date = datetime.now()
        processing = end_date - start_date

        # ------------------ DATABASE CONNECTION ------------------
        # Create conncetion with database
        database_connection = sqlite3.connect('API_database.db')
        cursor = database_connection.cursor()

        # query 
        query_insert = f'''
            INSERT INTO Log_API (Inputs, Start, End, Processing)
            VALUES ('{input}', '{start_date}', '{end_date}', '{processing}')
        '''

        print(query_insert)
        # Executing query
        cursor.execute(query_insert)
        database_connection.commit()
        cursor.close()

        # Return model
        return {'Rent Value': str(prediction)}
    except:
        return {'Warning': 'Error'}


if __name__ == '__main__':
    app.run(debug = True)

