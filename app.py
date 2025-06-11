import streamlit as st
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import math

# Set page config
st.set_page_config(
    page_title="Disease Risk Prediction Demo",
    page_icon="🧬",
    layout="wide"
)

st.image("https://www.kalgeninnolab.co.id/frontend/web/images/kalgen-logo-home.png", width=120)
# Title
st.title("🧬 Disease Risk Prediction")
st.write("Find out how your lifestyle and health conditions can be used to predict disease risks.")

# Create sections
def personal_info_section():
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        height = st.number_input("Height (cm)", min_value=0, max_value=300, value=170)
        occupation = st.text_input("Occupation")
        waist_circumference = st.number_input("Waist Circumference (cm)", min_value=0, max_value=200, value=80)
    
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=0, max_value=500, value=70)
        activity_level = st.selectbox(
            "Work Activity Level",
            ["Sedentary", "Lightly active", "Moderately active", "Very active"]
        )
    
    return {
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "occupation": occupation,
        "activity_level": activity_level,
        "waist_circumference": waist_circumference
    }

def physical_activity_section():
    st.header("Exercise Frequencies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exercise_freq = st.selectbox(
            "Exercise frequency (combined cardio and strength)",
            ["Never", "1-2 times per week", "3-4 times per week", "5+ times per week"]
        )
    
    with col2:
        duration = st.selectbox(
            "Average exercise duration",
            ["<15 minutes", "15-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"]
        )
        intensity = st.selectbox(
            "Typical exercise intensity",
            ["Light", "Medium", "Vigorous", "Very vigorous"]
        )
    
    return {
        "exercise_frequency": exercise_freq,
        "duration": duration,
        "intensity": intensity
    }

def lifestyle_section():
    st.header("Lifestyle Factors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = st.selectbox(
            "Average hours of sleep per night",
            ["< 5 hours (insufficient)", "5-7 hours (below optimal)", "7-9 hours (optimal)", "9+ hours (excessive)"], 
            key="sleep_hours"
        )
        stress_level = st.selectbox(
            "Overall stress level",
            ["Low", "Moderate", "High", "Very high"], key="stress_level"
        )
        total_cholesterol = st.selectbox(
            "Total Cholesterol Level",
            ["Low (<200 mg/dL)", "Medium (200-239 mg/dL)", "High (≥240 mg/dL)", "Unknown"]
        )
        blood_pressure_medication = st.selectbox(
            "Use of blood pressure lowering medications",
            ["No", "Not routine", "Yes routinely"]
        )
    
    with col2:
        smoking = st.selectbox(
            "Smoking status",
            ["Non-smoker", "Passive smoker", "Active smoker"]
        )
        alcohol = st.selectbox(
            "Alcohol consumption",
            ["No", "Yes"]
        )
        hba1c = st.number_input("HbA1c level (%)", min_value=0.0, max_value=20.0, value=5.5, step=0.1)
        fasting_glucose = st.number_input("Fasting glucose (mg/dL)", min_value=0, max_value=500, value=90)

    # Other symptoms
    st.subheader("Other Symptoms")
    col3, col4 = st.columns(2)
    
    with col3:
        frequent_hunger = st.radio(
            "Frequent hunger", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="frequent_hunger"
        )
        frequent_thirst = st.radio(
            "Frequent thirst", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="frequent_thirst"
        )
    
    with col4:
        frequent_urination = st.radio(
            "Frequent urination", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="frequent_urination"
        )
    
    return {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "smoking": smoking,
        "alcohol": alcohol,
        "total_cholesterol": total_cholesterol,
        "blood_pressure_medication": blood_pressure_medication,
        "hba1c": hba1c,
        "fasting_glucose": fasting_glucose,
        "frequent_hunger": frequent_hunger,
        "frequent_thirst": frequent_thirst,
        "frequent_urination": frequent_urination
    }

