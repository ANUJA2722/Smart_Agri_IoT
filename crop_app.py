import joblib
import serial
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

# ser = serial.Serial(
#     port='COM3',
#     baudrate=9600
# )

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    return render_template('Index.html')


@app.route('/Predict1')
def prediction1():
    return render_template('Index1.html')

@app.route("/about")
def about():
    return render_template('aboutUs.html')

@app.route("/service")
def service():
    return render_template('service.html')

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen=float(request.form['Nitrogen'])
    Phosphorus=float(request.form['Phosphorus'])
    Potassium=float(request.form['Potassium'])
    Temperature=float(request.form['Temperature'])
    Humidity=float(request.form['Humidity'])
    Ph=float(request.form['ph'])
    Rainfall=float(request.form['Rainfall'])
     
    values=[Nitrogen,Phosphorus,Potassium,Temperature,Humidity,Ph,Rainfall]
    
    if Ph>0 and Ph<=14 and Temperature<100 and Humidity>0:
        joblib.load('crop app','r')
        model = joblib.load(open('crop app','rb'))
        arr = [values]
        acc = model.predict(arr)
        acc = acc[0]
        return render_template('prediction.html', data=acc)
    else:
        return "Sorry...  Error in entered values in the form Please check the values and fill it again"

@app.route('/sensor')
def sensor():
    vals = ser.readline().decode()
    list_val =vals.split("_")
    list_val.pop()
    ser.reset_input_buffer()
    return render_template('sensor.html', val1 = list_val[0], val2 = list_val[1], val3 = list_val[2], val4 = list_val[3])


@app.route('/form1', methods=["POST"])
def brain1():
    Nitrogen=int(request.form['Nitrogen'])
    Phosphorus=int(request.form['Phosphorus'])
    Potassium=int(request.form['Potassium'])
    
     
    values=[Nitrogen,Phosphorus,Potassium]
    
    if Nitrogen>=0 and Nitrogen<=100 and Phosphorus>=0 and Phosphorus<=100 and Potassium>=0 and Potassium<=100:
        joblib.load('ferti app','r')
        model = joblib.load(open('ferti app','rb'))
        arr = [values]
        acc = model.predict(arr)
        if acc[0] == 0:
            ans = "TEN-TWENTY SIX-TWENTY SIX"
        elif acc[0] == 1:
            ans = "Fourteen-Thirty Five-Fourteen"
        elif acc[0] == 2:
            ans = "Seventeen-Seventeen-Seventeen"   
        elif acc[0] == 3:
            ans = "TWENTY-TWENTY"
        elif acc[0] == 4:
            ans = "TWENTY EIGHT-TWENTY EIGHT"
        elif acc[0] == 5:
            ans = "DAP"
        else:
            ans = "UREA"
        # print(acc)
        return render_template('prediction1.html', prediction= ans)
    else:
        return "Sorry...  Error in entered values in the form Please check the values and fill it again"


if __name__ == '__main__':
    app.run()