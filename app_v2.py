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

# --- LANGUAGE DICTIONARY ---
LANG = {
    'en': {
        # UI Header Titles
        'title': "🧬 Disease Risk Prediction",
        'subtitle': "Find out how your lifestyle and health conditions can be used to predict disease risks.",
        'form_title': "📝 Health Risk Assessment Questionnaire",
        'results_title': "📊 Your Health Risk Assessment Results",
        'back_button': "🔙 Back to Questionnaire",
        'success_msg': "✅ Risk scores calculated successfully!",
        'personal_info': "Personal Information",
        'exercise_header': "Exercise Frequencies",
        'lifestyle_header': "Lifestyle Factors",
        'health_header': "Health Status",
        'family_history': "Family History",
        'genetic_header': "Previous Genetic Testing",
        'recommendation_header': "Your Personalized Health Recommendations",
        'take_action_header': "Take Action",
        'result_header': "Your Health Risk Assessment",
        'result_subtext': "Risk scores are categorized as: Low (< 40%), Moderate (40-60%), High (> 60%)",

        # Personal
        'age': "Age",
        'height': "Height (cm)",
        'weight': "Weight (kg)",
        'waist': "Waist Circumference (cm)",
        'occupation': "Occupation",
        'sex': "Sex",
        'sex_options': ["Male", "Female"],
        'activity_level': "Work Activity Level",
        'activity_options': ["Sedentary", "Lightly active", "Moderately active", "Very active"],

        # Exercise
        'exercise_freq': "Exercise frequency (combined cardio and strength)",
        'exercise_duration': "Average exercise duration",
        'exercise_intensity': "Typical exercise intensity",

        # Lifestyle
        'sleep_hours': "Average hours of sleep per night",
        'stress_level': "Overall stress level",
        'cholesterol_level': "Total Cholesterol Level",
        'bp_meds': "Use of blood pressure lowering medications",
        'smoking_status': "Smoking status",
        'alcohol_use': "Alcohol consumption",
        'hba1c_label': "HbA1c level (%)",
        'fasting_glucose': "Fasting glucose (mg/dL)",

        # Symptoms
        'symptoms_header': "Other Symptoms",
        'frequent_hunger': "Frequent hunger",
        'frequent_thirst': "Frequent thirst",
        'frequent_urination': "Frequent urination",

        # Health
        'conditions_label': "Current health conditions",
        'medications_label': "Current medications (if any)",
        'diabetes_label': "Diabetes History",
        'cancer_label': "Cancer History",
        'cvd_label': "CVD History",
        'diabetes_history': "Family history of diabetes",
        'cancer_history': "Family history of cancer",
        'cvd_history': "Family history of cardiovascular disease",

        # Well & Fit
        'symptom_fatigue': "Fatigue",
        'symptom_joint_pain': "Joint pain",
        'symptom_digestive': "Digestive discomfort",
        'symptom_skin_issues': "Skin issues",
        'symptom_headaches': "Headaches",
        'symptom_mood': "Mood fluctuations",
        'symptom_cognitive': "Cognitive difficulties",
        'symptom_sleep': "Sleep disturbances",

        # Genetic
        'had_testing': "Have you had genetic testing before?",
        'findings': "Please describe any significant findings",

        # Results
        'risk_level_low': "Risk Level: Low",
        'risk_level_moderate': "Risk Level: Moderate",
        'risk_level_high': "Risk Level: High",
        'risk_na': "Risk Level: N/A (Condition present)",
        'recommendations_label': "Recommendations:",
        'recommended_product': "Recommended Product:",
        'no_recommendation': "Follow your healthcare provider's treatment plan",

        #st_info
        'none_removed_info': "ℹ️ 'None' has been automatically removed since you selected other conditions.",

        #wellfit
        'wellfit_header': "Well & Fit Assessment",

        #submit
        'submit_button': "Calculate Risk Scores",

        #recommendation
        'category_metabolic': "Metabolic & Lifestyle Risk",
        'category_cvd': "CVD & Stroke Risk",
        'category_diabetes': "Diabetes Risk",
        'category_cancer': "Cancer Risk",
        'genetic_header': "Previous Genetic Testing",
        'had_testing': "Have you had genetic testing before?",
        'findings': "Please describe any significant findings"
    },

    'id': {
        # UI Header Titles
        'title': "🧬 Prediksi Risiko Penyakit",
        'subtitle': "Cari tahu bagaimana gaya hidup dan kondisi kesehatan Anda dapat digunakan untuk memprediksi risiko penyakit.",
        'form_title': "📝 Kuesioner Penilaian Risiko Kesehatan",
        'results_title': "📊 Hasil Penilaian Risiko Kesehatan Anda",
        'back_button': "🔙 Kembali ke Kuesioner",
        'success_msg': "✅ Skor risiko berhasil dihitung!",
        'personal_info': "Informasi Pribadi",
        'exercise_header': "Frekuensi Olahraga",
        'lifestyle_header': "Faktor Gaya Hidup",
        'health_header': "Kondisi Kesehatan",
        'family_history': "Riwayat Keluarga",
        'genetic_header': "Pemeriksaan Genetik Sebelumnya",
        'recommendation_header': "Rekomendasi Kesehatan Pribadi Anda",
        'take_action_header': "Ambil Tindakan",
        'result_header': "Penilaian Risiko Kesehatan Anda",
        'result_subtext': "Skor risiko dikategorikan sebagai: Rendah (< 40%), Sedang (40-60%), Tinggi (> 60%)",

        # Personal
        'age': "Usia",
        'height': "Tinggi Badan (cm)",
        'weight': "Berat Badan (kg)",
        'waist': "Lingkar Pinggang (cm)",
        'occupation': "Pekerjaan",
        'sex': "Jenis Kelamin",
        'sex_options': ["Laki-laki", "Perempuan"],
        'activity_level': "Tingkat Aktivitas Pekerjaan",
        'activity_options': ["Duduk terus-menerus", "Sedikit aktif", "Cukup aktif", "Sangat aktif"],

        # Exercise
        'exercise_freq': "Frekuensi olahraga (gabungan kardio & kekuatan)",
        'exercise_duration': "Durasi rata-rata olahraga",
        'exercise_intensity': "Intensitas olahraga",

        # Lifestyle
        'sleep_hours': "Rata-rata jam tidur per malam",
        'stress_level': "Tingkat stres",
        'cholesterol_level': "Kadar Kolesterol Total",
        'bp_meds': "Penggunaan obat penurun tekanan darah",
        'smoking_status': "Status merokok",
        'alcohol_use': "Konsumsi alkohol",
        'hba1c_label': "Kadar HbA1c (%)",
        'fasting_glucose': "Gula darah puasa (mg/dL)",

        # Symptoms
        'symptoms_header': "Gejala Lainnya",
        'frequent_hunger': "Frekuensi rasa lapar",
        'frequent_thirst': "Frekuensi rasa haus",
        'frequent_urination': "Frekuensi buang air kecil",

        # Health
        'conditions_label': "Kondisi kesehatan saat ini",
        'medications_label': "Obat yang sedang dikonsumsi (jika ada)",
        'diabetes_label': "Riwayat Diabetes",
        'cancer_label': "Riwayat Kanker",
        'cvd_label': "Riwayat Penyakit Jantung",
        'diabetes_history': "Riwayat keluarga diabetes",
        'cancer_history': "Riwayat keluarga kanker",
        'cvd_history': "Riwayat keluarga penyakit jantung",

        # Well & Fit
        'symptom_fatigue': "Kelelahan",
        'symptom_joint_pain': "Nyeri sendi",
        'symptom_digestive': "Gangguan pencernaan",
        'symptom_skin_issues': "Masalah kulit",
        'symptom_headaches': "Sakit kepala",
        'symptom_mood': "Fluktuasi mood",
        'symptom_cognitive': "Kesulitan kognitif",
        'symptom_sleep': "Gangguan tidur",

        # Genetic
        'had_testing': "Apakah Anda pernah melakukan tes genetik sebelumnya?",
        'findings': "Jelaskan hasil temuan yang signifikan",

        # Results
        'risk_level_low': "Tingkat Risiko: Rendah",
        'risk_level_moderate': "Tingkat Risiko: Sedang",
        'risk_level_high': "Tingkat Risiko: Tinggi",
        'risk_na': "Tingkat Risiko: N/A (Kondisi sudah ada)",
        'recommendations_label': "Rekomendasi:",
        'recommended_product': "Produk Rekomendasi:",
        'no_recommendation': "Ikuti rencana pengobatan dari penyedia layanan kesehatan Anda",

        #st_info
        'none_removed_info': "ℹ️ 'Tidak ada' dihapus secara otomatis karena Anda memilih kondisi lainnya.",

        #wellfit
        'wellfit_header': "Penilaian Kesehatan & Kebugaran",

        #submit
        'submit_button': "Hitung Skor Risiko",

        #recommendation
        'category_metabolic': "Risiko Metabolik & Gaya Hidup",
        'category_cvd': "Risiko Penyakit Jantung & Stroke",
        'category_diabetes': "Risiko Diabetes",
        'category_cancer': "Risiko Kanker",
        'genetic_header': "Pemeriksaan Genetik Sebelumnya",
        'had_testing': "Apakah Anda pernah melakukan tes genetik sebelumnya?",
        'findings': "Jelaskan hasil temuan yang signifikan"

    }
}

