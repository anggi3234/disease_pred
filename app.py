import streamlit as st
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Disease Risk Prediction Demo",
    page_icon="🧬",
    layout="wide"
)

st.image("https://www.kalgeninnolab.co.id/frontend/web/images/kalgen-logo-home.png", width=120)
# Title
st.title("🧬 Disease Risk Prediction Demo")
st.write("This demo shows how genetic and lifestyle data can be used to predict disease risks.")

# Create sections
def personal_info_section():
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        height = st.number_input("Height (cm)", min_value=0, max_value=300, value=170)
        occupation = st.text_input("Occupation")
    
    with col2:
        sex = st.selectbox("Biological Sex", ["Male", "Female", "Other"])
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
        "activity_level": activity_level
    }

def physical_activity_section():
    st.header("Physical Activity Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cardio_freq = st.selectbox(
            "Cardio/aerobic exercise frequency",
            ["Never", "1-2 times per week", "3-4 times per week", "5+ times per week"]
        )
        strength_freq = st.selectbox(
            "Strength training frequency",
            ["Never", "1-2 times per week", "3-4 times per week", "5+ times per week"]
        )
    
    with col2:
        duration = st.selectbox(
            "Average exercise duration",
            ["<15 minutes", "15-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"]
        )
        intensity = st.selectbox(
            "Typical exercise intensity",
            ["Light", "Moderate", "Vigorous", "Very vigorous"]
        )
    
    return {
        "cardio_frequency": cardio_freq,
        "strength_frequency": strength_freq,
        "duration": duration,
        "intensity": intensity
    }

def lifestyle_section():
    st.header("Lifestyle Factors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = st.selectbox(
            "Average hours of sleep per night",
            ["<5", "5-6", "6-7", "7-8", "8-9", "9+"]
        )
        stress_level = st.selectbox(
            "Overall stress level",
            ["Low", "Moderate", "High", "Very high"]
        )
    
    with col2:
        smoking = st.selectbox(
            "Smoking status",
            ["Never smoked", "Former smoker", "Current smoker"]
        )
        alcohol = st.selectbox(
            "Alcohol consumption frequency",
            ["Never", "Monthly or less", "2-4 times a month", "2-3 times a week", "4+ times a week"]
        )
    
    return {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "smoking": smoking,
        "alcohol": alcohol
    }

