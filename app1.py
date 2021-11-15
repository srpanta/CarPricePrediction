from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('Random_Forest_Regression_Model.pkl','rb'))
@app.route('/',methods=["GET"])
def Home():
	return render_template('carprice1.html')

standard_to = StandardScaler()
@app.route('/predict',methods=["POST"])
def predict():
	if request.method=="POST":
		cylindernumber_four = str(request.form["Cylinder Number"])
		if(cylindernumber_four=="Four"):
			cylindernumber_four=1
		else:
			cylindernumber_four=0
		enginesize = int(request.form["Engine Size"])
		curbweight = int(request.form["Curbe Weight"])
		boreratio = int(request.form["Bore Ratio"])
		carwidth = int(request.form["Car Width"])
		horsepower = int(request.form["Horsepower"])
		highwaympg  = int(request.form["Highway MPG"])
		drivewheel_rwd = str(request.form["Drive Wheel"])
		if(drivewheel_rwd=="Rear"):
			drivewheel_rwd = 1
			drivewheel_fwd = 0
		else:
			drivewheel_rwd = 0
			drivewheel_fwd = 1
		carlength = int(request.form["Car Length"])
		fuelsystem_mpfi = str(request.form["Fuel System"])
		if(fuelsystem_mpfi == "mpfi"):
			fuelsystem_mpfi=1
		else:
			fuelsystem_mpfi=0
		input_features = [cylindernumber_four, enginesize, curbweight, boreratio, carwidth, horsepower, highwaympg, drivewheel_rwd, carlength,fuelsystem_mpfi]
		input_feat=[np.array(input_features)]
		prediction = model.predict(input_feat)
		output = round(prediction[0],2)
		if output<0:
			return render_template('carprice1.html',prediction_text="Sorry you cannot sell this car")
		else:
			return render_template('carprice1.html',prediction_text="Predicted Selling Price of this car is {}".format(output))
	else:
		return render_template('carprice1.html')
if __name__=="__main__":
	app.run(debug=True)