sleep_map = {
    "en": {
        "< 5 hours (insufficient)": "< 5 hours (insufficient)",
        "5-7 hours (below optimal)": "5-7 hours (below optimal)",
        "7-9 hours (optimal)": "7-9 hours (optimal)",
        "9+ hours (excessive)": "9+ hours (excessive)"
    },
    "id": {
        "< 5 hours (insufficient)": "< 5 jam (tidak cukup)",
        "5-7 hours (below optimal)": "5–7 jam (kurang optimal)",
        "7-9 hours (optimal)": "7–9 jam (optimal)",
        "9+ hours (excessive)": "> 9 jam (berlebihan)"
    }
}

stress_map = {
    "en": {
        "Low": "Low", "Moderate": "Moderate", "High": "High", "Very high": "Very high"
    },
    "id": {
        "Low": "Rendah", "Moderate": "Sedang", "High": "Tinggi", "Very high": "Sangat tinggi"
    }
}

cholesterol_map = {
    "en": {
        "Low (<200 mg/dL)": "Low (<200 mg/dL)",
        "Medium (200-239 mg/dL)": "Medium (200–239 mg/dL)",
        "High (≥240 mg/dL)": "High (≥240 mg/dL)",
        "Unknown": "Unknown"
    },
    "id": {
        "Low (<200 mg/dL)": "Rendah (<200 mg/dL)",
        "Medium (200-239 mg/dL)": "Sedang (200–239 mg/dL)",
        "High (≥240 mg/dL)": "Tinggi (≥240 mg/dL)",
        "Unknown": "Tidak diketahui"
    }
}