def health_conditions_section():
    st.header("Health Status")
    
    conditions = st.multiselect(
        "Current health conditions",
        ["Hypertension", "High cholesterol", "Diabetes", "Cardiovascular disease",
         "Autoimmune condition", "Inflammatory condition", "Digestive disorders",
         "Skin conditions", "None"],
        default=["None"]
    )
    
    medications = st.text_input("Current medications (if any)")
    
    st.subheader("Symptom Assessment")
    col1, col2 = st.columns(2)
    
    symptoms = {}
    with col1:
        symptoms["fatigue"] = st.select_slider(
            "Fatigue",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["joint_pain"] = st.select_slider(
            "Joint pain",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["digestive"] = st.select_slider(
            "Digestive discomfort",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["skin_issues"] = st.select_slider(
            "Skin issues",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    
    with col2:
        symptoms["headaches"] = st.select_slider(
            "Headaches",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["mood"] = st.select_slider(
            "Mood fluctuations",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["cognitive"] = st.select_slider(
            "Cognitive difficulties",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        symptoms["sleep_issues"] = st.select_slider(
            "Sleep disturbances",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    
    return {
        "conditions": conditions,
        "medications": medications,
        "symptoms": symptoms
    }

def eating_behavior_section():
    st.header("Eating Behaviors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        emotional_eating = st.select_slider(
            "Do you often eat when stressed or emotional?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        meal_satisfaction = st.select_slider(
            "Do you feel satisfied after meals?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
    
    with col2:
        snacking = st.select_slider(
            "Do you snack between meals?",
            ["Never", "Rarely", "Sometimes", "Often", "Always"]
        )
        portion_control = st.select_slider(
            "How well do you control portion sizes?",
            ["Poor", "Fair", "Good", "Very good", "Excellent"]
        )
    
    return {
        "emotional_eating": emotional_eating,
        "meal_satisfaction": meal_satisfaction,
        "snacking": snacking,
        "portion_control": portion_control
    }

def genetic_testing_section():
    st.header("Previous Genetic Testing")
    
    had_testing = st.selectbox(
        "Have you had genetic testing before?",
        ["No", "Yes"]
    )
    
    findings = None
    if had_testing == "Yes":
        findings = st.text_area(
            "Please describe any significant findings",
            height=100
        )
    
    return {
        "had_testing": had_testing,
        "findings": findings if had_testing == "Yes" else ""
    }

def process_questionnaire_data(data):
    """Process questionnaire responses into numerical features"""
    features = {}
    
    # Process demographic features
    features['age'] = data['personal']['age']
    features['bmi'] = data['personal']['weight'] / ((data['personal']['height']/100) ** 2)
    features['gender_male'] = 1 if data['personal']['sex'] == 'Male' else 0
    
    # Process activity features
    features['met_hours'] = calculate_met_hours(data['activity'])
    
    # Process lifestyle features
    features['sleep_score'] = calculate_sleep_score(data['lifestyle'])
    features['stress_score'] = calculate_stress_score(data['lifestyle'])
    features['smoking_risk'] = calculate_smoking_risk(data['lifestyle'])
    features['alcohol_risk'] = calculate_alcohol_risk(data['lifestyle'])
    
    # Process health features
    features['health_condition_score'] = calculate_health_condition_score(data['health'])
    features['symptom_severity'] = calculate_symptom_severity(data['health'])
    features['eating_behavior_score'] = calculate_eating_behavior_score(data['eating'])
    
    return features

def calculate_met_hours(activity_data):
    """Calculate MET hours based on exercise frequency, duration and intensity"""
    # Map intensity to MET values
    intensity_to_met = {
        'Light': 2.5,
        'Moderate': 4.5,
        'Vigorous': 7.0,
        'Very vigorous': 10.0
    }
    
    # Map frequency to times per week
    freq_to_num = {
        'Never': 0,
        '1-2 times per week': 1.5,
        '3-4 times per week': 3.5,
        '5+ times per week': 5.5
    }
    
    # Map duration to hours
    duration_to_hours = {
        '<15 minutes': 0.25,
        '15-30 minutes': 0.375,
        '30-45 minutes': 0.625,
        '45-60 minutes': 0.875,
        '60+ minutes': 1.25
    }
    
    # Calculate MET hours per week
    met_value = intensity_to_met[activity_data['intensity']]
    cardio_times = freq_to_num[activity_data['cardio_frequency']]
    strength_times = freq_to_num[activity_data['strength_frequency']]
    hours = duration_to_hours[activity_data['duration']]
    
    return met_value * (cardio_times + strength_times) * hours

def calculate_sleep_score(lifestyle_data):
    """Calculate sleep score (0-1)"""
    sleep_hours_map = {
        '<5': 0.2,
        '5-6': 0.4,
        '6-7': 0.6,
        '7-8': 1.0,
        '8-9': 0.8,
        '9+': 0.6
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
        'Never smoked': 0.1,
        'Former smoker': 0.4,
        'Current smoker': 1.0
    }
    return smoking_map[lifestyle_data['smoking']]

def calculate_alcohol_risk(lifestyle_data):
    """Calculate alcohol risk score (0-1)"""
    alcohol_map = {
        'Never': 0.1,
        'Monthly or less': 0.2,
        '2-4 times a month': 0.4,
        '2-3 times a week': 0.7,
        '4+ times a week': 1.0
    }
    return alcohol_map[lifestyle_data['alcohol']]

def calculate_health_condition_score(health_data):
    """Calculate health condition risk score (0-1)"""
    if 'None' in health_data['conditions']:
        return 0.1
    
    condition_weights = {
        'Hypertension': 0.7,
        'High cholesterol': 0.6,
        'Diabetes': 0.8,
        'Cardiovascular disease': 0.9,
        'Autoimmune condition': 0.7,
        'Inflammatory condition': 0.6,
        'Digestive disorders': 0.5,
        'Skin conditions': 0.4
    }
    
    total_weight = sum(condition_weights[c] for c in health_data['conditions'] if c != 'None')
    return min(total_weight / 3, 1.0)  # Normalize to 0-1

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

def calculate_eating_behavior_score(eating_data):
    """Calculate eating behavior risk score (0-1, higher is worse)"""
    behavior_map = {
        'Never': 0,
        'Rarely': 0.25,
        'Sometimes': 0.5,
        'Often': 0.75,
        'Always': 1.0
    }
    
    emotional_eating_score = behavior_map[eating_data['emotional_eating']]
    snacking_score = behavior_map[eating_data['snacking']]
    
    # Reverse scale for positive behaviors
    satisfaction_score = 1 - behavior_map[eating_data['meal_satisfaction']]
    
    portion_control_map = {
        'Poor': 1.0,
        'Fair': 0.75,
        'Good': 0.5,
        'Very good': 0.25,
        'Excellent': 0
    }
    portion_score = portion_control_map[eating_data['portion_control']]
    
    return (emotional_eating_score + snacking_score + satisfaction_score + portion_score) / 4

def calculate_risk_scores(features):
    """Calculate risk scores for different health aspects"""
    risk_scores = {}
    
    # Metabolic health risk
    metabolic_risk = (
        0.3 * max(0, (features['bmi'] - 18.5) / (30 - 18.5)) +  # BMI contribution
        0.2 * (1 - min(features['met_hours'] / 40, 1)) +  # Activity contribution
        0.2 * features['eating_behavior_score'] +  # Eating behavior contribution
        0.15 * features['stress_score'] +  # Stress contribution
        0.1 * features['smoking_risk'] +  # Smoking contribution
        0.05 * features['alcohol_risk']  # Alcohol contribution
    )
    risk_scores['metabolic_health'] = max(0, min(1, metabolic_risk))
    
    # Cardiovascular risk
    cv_risk = (
        0.25 * (features['age'] - 20) / (80 - 20) +  # Age contribution
        0.2 * (1 - min(features['met_hours'] / 40, 1)) +  # Activity contribution
        0.2 * features['stress_score'] +  # Stress contribution
        0.15 * features['smoking_risk'] +  # Smoking contribution
        0.1 * features['alcohol_risk'] +  # Alcohol contribution
        0.1 * features['health_condition_score']  # Existing conditions contribution
    )
    risk_scores['cardiovascular'] = max(0, min(1, cv_risk))
    
    # Sleep and recovery risk
    recovery_risk = (
        0.35 * (1 - features['sleep_score']) +  # Sleep contribution
        0.3 * features['stress_score'] +  # Stress contribution
        0.25 * features['symptom_severity'] +  # Symptoms contribution
        0.1 * (1 - min(features['met_hours'] / 40, 1))  # Activity contribution
    )
    risk_scores['sleep_recovery'] = max(0, min(1, recovery_risk))
    
    # Lifestyle risk
    lifestyle_risk = (
        0.3 * features['smoking_risk'] +  # Smoking contribution
        0.25 * features['alcohol_risk'] +  # Alcohol contribution
        0.25 * features['stress_score'] +  # Stress contribution
        0.2 * features['symptom_severity']  # Symptoms contribution
    )
    risk_scores['lifestyle'] = max(0, min(1, lifestyle_risk))
    
    return risk_scores

def generate_recommendations(risk_scores, features):
    """Generate personalized recommendations based on risk assessment"""
    recommendations = []
    
    # Metabolic health recommendations
    if risk_scores['metabolic_health'] > 0.6:
        recs = [
            "Aim for 150 minutes of moderate exercise per week",
            "Monitor portion sizes and meal timing",
            "Consider consulting a nutritionist for personalized dietary advice"
        ]
        if features['eating_behavior_score'] > 0.6:
            recs.append("Practice mindful eating techniques")
            recs.append("Keep a food diary to track emotional eating triggers")
        if features['bmi'] > 25:
            recs.append("Focus on gradual, sustainable weight management")
        recommendations.append({
            'category': 'Metabolic Health',
            'recommendations': recs
        })
    
    # Cardiovascular recommendations
    if risk_scores['cardiovascular'] > 0.6:
        recs = [
            "Increase aerobic exercise frequency",
            "Consider stress management techniques",
            "Monitor blood pressure regularly"
        ]
        if features['health_condition_score'] > 0.6:
            recs.append("Regular cardiovascular health monitoring with healthcare provider")
        if features['smoking_risk'] > 0.5:
            recs.append("Consider smoking cessation programs")
        recommendations.append({
            'category': 'Cardiovascular Health',
            'recommendations': recs
        })
    
    # Sleep and recovery recommendations
    if risk_scores['sleep_recovery'] > 0.6:
        recs = [
            "Establish a consistent sleep schedule",
            "Practice relaxation techniques before bed",
            "Limit screen time in the evening"
        ]
        if features['symptom_severity'] > 0.6:
            recs.append("Consider consulting a sleep specialist")
        if features['stress_score'] > 0.6:
            recs.append("Explore stress management techniques like meditation or yoga")
        recommendations.append({
            'category': 'Sleep & Recovery',
            'recommendations': recs
        })
    
    # Lifestyle recommendations
    if risk_scores['lifestyle'] > 0.6:
        recs = []
        if features['smoking_risk'] > 0.5:
            recs.extend([
                "Consider smoking cessation programs",
                "Seek support from healthcare providers for quitting smoking"
            ])
        if features['alcohol_risk'] > 0.6:
            recs.extend([
                "Consider reducing alcohol consumption",
                "Explore alcohol-free social activities"
            ])
        if features['stress_score'] > 0.6:
            recs.extend([
                "Practice daily stress management techniques",
                "Consider counseling or therapy for stress management"
            ])
        if recs:
            recommendations.append({
                'category': 'Lifestyle Health',
                'recommendations': recs
            })
    
    return recommendations

def display_results(risk_scores, recommendations):
    """Display risk scores and recommendations"""
    st.header("Your Health Risk Assessment")
    
    # Display risk scores with color-coded indicators
    st.write("Risk scores are categorized as: Low (< 40%), Moderate (40-60%), High (> 60%)")
    
    col1, col2 = st.columns(2)
    
    def display_risk_metric(label, value):
        # Display the metric
        st.metric(
            label, 
            f"{value*100:.1f}%"
        )
        
        # Display risk level using Streamlit's native components
        risk_level = "Low" if value < 0.4 else "Moderate" if value < 0.6 else "High"
        if value < 0.4:
            st.success(f"Risk Level: {risk_level}")
        elif value < 0.6:
            st.warning(f"Risk Level: {risk_level}")
        else:
            st.error(f"Risk Level: {risk_level}")
    
    with col1:
        display_risk_metric("Metabolic Health Risk", risk_scores['metabolic_health'])
        st.divider()
        display_risk_metric("Cardiovascular Risk", risk_scores['cardiovascular'])
    
    with col2:
        display_risk_metric("Sleep & Recovery Risk", risk_scores['sleep_recovery'])
        st.divider()
        display_risk_metric("Lifestyle Risk", risk_scores['lifestyle'])
    
    st.header("Your Personalized Health Recommendations")
    
    if not recommendations:
        st.info("Great news! Your risk levels are low. Keep maintaining your healthy lifestyle!")
    else:
        for category in recommendations:
            with st.expander(f"🎯 {category['category']} Recommendations", expanded=True):
                st.subheader("Why these recommendations?")
                if category['category'] == 'Metabolic Health':
                    st.write("These recommendations focus on optimizing your metabolism through exercise and lifestyle changes. Following these guidelines can help maintain healthy weight, blood sugar levels, and overall metabolic function.")
                elif category['category'] == 'Cardiovascular Health':
                    st.write("Heart health is influenced by multiple factors including exercise, stress, and lifestyle choices. These recommendations aim to support your cardiovascular system and reduce risk factors.")
                elif category['category'] == 'Sleep & Recovery':
                    st.write("Quality sleep and proper recovery are essential for overall health, immune function, and mental well-being. These suggestions can help improve your sleep quality and stress management.")
                elif category['category'] == 'Lifestyle Health':
                    st.write("Lifestyle factors like smoking, alcohol consumption, and stress management significantly impact your overall health. These recommendations help address key lifestyle risk factors.")
                
                st.subheader("Action Steps")
                for i, rec in enumerate(category['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                
                st.subheader("Implementation Tips")
                if category['category'] == 'Metabolic Health':
                    st.write("• Start with small changes and gradually build up")
                    st.write("• Use a food diary to track meals and portions")
                    st.write("• Plan meals in advance to make healthy choices easier")
                    st.write("• Stay hydrated throughout the day")
                elif category['category'] == 'Cardiovascular Health':
                    st.write("• Begin with walking and gradually increase intensity")
                    st.write("• Monitor your heart rate during exercise")
                    st.write("• Practice stress-reduction techniques daily")
                    st.write("• Consider joining a fitness group for motivation")
                elif category['category'] == 'Sleep & Recovery':
                    st.write("• Create a consistent bedtime routine")
                    st.write("• Make your bedroom dark, quiet, and cool")
                    st.write("• Avoid screens 1-2 hours before bed")
                    st.write("• Practice relaxation techniques before sleep")
                elif category['category'] == 'Lifestyle Health':
                    st.write("• Set specific, achievable goals for lifestyle changes")
                    st.write("• Build a support network for accountability")
                    st.write("• Consider professional help when needed")
                    st.write("• Celebrate small victories in your health journey")
    
    st.header("Track Your Progress")
    st.write("To improve your health outcomes:")
    st.write("1. Save these recommendations for reference")
    st.write("2. Start with 1-2 changes that feel most manageable")
    st.write("3. Track your progress daily or weekly")
    st.write("4. Retake this assessment in 3-6 months to monitor improvements")
    
    if recommendations:
        report = "Your Health Recommendations\n\n"
        for category in recommendations:
            report += f"\n{category['category']}:\n"
            for rec in category['recommendations']:
                report += f"- {rec}\n"
        
        st.download_button(
            label="Download Recommendations",
            data=report,
            file_name="health_recommendations.txt",
            mime="text/plain"
        )

# Main app flow
def main():
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Questionnaire", "Results"])
    
    with tab1:
        with st.form("health_questionnaire"):
            # Collect data from each section
            personal_data = personal_info_section()
            activity_data = physical_activity_section()
            lifestyle_data = lifestyle_section()
            health_data = health_conditions_section()
            eating_data = eating_behavior_section()
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
                    'eating': eating_data,
                    'genetic': genetic_data
                }
                st.session_state.show_results = True
                
                # Show success message and redirect instruction
                st.success("✅ Risk scores calculated successfully!")
                st.info("👆 **Please click on the 'Results' tab above to view your personalized health assessment and recommendations.**")
                st.balloons()  # Add a celebratory animation
    
    with tab2:
        if 'show_results' in st.session_state and st.session_state.show_results:
            # Process the data
            features = process_questionnaire_data(st.session_state.questionnaire_data)
            
            # Calculate risk scores
            risk_scores = calculate_risk_scores(features)
            
            # Generate recommendations
            recommendations = generate_recommendations(risk_scores, features)
            
            # Display results
            display_results(risk_scores, recommendations)
        else:
            st.info("Please complete the questionnaire to see your results.")

if __name__ == "__main__":
    main()