def health_conditions_section():
    st.header("Health Status")
    
    conditions = st.multiselect(
        "Current health conditions",
        ["Hypertension", "High cholesterol", "Diabetes", "Cardiovascular disease", "Cancer",
         "Autoimmune condition", "Inflammatory condition", "Digestive disorders",
         "Skin conditions", "None"],
        default=["None"]
    )
    
    # Remove "None" if other conditions are selected (without rerun)
    if len(conditions) > 1 and "None" in conditions:
        conditions = [c for c in conditions if c != "None"]
        # Show a message instead of forcing rerun
        st.info("ℹ️ 'None' has been automatically removed since you selected other conditions.")
    
    medications = st.text_input("Current medications (if any)")
    
    # Family History
    st.subheader("Family History")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Diabetes History**")
        diabetes_history = st.selectbox(
            "Family history of diabetes",
            ["None", "Grandparent affected", "Parent affected", "Sibling affected"],
            key="diabetes_history"
        )
    
    with col2:
        st.write("**Cancer History**")
        cancer_history = st.selectbox(
            "Family history of cancer",
            ["None", "Grandparent affected", "Parent affected", "Sibling affected"],
            key="cancer_history"
        )
    
    with col3:
        st.write("**CVD History**")
        cvd_history = st.selectbox(
            "Family history of cardiovascular disease",
            ["None", "Grandparent affected", "Parent affected", "Sibling affected"],
            key="cvd_history"
        )
    
    st.subheader("Well & Fit Assessment")
    col1, col2 = st.columns(2)
    
    symptoms = {}
    with col1:
        symptoms["fatigue"] = st.radio(
            "Fatigue", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="fatigue"
        )
        symptoms["joint_pain"] = st.radio(
            "Joint pain", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="joint_pain"
        )
        symptoms["digestive"] = st.radio(
            "Digestive discomfort", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="digestive"
        )
        symptoms["skin_issues"] = st.radio(
            "Skin issues", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="skin_issues"
        )
    
    with col2:
        symptoms["headaches"] = st.radio(
            "Headaches", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="headaches"
        )
        symptoms["mood"] = st.radio(
            "Mood fluctuations", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="mood"
        )
        symptoms["cognitive"] = st.radio(
            "Cognitive difficulties", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="cognitive"
        )
        symptoms["sleep_issues"] = st.radio(
            "Sleep disturbances", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="sleep_issues"
        )
    
    return {
        "conditions": conditions,
        "medications": medications,
        "diabetes_history": diabetes_history,
        "cancer_history": cancer_history,
        "cvd_history": cvd_history,
        "symptoms": symptoms
    }

def genetic_testing_section():
    st.header("Previous Genetic Testing")
    
    had_testing = st.selectbox(
        "Have you had genetic testing before?",
        ["No", "Yes"]
    )
    
    findings = ""
    if had_testing == "Yes":
        findings = st.text_area(
            "Please describe any significant findings",
            height=100
        )
    
    return {
        "had_testing": had_testing,
        "findings": findings
    }

def process_questionnaire_data(data):
    """Process questionnaire responses into numerical features"""
    features = {}
    
    # Process demographic features
    features['age'] = data['personal']['age']
    features['bmi'] = data['personal']['weight'] / ((data['personal']['height']/100) ** 2)
    features['gender_male'] = 1 if data['personal']['sex'] == 'Male' else 0
    features['waist_circumference'] = data['personal']['waist_circumference']
    
    # Process activity features
    features['met_hours'] = calculate_met_hours(data['activity'])
    
    # Process lifestyle features
    features['sleep_score'] = calculate_sleep_score(data['lifestyle'])
    features['stress_score'] = calculate_stress_score(data['lifestyle'])
    features['smoking_risk'] = calculate_smoking_risk(data['lifestyle'])
    features['alcohol_risk'] = 1 if data['lifestyle']['alcohol'] == 'Yes' else 0
    features['total_cholesterol'] = map_cholesterol_level(data['lifestyle']['total_cholesterol'])
    features['bp_medication'] = map_bp_medication(data['lifestyle']['blood_pressure_medication'])
    features['hba1c'] = data['lifestyle']['hba1c']
    features['fasting_glucose'] = data['lifestyle']['fasting_glucose']
    features['diabetes_symptoms'] = calculate_diabetes_symptoms(data['lifestyle'])
    
    # Process health features
    features['health_condition_score'] = calculate_health_condition_score(data['health'])
    features['symptom_severity'] = calculate_symptom_severity(data['health'])
    features['diabetes_family_history'] = map_family_history(data['health']['diabetes_history'])
    features['cancer_family_history'] = map_family_history(data['health']['cancer_history'])
    features['cvd_family_history'] = map_family_history(data['health']['cvd_history'])
    
    # Current conditions flags
    features['has_diabetes'] = 'Diabetes' in data['health']['conditions']
    features['has_cvd'] = 'Cardiovascular disease' in data['health']['conditions']
    features['has_cancer'] = 'Cancer' in data['health']['conditions']
    
    return features