bp_map = {
    "en": {"No": "No", "Not routine": "Not routine", "Yes routinely": "Yes routinely"},
    "id": {"No": "Tidak", "Not routine": "Tidak rutin", "Yes routinely": "Ya (rutin)"}
}

smoking_map = {
    "en": {"Non-smoker": "Non-smoker", "Passive smoker": "Passive smoker", "Active smoker": "Active smoker"},
    "id": {"Non-smoker": "Tidak merokok", "Passive smoker": "Perokok pasif", "Active smoker": "Perokok aktif"}
}

alcohol_map = {
    "en": {"No": "No", "Yes": "Yes"},
    "id": {"No": "Tidak", "Yes": "Ya"}
}

symptom_scale = {
    "en": {
        "Never": "Never", "Rarely": "Rarely", "Sometimes": "Sometimes", "Often": "Often", "Always": "Always"
    },
    "id": {
        "Never": "Tidak pernah", "Rarely": "Jarang", "Sometimes": "Kadang-kadang", "Often": "Sering", "Always": "Selalu"
    }
}

health_conditions_map = {
    "en": {
        "Hypertension": "Hypertension",
        "High cholesterol": "High cholesterol",
        "Diabetes": "Diabetes",
        "Cardiovascular disease": "Cardiovascular disease",
        "Cancer": "Cancer",
        "Autoimmune condition": "Autoimmune condition",
        "Inflammatory condition": "Inflammatory condition",
        "Digestive disorders": "Digestive disorders",
        "Skin conditions": "Skin conditions",
        "None": "None"
    },
    "id": {
        "Hypertension": "Hipertensi",
        "High cholesterol": "Kolesterol tinggi",
        "Diabetes": "Diabetes",
        "Cardiovascular disease": "Penyakit kardiovaskular",
        "Cancer": "Kanker",
        "Autoimmune condition": "Kondisi autoimun",
        "Inflammatory condition": "Kondisi peradangan",
        "Digestive disorders": "Gangguan pencernaan",
        "Skin conditions": "Masalah kulit",
        "None": "Tidak ada"
    }
}

