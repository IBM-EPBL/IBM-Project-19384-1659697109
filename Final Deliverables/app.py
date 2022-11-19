from flask import Flask, render_template,request
import pickle
import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "eJqAgq9PC4DNCsDnTj0pfeO4-Rk0jXwNWF61-LDwFYDL"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [
    {"field": [["Age","Gender","Total_bilirubin","Direct_bilirubin","Alkaline_Phosphotase","Alamine_aminotransferase","Aspartate_aminotransferase","Total_proteins","Albumin","Albumin_and_Globulin_Ratio"]], "values": [[60, 0, 0.5, 0.1, 500, 20, 34, 5.9, 1.6, 0.37]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1fa5146a-e569-4468-9102-608caa26c387/predictions?version=2022-11-18', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})


app = Flask(__name__)

@app.route('/')
def bot():
    return render_template('home.html')

@app.route('/predict',methods=["POST"])

def predict():
    Age=request.form['Age']
    gender=request.form['Gender']
    tb=request.form['Total_bilirubin']
    db=request.form['Direct_bilirubin']
    ap=request.form['Alkaline_Phosphotase']
    aa1=request.form['Alamine_aminotransferase']
    aa2=request.form['Aspartate_aminotransferase']
    tp=request.form['Total_proteins']
    a=request.form['Albumin']
    agr=request.form['Albumin_and_Globulin_Ratio']
    
    data=[[float(Age),float(gender),float(tb),float(db),float(ap),float(aa1),float(aa2),float(tp),float(a),float(agr)]]
    model=pickle.load(open('liver_analysis.pkl','rb'))
    print(data)
    prediction=model.predict(data)
    
    if (prediction==1):
        output="You do not have liver disease."
    else:
        output="You have liver disease"
    return render_template('home.html',prediction_text=output)

if __name__=='__main__':
    app.run(debug=True)
        