def calculate_met_hours(activity_data):
    """Calculate MET hours based on exercise frequency, duration and intensity"""
    intensity_to_met = {
        'Light': 2.5,
        'Medium': 4.5,
        'Vigorous': 7.0,
        'Very vigorous': 10.0
    }
    
    freq_to_num = {
        'Never': 0,
        '1-2 times per week': 1.5,
        '3-4 times per week': 3.5,
        '5+ times per week': 5.5
    }
    
    duration_to_hours = {
        '<15 minutes': 0.25,
        '15-30 minutes': 0.375,
        '30-45 minutes': 0.625,
        '45-60 minutes': 0.875,
        '60+ minutes': 1.25
    }
    
    met_value = intensity_to_met[activity_data['intensity']]
    exercise_times = freq_to_num[activity_data['exercise_frequency']]
    hours = duration_to_hours[activity_data['duration']]
    
    return met_value * exercise_times * hours

def calculate_sleep_score(lifestyle_data):
    """Calculate sleep score (0-1)"""
    sleep_hours_map = {
        '< 5 hours (insufficient)': 0.2,
        '5-7 hours (below optimal)': 0.6,
        '7-9 hours (optimal)': 1.0,
        '9+ hours (excessive)': 0.6
    }
    return sleep_hours_map[lifestyle_data['sleep_hours']]

def calculate_stress_score(lifestyle_data):
    """Calculate stress score (0-1, higher is worse)"""
    stress_map = {
        'Low': 0.2,
        'Moderate': 0.4,
        'High': 0.7,
        'Very high': 1.0
    }
    return stress_map[lifestyle_data['stress_level']]

def calculate_smoking_risk(lifestyle_data):
    """Calculate smoking risk score (0-1)"""
    smoking_map = {
        'Non-smoker': 0.0,
        'Passive smoker': 0.3,
        'Active smoker': 1.0
    }
    return smoking_map[lifestyle_data['smoking']]

def map_cholesterol_level(cholesterol_str):
    """Map cholesterol level to numerical value"""
    cholesterol_map = {
        'Low (<200 mg/dL)': 180,
        'Medium (200-239 mg/dL)': 220,
        'High (≥240 mg/dL)': 260,
        'Unknown': 200  # Use average value
    }
    return cholesterol_map[cholesterol_str]

def map_bp_medication(bp_med_str):
    """Map BP medication to numerical value"""
    bp_map = {
        'No': 0,
        'Not routine': 0.5,
        'Yes routinely': 1
    }
    return bp_map[bp_med_str]

def calculate_diabetes_symptoms(lifestyle_data):
    """Calculate diabetes symptoms score"""
    symptom_map = {
        'Never': 0,
        'Rarely': 0.25,
        'Sometimes': 0.5,
        'Often': 0.75,
        'Always': 1.0
    }
    
    hunger_score = symptom_map[lifestyle_data['frequent_hunger']]
    thirst_score = symptom_map[lifestyle_data['frequent_thirst']]
    urination_score = symptom_map[lifestyle_data['frequent_urination']]
    
    return (hunger_score + thirst_score + urination_score) / 3

def map_family_history(history_str):
    """Map family history to weighted score"""
    history_map = {
        'None': 0,
        'Grandparent affected': 1,
        'Parent affected': 2,
        'Sibling affected': 3
    }
    return history_map[history_str]

def calculate_health_condition_score(health_data):
    """Calculate health condition risk score (0-1)"""
    if 'None' in health_data['conditions']:
        return 0.1
    
    condition_weights = {
        'Hypertension': 0.7,
        'High cholesterol': 0.6,
        'Diabetes': 0.8,
        'Cardiovascular disease': 0.9,
        'Cancer': 0.9,
        'Autoimmune condition': 0.7,
        'Inflammatory condition': 0.6,
        'Digestive disorders': 0.5,
        'Skin conditions': 0.4
    }
    
    total_weight = sum(condition_weights[c] for c in health_data['conditions'] if c != 'None')
    return min(total_weight / 3, 1.0)

def calculate_symptom_severity(health_data):
    """Calculate symptom severity score (0-1)"""
    severity_map = {
        'Never': 0,
        'Rarely': 0.25,
        'Sometimes': 0.5,
        'Often': 0.75,
        'Always': 1.0
    }
    
    symptoms = health_data['symptoms']
    total_severity = sum(severity_map[v] for v in symptoms.values())
    return total_severity / len(symptoms)

