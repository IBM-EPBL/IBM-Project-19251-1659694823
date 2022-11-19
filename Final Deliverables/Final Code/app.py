import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests
from flask import Flask, request, render_template, redirect, url_for
from cloudant.client import Cloudant

# Authenticate using an IAM API key
client = Cloudant.iam('7a432718-925c-4d97-b679-d49131ffae12-bluemix','aQskDQNm0R_p8myc2CcIXTJ3COwVpWeN3VKVrddm4MjP', connect=True)

# Create a database using an initialized client
my_database = client.create_database('my_database')

model = load_model(r"Updated-Xception-diabetic-retinopathy.h5")

app = Flask(__name__)


# default home page or route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def home():
    return render_template("index.html")


# registration page
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/afterreg', methods=['POST'])
def afterreg():
    x = [x for x in request.form.values()]
    print(x)
    data = {
    '_id': x[1], # Setting _id is optional
    'name': x[0],
    'psw':x[2]
    }
    print(data)
    
    query = {'_id': {'$eq': data['_id']}}
    
    docs = my_database.get_query_result(query)
    print(docs)
    
    print(len(docs.all()))
    
    if(len(docs.all())==0):
        url = my_database.create_document(data)
        #response = requests.get(url)
        return render_template('register.html', pred="Registration Successful, please login using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your details")

# login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)
    
    query = {'_id': {'$eq': user}}    
    
    docs = my_database.get_query_result(query)
    print(docs)
    
    print(len(docs.all()))
    
    
    if(len(docs.all())==0):
        return render_template('login.html', pred="The username is not found.")
    else:
        if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
            return redirect(url_for('prediction'))
        else:
            print('Invalid User')
    
    
@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/result',methods=["GET","POST"])
def res():
    if request.method=="POST":
        f=request.files['image']
        basepath=os.path.dirname(__file__) #getting the current path i.e where app.py is present
        #print("current path",basepath)
        filepath=os.path.join(basepath,'uploads',f.filename) #from anywhere in the system we can give image but we want that image later  to process so we are saving it to uploads folder for reusing
        #print("upload folder is",filepath)
        f.save(filepath)

        img=image.load_img(filepath,target_size=(299,299))
        x=image.img_to_array(img)#img to array
        x=np.expand_dims(x,axis=0)#used for adding one more dimension
        #print(x)
        img_data=preprocess_input(x)
        prediction=np.argmax(model.predict(img_data), axis=1)

        #prediction=model.predict(x)#instead of predict_classes(x) we can use predict(X) ---->predict_classes(x) gave error
        #print("prediction is ",prediction)
        index=['No Diabetic Retinopathy', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
        #result = str(index[output[0]])
        result=str(index[ prediction[0]])
        print(result)
        return render_template('prediction.html',prediction=result)
        



""" Running our application """
if __name__ == "__main__":
    app.run()