family_history_map = {
    "en": {
        "None": "None",
        "Grandparent affected": "Grandparent affected",
        "Parent affected": "Parent affected",
        "Sibling affected": "Sibling affected"
    },
    "id": {
        "None": "Tidak ada",
        "Grandparent affected": "Kakek/nenek terkena",
        "Parent affected": "Orang tua terkena",
        "Sibling affected": "Saudara kandung terkena"
    }
}

symptom_scale = {
    "en": {
        "Never": "Never",
        "Rarely": "Rarely",
        "Sometimes": "Sometimes",
        "Often": "Often",
        "Always": "Always"
    },
    "id": {
        "Never": "Tidak pernah",
        "Rarely": "Jarang",
        "Sometimes": "Kadang-kadang",
        "Often": "Sering",
        "Always": "Selalu"
    }
}

wellfit_scale = {
    "en": {
        "Never": "Never",
        "Rarely": "Rarely",
        "Sometimes": "Sometimes",
        "Often": "Often",
        "Always": "Always"
    },
    "id": {
        "Never": "Tidak pernah",
        "Rarely": "Jarang",
        "Sometimes": "Kadang-kadang",
        "Often": "Sering",
        "Always": "Selalu"
    }
}

RECOMMENDATIONS = {
    "metabolic": {
        "en": [
            "Follow Genme Life health recommendations for metabolic optimization",
            "Increase physical activity to 150 minutes of moderate exercise per week",
            "Implement stress management techniques like meditation or yoga",
            "Maintain consistent sleep schedule for 7-9 hours per night",
            "Focus on gradual, sustainable weight management",
            "Consider smoking cessation programs"
        ],
        "id": [
            "Ikuti rekomendasi kesehatan Genme Life untuk optimasi metabolik",
            "Tingkatkan aktivitas fisik hingga 150 menit olahraga sedang per minggu",
            "Lakukan manajemen stres seperti meditasi atau yoga",
            "Tidur teratur selama 7–9 jam per malam",
            "Fokus pada pengelolaan berat badan yang bertahap dan berkelanjutan",
            "Pertimbangkan program berhenti merokok"
        ]
    },
            "cvd": {
            "en": [
                "Follow Strokegenme guidance for cardiovascular health",
                "Schedule regular lipid panel blood checkups",
                "Monitor blood pressure regularly",
                "Increase aerobic exercise frequency",
                "Smoking cessation is critical for heart health",
                "Implement cardiovascular-protective stress management"
            ],
            "id": [
                "Ikuti panduan Strokegenme untuk kesehatan jantung",
                "Jadwalkan pemeriksaan darah panel lipid secara rutin",
                "Pantau tekanan darah secara teratur",
                "Tingkatkan frekuensi olahraga aerobik",
                "Berhenti merokok sangat penting untuk kesehatan jantung",
                "Kelola stres dengan pendekatan yang melindungi kesehatan jantung"
            ]
        },
        "diabetes": {
            "en": [
                "Schedule immediate medical checkup with HbA1c and fasting glucose tests",
                "Monitor blood glucose levels regularly",
                "Follow diabetes prevention dietary guidelines",
                "Increase physical activity to improve insulin sensitivity",
                "Weight management is crucial for diabetes prevention",
                "Discuss diabetes symptoms with healthcare provider immediately"
            ],
            "id": [
                "Segera jadwalkan pemeriksaan medis dengan tes HbA1c dan glukosa puasa",
                "Pantau kadar gula darah secara rutin",
                "Ikuti panduan diet pencegahan diabetes",
                "Tingkatkan aktivitas fisik untuk meningkatkan sensitivitas insulin",
                "Pengelolaan berat badan penting untuk pencegahan diabetes",
                "Diskusikan gejala diabetes dengan tenaga medis sesegera mungkin"
            ]
        },
        "cancer": {
            "en": [
                "Consider SpotMas screening for early cancer detection",
                "Schedule KalScreen 69 testing panels",
                "Maintain regular cancer screening as per age guidelines",
                "Adopt cancer-preventive lifestyle modifications",
                "Smoking cessation significantly reduces cancer risk",
                "Consider reducing alcohol consumption"
            ],
            "id": [
                "Pertimbangkan pemeriksaan SpotMas untuk deteksi dini kanker",
                "Jadwalkan panel tes KalScreen 69",
                "Lakukan skrining kanker secara rutin sesuai usia",
                "Terapkan gaya hidup pencegahan kanker",
                "Berhenti merokok dapat secara signifikan menurunkan risiko kanker",
                "Pertimbangkan untuk mengurangi konsumsi alkohol"
            ]
        }
}
   