def calculate_framingham_risk_score(features):
    """Calculate Framingham Risk Score for CVD"""
    age = features['age']
    is_male = features['gender_male']
    total_chol = features['total_cholesterol']
    smoking = features['smoking_risk']
    bp_meds = features['bp_medication']
    
    # Simplified Framingham calculation
    risk_score = 0
    
    # Age points
    if is_male:
        if age >= 70: risk_score += 11
        elif age >= 65: risk_score += 10
        elif age >= 60: risk_score += 8
        elif age >= 55: risk_score += 6
        elif age >= 50: risk_score += 4
        elif age >= 45: risk_score += 3
        elif age >= 40: risk_score += 2
        elif age >= 35: risk_score += 1
    else:  # Female
        if age >= 75: risk_score += 16
        elif age >= 70: risk_score += 12
        elif age >= 65: risk_score += 9
        elif age >= 60: risk_score += 7
        elif age >= 55: risk_score += 4
        elif age >= 50: risk_score += 3
        elif age >= 45: risk_score += 2
        elif age >= 40: risk_score += 1
    
    # Cholesterol points
    if total_chol >= 280:
        risk_score += 3 if is_male else 4
    elif total_chol >= 240:
        risk_score += 2 if is_male else 2
    elif total_chol >= 200:
        risk_score += 1 if is_male else 1
    
    # Smoking
    if smoking > 0.5:  # Active smoker
        risk_score += 4 if is_male else 3
    
    # BP medication
    if bp_meds > 0.5:
        risk_score += 2
    
    # Convert to probability (simplified)
    probability = min(risk_score / 20.0, 1.0)
    return probability

def calculate_risk_scores(features):
    """Calculate risk scores for different health aspects"""
    risk_scores = {}
    
    # Metabolic and Lifestyle Risk
    metabolic_risk = (
        0.25 * max(0, (features['bmi'] - 18.5) / (30 - 18.5)) +
        0.2 * (1 - min(features['met_hours'] / 40, 1)) +
        0.2 * features['stress_score'] +
        0.15 * features['smoking_risk'] +
        0.1 * features['alcohol_risk'] +
        0.1 * (1 - features['sleep_score'])
    )
    risk_scores['metabolic_lifestyle'] = max(0, min(1, metabolic_risk))
    
    # CVD & Stroke Risk (Framingham-based)
    if not features['has_cvd']:
        cvd_risk = calculate_framingham_risk_score(features)
        # Add family history
        cvd_risk += features['cvd_family_history'] * 0.1
        risk_scores['cvd_stroke'] = max(0, min(1, cvd_risk))
    
    # Diabetes Risk
    if not features['has_diabetes']:
        # Adjust waist circumference if zero
        waist_adj = features['waist_circumference'] if features['waist_circumference'] > 0 else 80
        
        diabetes_risk = (
            0.25 * max(0, (features['bmi'] - 18.5) / (35 - 18.5)) +
            0.2 * max(0, (waist_adj - 70) / (120 - 70)) +
            0.15 * (1 if features['hba1c'] >= 6.0 else features['hba1c'] / 6.0) +
            0.15 * (1 if features['fasting_glucose'] > 120 else features['fasting_glucose'] / 120) +
            0.1 * (1 - min(features['met_hours'] / 40, 1)) +
            0.05 * features['diabetes_family_history'] * 0.1 +
            0.1 * features['diabetes_symptoms']
        )
        risk_scores['diabetes'] = max(0, min(1, diabetes_risk))
    
    # Cancer Risk
    if not features['has_cancer']:
        cancer_risk = (
            0.3 * (features['age'] - 20) / (80 - 20) +
            0.25 * features['smoking_risk'] +
            0.2 * features['alcohol_risk'] +
            0.15 * max(0, (features['bmi'] - 18.5) / (35 - 18.5)) +
            0.1 * features['cancer_family_history'] * 0.1
        )
        risk_scores['cancer'] = max(0, min(1, cancer_risk))
    
    return risk_scores

