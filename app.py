import streamlit as st
import pandas as pd
import os

# Quick sort implementation
def quick_sort(arr, low, high, key):
    if low < high:
        pi = partition(arr, low, high, key)
        quick_sort(arr, low, pi - 1, key)
        quick_sort(arr, pi + 1, high, key)

def partition(arr, low, high, key):
    i = low - 1
    pivot = arr[high][key]
    for j in range(low, high):
        if arr[j][key] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Knapsack problem algorithm implementation
def knapsack(crops, max_weight, weight_key, value_key):
    n = len(crops)
    K = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]
    
    for i in range(n + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif crops[i - 1][weight_key] <= w:
                K[i][w] = max(crops[i - 1][value_key] + K[i - 1][w - crops[i - 1][weight_key]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]
    
    res = K[n][max_weight]
    w = max_weight
    selected_crops = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            selected_crops.append(crops[i - 1])
            res -= crops[i - 1][value_key]
            w -= crops[i - 1][weight_key]
    
    return selected_crops

# Define the CropRecommendationSystem class
class CropRecommendationSystem:
    def __init__(self, dataset):
        self.dataset = dataset

    def recommended_crop(self, user_data):
        matched_crops = []
        for index, crop in self.dataset.iterrows():
            if (user_data["nitrogen"] >= crop["nitrogen"] and user_data["nitrogen"] <= crop["nitrogen"]) and \
               (user_data["phosphorous"] >= crop["phosphorus"] and user_data["phosphorous"] <= crop["phosphorus"]) and \
               (user_data["potassium"] >= crop["potassium"] and user_data["potassium"] <= crop["potassium"]) and \
               (user_data["temperature"] >= crop["temperature"] and user_data["temperature"] <= crop["temperature"]) and \
               (user_data["humidity"] >= crop["humidity"] and user_data["humidity"] <= crop["humidity"]) and \
               (user_data["ph"] >= crop["ph"] and user_data["ph"] <= crop["ph"]) and \
               (user_data["rainfall"] >= crop["rainfall"] and user_data["rainfall"] <= crop["rainfall"]):
                matched_crops.append(crop.to_dict())

        # Sort matched crops using quick sort based on a chosen attribute, e.g., 'yield'
        quick_sort(matched_crops, 0, len(matched_crops) - 1, 'yield')
        # Return the sorted crop labels
        return [crop["label"] for crop in matched_crops]

# Load dataset
@st.cache_data
def load_dataset(filepath):
    if not os.path.isfile(filepath):
        st.error(f"File not found: {filepath}")
        return None
    return pd.read_csv(filepath)

dataset_path = "D:/SEM 4/Data Structures/crop dataset (project).csv"
dataset = load_dataset(dataset_path)

if dataset is not None:
    recommendation_system = CropRecommendationSystem(dataset)
else:
    st.stop()

# Define navigation
PAGES = {
    "Home": "home",
    "Personal Details": "personal_details",
    "Recommendations": "recommendations",
    "Feedback": "feedback",
    "About": "about",
    "Contact Us": "contact",
    "Gallery": "gallery"
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Define the Home page
def home():
    st.title("Crop Recommendation System")
    st.write("Welcome to the Crop Recommendation System. Use the sidebar to navigate to different pages.")
    st.image("D:/SEM 4/Data Structures/home.jpg", caption="Crop Recommendation", use_column_width=True)
    st.write("""
    This system helps farmers to select the best crop to grow based on soil and climate conditions. 
    It uses a dataset to recommend crops based on various parameters like nitrogen, phosphorous, potassium, temperature, humidity, soil pH, and rainfall. Join us and enjoy the journey of crop recommendation.
    """)

# Define the Personal Details page
def personal_details():
    st.title("Personal Details")
    
    with st.form("personal_details_form"):
        name = st.text_input("Enter your name:")
        date_of_birth = st.date_input("Enter your date of birth:")
        gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
        email = st.text_input("Enter your email:")
        phone = st.text_input("Enter your phone number:")
        address = st.text_area("Enter your address:")
        submit_button = st.form_submit_button("Submit")

    # Store personal details in session state
    if submit_button and name and date_of_birth and gender and email and phone and address:
        st.session_state['personal_details'] = {
            "name": name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "email": email,
            "phone": phone,
            "address": address
        }
        st.success("Personal details saved successfully.")

# Define the Recommendations page
def recommendations():
    st.title("Get Crop Recommendations")
    
    if 'personal_details' not in st.session_state:
        st.warning("Please provide your personal details first.")
        return
    
    with st.form("recommendation_form"):
        nitrogen = st.number_input("Enter nitrogen level:")
        phosphorous = st.number_input("Enter phosphorous level:")
        potassium = st.number_input("Enter potassium level:")
        temperature = st.number_input("Enter temperature in Celsius:")
        humidity = st.number_input("Enter humidity percentage:")
        ph = st.number_input("Enter soil pH:")
        rainfall = st.number_input("Enter rainfall in mm:")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        user_data = {
            "nitrogen": nitrogen,
            "phosphorous": phosphorous,
            "potassium": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }
        recommended_crops = recommendation_system.recommended_crop(user_data)
        if not recommended_crops:
            recommended_crops = ["Recommended crop: cotton"]
        
        personal_details = st.session_state['personal_details']
        st.write(f"Hello {personal_details['name']}, Recommended crop: {', '.join(recommended_crops)}")

# Define the Feedback page
def feedback():
    st.title("Feedback")
    
    st.image("D:/SEM 4/Data Structures/feedback.jpg", caption="We Value Your Feedback", use_column_width=True)
    
    with st.form("feedback_form"):
        feedback_text = st.text_area("Please provide your feedback:")
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        st.write("Thank you for your feedback!")

# Define the About page
def about():
    st.title("About")
    st.write("This Crop Recommendation System helps farmers to select the best crop to grow based on soil and climate conditions.")
    st.write("It uses a dataset to recommend crops based on various parameters like nitrogen, phosphorous, potassium, temperature, humidity, soil pH, and rainfall.")
    st.image("D:/SEM 4/Data Structures/about.jpg", caption="About Us", use_column_width=True)

# Define the Contact Us page
def contact():
    st.title("Contact Us")
    st.write("For any inquiries or support, please contact us at:")
    st.write("Email: support@croprecommendation.com")
    st.write("Phone: +91 93607 57708")
    st.image("D:/SEM 4/Data Structures/contact_us.jpg", caption="Contact Us", use_column_width=True)

# Define the Gallery page
def gallery():
    st.title("Gallery")
    st.write("Here are some pictures related to crop cultivation and farming.")
    st.image("D:/SEM 4/Data Structures/g1.jpg", caption="Crop Field 1", use_column_width=True)
    st.image("D:/SEM 4/Data Structures/g2.jpg", caption="Crop Field 2", use_column_width=True)
    st.image("D:/SEM 4/Data Structures/g3.jpg", caption="Crop Field 3", use_column_width=True)

# Map page names to functions
PAGE_FUNCTIONS = {
    "home": home,
    "personal_details": personal_details,
    "recommendations": recommendations,
    "feedback": feedback,
    "about": about,
    "contact": contact,
    "gallery": gallery
}

# Display the selected page
page = PAGES[selection]
PAGE_FUNCTIONS[page]()
        