genetic_test_map = {
    "en": {"No": "No", "Yes": "Yes"},
    "id": {"No": "Tidak", "Yes": "Ya"}
}

def map_selectbox(label, options_map, key=None):
    lang = st.session_state.lang
    display = list(options_map[lang].values())
    selected = st.selectbox(label, display, key=key)
    return [k for k, v in options_map[lang].items() if v == selected][0]


# --- LANGUAGE SELECTION ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

lang_choice = st.selectbox("🌐 Language / Bahasa", ["English", "Bahasa Indonesia"])
st.session_state.lang = 'en' if lang_choice == 'English' else 'id'
T = LANG[st.session_state.lang]

st.image("https://www.kalgeninnolab.co.id/frontend/web/images/kalgen-logo-home.png", width=120)
# Title
st.title(T['title'])
st.write(T['subtitle'])

# Create sections
def personal_info_section():
    st.header(T['personal_info'])
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input(T['age'], min_value=0, max_value=120, value=30)
        height = st.number_input(T['height'], min_value=0, max_value=300, value=170)
        occupation = st.text_input(T['occupation'])
        waist = st.number_input(T['waist'], min_value=0, max_value=200, value=80)

    with col2:
        sex = st.selectbox(T['sex'], T['sex_options'])
        weight = st.number_input(T['weight'], min_value=0, max_value=500, value=70)
        activity = st.selectbox(T['activity_level'], T['activity_options'])

    return {
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "occupation": occupation,
        "activity_level": activity,
        "waist_circumference": waist
    }


def physical_activity_section():
    st.header(T['exercise_header'])

    # Value-label mapping
    freq_map = {
        "Never": "Tidak pernah",
        "1-2 times per week": "1-2 kali/minggu",
        "3-4 times per week": "3-4 kali/minggu",
        "5+ times per week": "Lebih dari 5 kali/minggu"
    }

    duration_map = {
        "<15 minutes": "<15 menit",
        "15-30 minutes": "15–30 menit",
        "30-45 minutes": "30–45 menit",
        "45-60 minutes": "45–60 menit",
        "60+ minutes": ">60 menit"
    }

    intensity_map = {
        "Light": "Ringan",
        "Medium": "Sedang",
        "Vigorous": "Berat",
        "Very vigorous": "Sangat berat"
    }

    col1, col2 = st.columns(2)

    with col1:
        freq_display = list(freq_map.values())
        freq_selected_label = st.selectbox(T['exercise_freq'], freq_display)
        exercise_freq = [k for k, v in freq_map.items() if v == freq_selected_label][0]

    with col2:
        duration_display = list(duration_map.values())
        duration_selected_label = st.selectbox(T['exercise_duration'], duration_display)
        duration = [k for k, v in duration_map.items() if v == duration_selected_label][0]

        intensity_display = list(intensity_map.values())
        intensity_selected_label = st.selectbox(T['exercise_intensity'], intensity_display)
        intensity = [k for k, v in intensity_map.items() if v == intensity_selected_label][0]

    return {
        "exercise_frequency": exercise_freq,
        "duration": duration,
        "intensity": intensity
    }