def generate_recommendations(risk_scores, features):
    """Generate personalized recommendations based on risk assessment"""
    recommendations = []
    
    # Metabolic & Lifestyle recommendations (Genme Life)
    if 'metabolic_lifestyle' in risk_scores and risk_scores['metabolic_lifestyle'] >= 0.4:
        recs = [
            "Follow Genme Life health recommendations for metabolic optimization",
            "Increase physical activity to 150 minutes of moderate exercise per week",
            "Implement stress management techniques like meditation or yoga",
            "Maintain consistent sleep schedule for 7-9 hours per night"
        ]
        if features['bmi'] > 25:
            recs.append("Focus on gradual, sustainable weight management")
        if features['smoking_risk'] > 0.5:
            recs.append("Consider smoking cessation programs")
        recommendations.append({
            'category': 'Metabolic & Lifestyle Risk (Genme Life)',
            'recommendations': recs
        })
    
    # CVD & Stroke recommendations
    if 'cvd_stroke' in risk_scores and risk_scores['cvd_stroke'] >= 0.3:  # Lower cutoff for sensitivity
        recs = [
            "Follow Strokegenme guidance for cardiovascular health",
            "Schedule regular lipid panel blood checkups",
            "Monitor blood pressure regularly",
            "Increase aerobic exercise frequency"
        ]
        if features['smoking_risk'] > 0.5:
            recs.append("Smoking cessation is critical for heart health")
        if features['stress_score'] > 0.6:
            recs.append("Implement cardiovascular-protective stress management")
        recommendations.append({
            'category': 'CVD & Stroke Risk',
            'recommendations': recs
        })
    
    # Diabetes recommendations
    if 'diabetes' in risk_scores and risk_scores['diabetes'] >= 0.4:
        recs = [
            "Schedule immediate medical checkup with HbA1c and fasting glucose tests",
            "Monitor blood glucose levels regularly",
            "Follow diabetes prevention dietary guidelines",
            "Increase physical activity to improve insulin sensitivity"
        ]
        if features['bmi'] > 25:
            recs.append("Weight management is crucial for diabetes prevention")
        if features['diabetes_symptoms'] > 0.5:
            recs.append("Discuss diabetes symptoms with healthcare provider immediately")
        recommendations.append({
            'category': 'Diabetes Risk',
            'recommendations': recs
        })
    
    # Cancer recommendations (SpotMas)
    if 'cancer' in risk_scores and risk_scores['cancer'] >= 0.3:  # Lower cutoff for early detection
        recs = [
            "Consider SpotMas screening for early cancer detection",
            "Schedule KalScreen 69 testing panels",
            "Maintain regular cancer screening as per age guidelines",
            "Adopt cancer-preventive lifestyle modifications"
        ]
        if features['smoking_risk'] > 0.5:
            recs.append("Smoking cessation significantly reduces cancer risk")
        if features['alcohol_risk'] > 0.5:
            recs.append("Consider reducing alcohol consumption")
        recommendations.append({
            'category': 'Cancer Risk (SpotMas)',
            'recommendations': recs
        })
    
    return recommendations

