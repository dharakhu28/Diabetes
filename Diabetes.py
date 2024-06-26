import streamlit as st 
import re
import sqlite3
import pickle
import pandas as pd

st.set_page_config(page_title="Diabetes Prediction", page_icon="Fevicon.jpeg", layout="centered", initial_sidebar_state="auto", menu_items=None)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.

    Returns
    -------
    None.
    The background

    '''
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:url("https://www.shutterstock.com/image-vector/cute-cartoon-red-droplet-checks-260nw-2280322507.jpg");
            
            background-size: cover
            }}
         </style>
         """,
         unsafe_allow_html=True
        )
set_bg_hack_url()

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()
    
menu = ["Home","SignUp","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
        """
        <h2 style="color:black">Welcome to Diabetes Prediction System</h2>
        <h1>   </h1>
        <p align="justify">
        <b style="color:black">The Diabetes Condition Prediction System with Python Webapp is a cutting-edge solution aimed at early detection and management of
        diabetes using predictive analytics and a user-friendly webinterface. Utilizing machine learning algorithms implemented in Python, the system analyzes
        diverse health parameters,such as blood glucose levels,body mass index and medical history, to predict the likelihood of diabetes onset. The accompanying 
        web application provides an accessible platform for user to input relevant health data and in return it delivers real time prediction and personalized 
        recommendations for lifestyle modifications. By leveraging technology to forecast diabetes risk and offering actionable insight, this system contributes 
        to proactive healthcare, faciliating early intervention and improved quality of life for individuals at risk of or alredy living with diabetes.</b>
        </p>
        """
        ,unsafe_allow_html=True)
if choice=="SignUp":
        Fname = st.text_input("First Name")
        Lname = st.text_input("Last Name")
        Mname = st.text_input("Mobile Number")
        Email = st.text_input("Email")
        City = st.text_input("City")
        Password = st.text_input("Password",type="password")
        CPassword = st.text_input("Confirm Password",type="password")
        b2=st.button("SignUp")
        if b2:
            pattern=re.compile("[7-9][0-9]{9}")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if Password==CPassword:
                if (pattern.match(Mname)):
                    if re.fullmatch(regex, Email):
                        create_usertable()
                        add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                        st.success("SignUp Success")
                        st.info("Go to Logic Section for Login")
                    else:
                        st.warning("Not Valid Email")         
                else:
                    st.warning("Not Valid Mobile Number")
            else:
                st.warning("Pass Does Not Match")
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")    
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            result = login_user(Email,Password)
            if result:
                if Email=="a@a.com" and Password=="123":
                    st.success("Logged In as {}".format(Email))
                    st.success("Logged In as {}".format(Email))
                    Email1=st.text_input("DeleteEmail")
                    if st.button('Delete'):
                         delete_user(Email1)
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                    st.dataframe(clean_db)
                else:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)
                    Pregnancies=float(st.slider('Pregnancies Value', 0, 17))
                    Glucose=float(st.slider('Glucose Value', 0, 199))
                    BP=float(st.slider('BP Value', 0, 122))
                    SkinThickness=float(st.slider('SkinThickness Value', 0, 99))
                    Insullin=float(st.slider('Insullin Value', 0, 846))
                    BMI=float(st.slider('BMI Value', 0.0, 67.0))
                    DPF=float(st.slider('DPF Value', 0.078, 2.42))
                    Age=float(st.slider('Age Value', 21, 81))
                    my_array=[Pregnancies,Glucose,BP,SkinThickness,Insullin,BMI,DPF,Age] 
                    
                    b2=st.button("Predict")
                    model=pickle.load(open("model.pkl",'rb'))
                    if b2:                        
                        tdata=[my_array]
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                                test_prediction = model[0].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)
                        if choice2=="SVM":
                                test_prediction = model[1].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)                 
                        if choice2=="Decision Tree":
                                test_prediction = model[2].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)
                        if choice2=="Random Forest":
                                test_prediction = model[3].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)
                        if choice2=="Naive Bayes":
                                test_prediction = model[4].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)
                        if choice2=="ExtraTreesClassifier":
                                test_prediction = model[5].predict(tdata)
                                query=test_prediction[0]
                                #st.success(query)
                       
                        if query==0:
                            st.success("Not Diabetic")
                        else:
                            st.warning("Diabetic Detected")
            else:
                st.error("Wrong Email/Password")
        else:
            st.error("Wrong Email")
        
        