def lifestyle_section():
    st.header(T['lifestyle_header'])

    col1, col2 = st.columns(2)

    with col1:
        sleep_hours = map_selectbox(T['sleep_hours'], sleep_map, key="sleep_hours")
        stress_level = map_selectbox(T['stress_level'], stress_map, key="stress_level")
        total_cholesterol = map_selectbox(T['cholesterol_level'], cholesterol_map)
        blood_pressure_medication = map_selectbox(T['bp_meds'], bp_map)

    with col2:
        smoking = map_selectbox(T['smoking_status'], smoking_map)
        alcohol = map_selectbox(T['alcohol_use'], alcohol_map)
        hba1c = st.number_input(T['hba1c_label'], min_value=0.0, max_value=20.0, value=5.5, step=0.1)
        fasting_glucose = st.number_input(T['fasting_glucose'], min_value=0, max_value=500, value=90)

    st.subheader(T['symptoms_header'])
    col3, col4 = st.columns(2)

    with col3:
        hunger = map_selectbox(T['frequent_hunger'], symptom_scale, key="frequent_hunger")
        thirst = map_selectbox(T['frequent_thirst'], symptom_scale, key="frequent_thirst")

    with col4:
        urination = map_selectbox(T['frequent_urination'], symptom_scale, key="frequent_urination")

    return {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "total_cholesterol": total_cholesterol,
        "blood_pressure_medication": blood_pressure_medication,
        "smoking": smoking,
        "alcohol": alcohol,
        "hba1c": hba1c,
        "fasting_glucose": fasting_glucose,
        "frequent_hunger": hunger,
        "frequent_thirst": thirst,
        "frequent_urination": urination
    }



def health_conditions_section():
    st.header(T['health_header'])
    
    lang = st.session_state.lang
    options_dict = health_conditions_map[lang]
    reverse_dict = {v: k for k, v in options_dict.items()}

    display_values = list(options_dict.values())
    selected_display = st.multiselect(T['conditions_label'], display_values, default=[options_dict["None"]])

    # Get internal English keys
    conditions = [reverse_dict[label] for label in selected_display]

    
    if len(conditions) > 1 and "None" in conditions:
        conditions = [c for c in conditions if c != "None"]
        st.info(T['none_removed_info'])
    
    medications = st.text_input(T['medications_label'])

    # Family History
    st.subheader(T['family_history'])
    
    col1, col2, col3 = st.columns(3)
    
    lang = st.session_state.lang
    fam_map = family_history_map[lang]
    fam_rev = {v: k for k, v in fam_map.items()}

    with col1:
        st.write(f"**{T['diabetes_label']}**")
        diabetes_label = st.selectbox(T['diabetes_history'], list(fam_map.values()), key="diabetes_history")
        diabetes_history = fam_rev[diabetes_label]

    with col2:
        st.write(f"**{T['cancer_label']}**")
        cancer_label = st.selectbox(T['cancer_history'], list(fam_map.values()), key="cancer_history")
        cancer_history = fam_rev[cancer_label]

    with col3:
        st.write(f"**{T['cvd_label']}**")
        cvd_label = st.selectbox(T['cvd_history'], list(fam_map.values()), key="cvd_history")
        cvd_history = fam_rev[cvd_label]

    
    st.subheader(T['wellfit_header']) # Optional: move to LANG dict if needed
    wf_display = list(wellfit_scale[lang].values())
    wf_reverse = {v: k for k, v in wellfit_scale[lang].items()}

    col1, col2 = st.columns(2)
    symptoms = {}
    
    with col1:
        symptoms["fatigue"] = wf_reverse[st.radio(T['symptom_fatigue'], wf_display, key="fatigue")]
        symptoms["joint_pain"] = wf_reverse[st.radio(T['symptom_joint_pain'], wf_display, key="joint_pain")]
        symptoms["digestive"] = wf_reverse[st.radio(T['symptom_digestive'], wf_display, key="digestive")]
        symptoms["skin_issues"] = wf_reverse[st.radio(T['symptom_skin_issues'], wf_display, key="skin_issues")]

    with col2:
        symptoms["headaches"] = wf_reverse[st.radio(T['symptom_headaches'], wf_display, key="headaches")]
        symptoms["mood"] = wf_reverse[st.radio(T['symptom_mood'], wf_display, key="mood")]
        symptoms["cognitive"] = wf_reverse[st.radio(T['symptom_cognitive'], wf_display, key="cognitive")]
        symptoms["sleep_issues"] = wf_reverse[st.radio(T['symptom_sleep'], wf_display, key="sleep_issues")]

    return {
        "conditions": conditions,
        "medications": medications,
        "diabetes_history": diabetes_history,
        "cancer_history": cancer_history,
        "cvd_history": cvd_history,
        "symptoms": symptoms
    }