def display_results(risk_scores, recommendations):
    """Display risk scores and recommendations"""
    st.header("Your Health Risk Assessment")
    
    st.write("Risk scores are categorized as: Low (< 40%), Moderate (40-60%), High (> 60%)")
    
    # Always display all 4 categories in the same order
    all_categories = [
        ('Metabolic & Lifestyle Risk', 'metabolic_lifestyle'),
        ('CVD & Stroke Risk', 'cvd_stroke'),
        ('Diabetes Risk', 'diabetes'),
        ('Cancer Risk', 'cancer')
    ]
    
    # Create 4 columns for the 4 categories
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    def display_risk_metric(label, risk_key, col):
        with col:
            if risk_key in risk_scores:
                value = risk_scores[risk_key]
                st.metric(label, f"{value*100:.1f}%")
                risk_level = "Low" if value < 0.4 else "Moderate" if value < 0.6 else "High"
                if value < 0.4:
                    st.success(f"Risk Level: {risk_level}")
                elif value < 0.6:
                    st.warning(f"Risk Level: {risk_level}")
                else:
                    st.error(f"Risk Level: {risk_level}")
            else:
                # Show N/A for categories that don't apply
                st.metric(label, "N/A")
                st.info("Risk Level: N/A (Condition present)")
    
    # Display all 4 categories
    for i, (label, risk_key) in enumerate(all_categories):
        display_risk_metric(label, risk_key, cols[i])
    
    st.header("Your Personalized Health Recommendations")
    
    # Create sections for each category
    for category_name, risk_key in [
        ('Metabolic & Lifestyle Risk (Genme Life)', 'metabolic_lifestyle'),
        ('CVD & Stroke Risk', 'cvd_stroke'),
        ('Diabetes Risk', 'diabetes'),
        ('Cancer Risk (SpotMas)', 'cancer')
    ]:
        st.subheader(f"🎯 {category_name}")
        
        # Create 2 columns for recommendations and product image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Recommendations:**")
            
            # Check if this category has specific recommendations
            category_recommendations = None
            for rec_cat in recommendations:
                if rec_cat['category'] == category_name:
                    category_recommendations = rec_cat['recommendations']
                    break
            
            if category_recommendations:
                # Show specific recommendations for moderate/high risk
                for i, rec in enumerate(category_recommendations, 1):
                    st.write(f"{i}. {rec}")
            elif risk_key in risk_scores:
                # Show general recommendations for low risk
                if risk_key == 'metabolic_lifestyle':
                    st.write("1. Continue maintaining your healthy lifestyle")
                    st.write("2. Regular exercise and balanced nutrition")
                    st.write("3. Monitor stress levels and sleep quality")
                elif risk_key == 'cvd_stroke':
                    st.write("1. Maintain heart-healthy lifestyle")
                    st.write("2. Regular cardiovascular check-ups")
                    st.write("3. Monitor blood pressure and cholesterol")
                elif risk_key == 'diabetes':
                    st.write("1. Maintain healthy blood sugar levels")
                    st.write("2. Regular glucose monitoring")
                    st.write("3. Balanced diet and regular exercise")
                elif risk_key == 'cancer':
                    st.write("1. Continue cancer prevention practices")
                    st.write("2. Regular screening as per age guidelines")
                    st.write("3. Maintain healthy lifestyle habits")
            else:
                # Category not applicable (condition already present)
                st.write("1. Follow your healthcare provider's treatment plan")
                st.write("2. Regular monitoring and check-ups")
                st.write("3. Maintain prescribed medications")
        
        with col2:
            st.write("**Recommended Product:**")
            
            # Simple logic for image display as requested
            image_path = 'assets/MCU.jpg'  # Default
            caption = "General Health Screening"
            
            if risk_key == 'diabetes':
                image_path = 'assets/MCU.jpg'
                caption = "MCU Health Screening"
            elif risk_key == 'cvd_stroke' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/StrokeGENME.png'
                caption = "StrokeGENME - CVD Prevention"
            elif risk_key == 'cancer' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/Kalscanner69.png'
                caption = "Kalscanner69 - Cancer Screening"
            elif risk_key == 'metabolic_lifestyle' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/GENME_LIFE.png'
                caption = "GENME Life - Metabolic Health"
            
            try:
                st.image(image_path, caption=caption, use_container_width=True)
            except:
                st.error(f"Image not found: {image_path}")
        
        st.divider()
    
    # Action buttons
    st.header("Take Action")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Informasi Produk", use_container_width=True):
            st.markdown("[Contact Customer Relations](https://wa.me/your_whatsapp_number)")
    
    with col2:
        if st.button("🧪 Test Now", use_container_width=True):
            st.markdown("[Book Your Test](https://wa.me/your_whatsapp_number)")
    
    with col3:
        if st.button("🎁 Cek Promo", use_container_width=True):
            st.markdown("[Check Promotions](https://wa.me/your_whatsapp_number)")

# Main app flow
def main():
    # Initialize session state
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Check if results should be shown and auto-select Results tab
    if st.session_state.show_results:
        # Show results directly without tabs when calculation is complete
        st.header("📊 Your Health Risk Assessment Results")
        
        # Add a button to go back to questionnaire
        if st.button("🔙 Back to Questionnaire"):
            st.session_state.show_results = False
            st.rerun()
        
        # Process and display results
        features = process_questionnaire_data(st.session_state.questionnaire_data)
        risk_scores = calculate_risk_scores(features)
        recommendations = generate_recommendations(risk_scores, features)
        display_results(risk_scores, recommendations)
        
    else:
        # Show questionnaire form
        st.header("📝 Health Risk Assessment Questionnaire")
        
        with st.form("health_questionnaire"):
            # Collect data from each section
            personal_data = personal_info_section()
            activity_data = physical_activity_section()
            lifestyle_data = lifestyle_section()
            health_data = health_conditions_section()
            genetic_data = genetic_testing_section()
            
            # Submit button
            submitted = st.form_submit_button("Calculate Risk Scores", icon=":material/check_circle:")
            
            if submitted:
                # Store the collected data
                st.session_state.questionnaire_data = {
                    'personal': personal_data,
                    'activity': activity_data,
                    'lifestyle': lifestyle_data,
                    'health': health_data,
                    'genetic': genetic_data
                }
                st.session_state.show_results = True
                
                # Show success message and rerun to show results
                st.success("✅ Risk scores calculated successfully!")
                st.balloons()
                st.rerun()

if __name__ == "__main__":
    main()