def genetic_testing_section():
    st.header(T['genetic_header'])

    lang = st.session_state.lang
    test_map = genetic_test_map[lang]
    test_rev = {v: k for k, v in test_map.items()}

    had_label = st.selectbox(T['had_testing'], list(test_map.values()))
    had_testing = test_rev[had_label]

    findings = ""
    if had_testing == "Yes":
        findings = st.text_area(T['findings'], height=100)

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
    lang = st.session_state.lang
    recommendations = []
    
    if 'metabolic_lifestyle' in risk_scores and risk_scores['metabolic_lifestyle'] >= 0.4:
        recs = RECOMMENDATIONS["metabolic"][lang][:4]
        if features['bmi'] > 25:
            recs.append(RECOMMENDATIONS["metabolic"][lang][4])
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["metabolic"][lang][5])
        recommendations.append({
            'category': 'Metabolic & Lifestyle Risk',
            'recommendations': recs
        })

    # --- CVD ---
    if 'cvd_stroke' in risk_scores and risk_scores['cvd_stroke'] >= 0.3:
        recs = RECOMMENDATIONS["cvd"][lang][:4]
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cvd"][lang][4])
        if features['stress_score'] > 0.6:
            recs.append(RECOMMENDATIONS["cvd"][lang][5])
        recommendations.append({
            'category': 'CVD & Stroke Risk',
            'recommendations': recs
        })

    # --- DIABETES ---
    if 'diabetes' in risk_scores and risk_scores['diabetes'] >= 0.4:
        recs = RECOMMENDATIONS["diabetes"][lang][:4]
        if features['bmi'] > 25:
            recs.append(RECOMMENDATIONS["diabetes"][lang][4])
        if features['diabetes_symptoms'] > 0.5:
            recs.append(RECOMMENDATIONS["diabetes"][lang][5])
        recommendations.append({
            'category': 'Diabetes Risk',
            'recommendations': recs
        })

    # --- CANCER ---
    if 'cancer' in risk_scores and risk_scores['cancer'] >= 0.3:
        recs = RECOMMENDATIONS["cancer"][lang][:4]
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cancer"][lang][4])
        if features['alcohol_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cancer"][lang][5])
        recommendations.append({
            'category': 'Cancer Risk',
            'recommendations': recs
        })

    return recommendations

def display_results(risk_scores, recommendations):
    """Display risk scores and recommendations"""
    lang = st.session_state.lang

    st.header(T['result_header'])
    st.write(T['result_subtext'])

    # Translated category labels
    category_labels = {
        'metabolic_lifestyle': T['category_metabolic'],
        'cvd_stroke': T['category_cvd'],
        'diabetes': T['category_diabetes'],
        'cancer': T['category_cancer']
    }

    all_categories = [
        ('metabolic_lifestyle', 'metabolic_lifestyle'),
        ('cvd_stroke', 'cvd_stroke'),
        ('diabetes', 'diabetes'),
        ('cancer', 'cancer')
    ]

    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    def display_risk_metric(label_key, risk_key, col):
        with col:
            label = category_labels[label_key]
            if risk_key in risk_scores:
                value = risk_scores[risk_key]
                st.metric(label, f"{value*100:.1f}%")
                if value < 0.4:
                    st.success(T['risk_level_low'])
                elif value < 0.6:
                    st.warning(T['risk_level_moderate'])
                else:
                    st.error(T['risk_level_high'])
            else:
                st.metric(label, "N/A")
                st.info(T['risk_na'])

    for i, (label_key, risk_key) in enumerate(all_categories):
        display_risk_metric(label_key, risk_key, cols[i])

    # --- Recommendations Section ---
    st.header(T['recommendation_header'])

    for label_key, risk_key in all_categories:
        category_name = category_labels[label_key]
        st.subheader(f"🎯 {category_name}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"**{T['recommendations_label']}**")
            category_recommendations = None
            for rec_cat in recommendations:
                if rec_cat['category'] == category_name:
                    category_recommendations = rec_cat['recommendations']
                    break

            if category_recommendations:
                for i, rec in enumerate(category_recommendations, 1):
                    st.write(f"{i}. {rec}")
            elif risk_key in risk_scores:
                st.write("1. " + T['no_recommendation'])
                st.write("2. Regular monitoring and healthy habits")
                st.write("3. Follow-up with healthcare provider")
            else:
                st.write("1. " + T['no_recommendation'])
                st.write("2. Regular monitoring and check-ups")
                st.write("3. Maintain prescribed medications")

        with col2:
            st.write(f"**{T['recommended_product']}**")

            image_path = 'assets/MCU.jpg'
            caption = "General Health Screening"

            if risk_key == 'diabetes':
                image_path = 'assets/MCU.jpg'
                caption = "MCU – Pemeriksaan Kesehatan Metabolik" if lang == "id" else "MCU Health Screening"
            elif risk_key == 'cvd_stroke' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/StrokeGENME.png'
                caption = "StrokeGENME – Pencegahan Penyakit Jantung" if lang == "id" else "StrokeGENME – CVD Prevention"
            elif risk_key == 'cancer' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/Kalscanner69.png'
                caption = "Kalscanner69 – Deteksi Kanker" if lang == "id" else "Kalscanner69 – Cancer Screening"
            elif risk_key == 'metabolic_lifestyle' and risk_key in risk_scores and risk_scores[risk_key] >= 0.4:
                image_path = 'assets/GENME_LIFE.png'
                caption = "GENME Life – Kesehatan Metabolik" if lang == "id" else "GENME Life – Metabolic Health"

            try:
                st.image(image_path, caption=caption, use_container_width=True)
            except:
                st.error(f"Image not found: {image_path}")

        st.divider()

    # --- CTA Section ---
    st.header(T['take_action_header'])
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📞 Informasi Produk", use_container_width=True):
            st.markdown("[Hubungi Customer Relations](https://wa.me/your_whatsapp_number)")

    with col2:
        if st.button("🧪 Lakukan Tes", use_container_width=True):
            st.markdown("[Booking Tes Anda](https://wa.me/your_whatsapp_number)")

    with col3:
        if st.button("🎁 Lihat Promo", use_container_width=True):
            st.markdown("[Cek Promo Saat Ini](https://wa.me/your_whatsapp_number)")


# Main app flow
def main():
    # Initialize session state
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Check if results should be shown and auto-select Results tab
    if st.session_state.show_results:
        # Show results directly without tabs when calculation is complete
        st.header(T['results_title'])
        
        # Add a button to go back to questionnaire
        if st.button(T['back_button']):
            st.session_state.show_results = False
            st.rerun()
        
        # Process and display results
        features = process_questionnaire_data(st.session_state.questionnaire_data)
        risk_scores = calculate_risk_scores(features)
        recommendations = generate_recommendations(risk_scores, features)
        display_results(risk_scores, recommendations)
        
    else:
        # Show questionnaire form
        st.header(T['form_title'])
        
        with st.form("health_questionnaire"):
            # Collect data from each section
            personal_data = personal_info_section()
            activity_data = physical_activity_section()
            lifestyle_data = lifestyle_section()
            health_data = health_conditions_section()
            genetic_data = genetic_testing_section()
            
            # Submit button
            submitted = submitted = st.form_submit_button(T['submit_button'], icon=":material/check_circle:")
            
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
                st.success(T['success_msg'])
                st.balloons()
                st.rerun()

if __name__ == "__main__":
    main()