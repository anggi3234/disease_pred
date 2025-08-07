import streamlit as st
# from pydantic import BaseModel - This import is not used
from typing import List, Optional
import pandas as pd
import numpy as np
import math
import csv
import json
import os
from datetime import datetime
# Removed unused pydrive2 and io imports
from oauth2client.service_account import ServiceAccountCredentials
import gspread


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
        'take_action_header': "Contact Us",
        'result_header': "Your Health Risk Assessment",
        'result_subtext': "Risk scores are categorized as: Low (< 30%), Moderate (30-50%), High (> 50%)",

        # Personal
        'name': "Name",
        'phone': "Phone Number",
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
        'hba1c_label': "HbA1c level",
        'fasting_glucose': "Fasting glucose level",

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
        'wellfit_header': "Well & Fit Assessment",
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

        #submit
        'submit_button': "Calculate Risk Scores",
        
        #recommendation
        'category_metabolic': "Metabolic & Lifestyle Risk",
        'category_cvd': "CVD & Stroke Risk",
        'category_diabetes': "Diabetes Risk",
        'category_cancer': "Cancer Risk",

        # Contact buttons
        'promo_button': "🎁 Promo",
        'inquiry_button': "📞 Inquiry",
        'contact_whatsapp': "[WhatsApp Customer Relations](https://wa.me/your_whatsapp_number)",
        'check_promo': "✨ More Information ✨",

        # Success message for low risk
        'low_risk_success': "🎉 Great news! All your risk levels are in the low range. Keep maintaining your healthy lifestyle!",
        'general_maintenance': "General Health Maintenance:",
        'maintain_habits': "Continue your current healthy habits",
        'regular_checkups': "Regular preventive health check-ups",
        'stay_active': "Stay active and maintain balanced nutrition",
        'monitor_changes': "Monitor any changes in your health status",

        # Mandatory changes and fields
        'monitor_changes': "Monitor any changes in your health status",
        'mandatory_fields_error': "Please fill in the following mandatory fields: {fields}"
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
        'take_action_header': "Hubungi Kami",
        'result_header': "Penilaian Risiko Kesehatan Anda",
        'result_subtext': "Skor risiko dikategorikan sebagai: Rendah (< 30%), Sedang (30-50%), Tinggi (> 50%)",

        # Personal
        'name': "Nama",
        'phone': "Nomor Telepon",
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
        'hba1c_label': "Kadar HbA1c",
        'fasting_glucose': "Kadar glukosa puasa",

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
        'wellfit_header': "Penilaian Kesehatan & Kebugaran",
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

        #submit
        'submit_button': "Hitung Skor Risiko",

        #recommendation
        'category_metabolic': "Risiko Metabolik & Gaya Hidup",
        'category_cvd': "Risiko Penyakit Jantung & Stroke",
        'category_diabetes': "Risiko Diabetes",
        'category_cancer': "Risiko Kanker",

        # Contact buttons
        'promo_button': "🎁 Promo",
        'inquiry_button': "📞 Tanya",
        'contact_whatsapp': "[WhatsApp Customer Relations](https://wa.me/your_whatsapp_number)",
        'check_promo': "✨ Informasi Lebih Lanjut ✨",

        # Success message for low risk
        'low_risk_success': "🎉 Kabar baik! Semua tingkat risiko Anda dalam kategori rendah. Terus pertahankan gaya hidup sehat Anda!",
        'general_maintenance': "Pemeliharaan Kesehatan Umum:",
        'maintain_habits': "Lanjutkan kebiasaan sehat Anda saat ini",
        'regular_checkups': "Pemeriksaan kesehatan preventif secara rutin",
        'stay_active': "Tetap aktif dan jaga nutrisi seimbang",
        'monitor_changes': "Pantau perubahan pada status kesehatan Anda",

        # Mandatory changes and mandatory fields
        'monitor_changes': "Pantau perubahan pada status kesehatan Anda",
        'mandatory_fields_error': "Harap isi bidang wajib berikut: {fields}"
    }
}

# Translation mappings
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

sleep_map_help = {
    "en": "Total sleep duration including naps",
    "id": "Total durasi tidur termasuk tidur siang"
}

stress_map = {
    "en": {
        "Low": "Low", "Moderate": "Moderate", "High": "High", "Very high": "Very high"
    },
    "id": {
        "Low": "Rendah", "Moderate": "Sedang", "High": "Tinggi", "Very high": "Sangat tinggi"
    }
}

stress_map_help = {
    "en": "Low: Rarely stressed; Moderate: Sometimes stressed; High: Frequently stressed; Very high: Constantly overwhelmed",
    "id": "Rendah: Jarang stres; Sedang: Kadang-kadang stres; Tinggi: Sering stres; Sangat tinggi: Terus-menerus merasa kewalahan"
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

cholesterol_map_help = {
    "en": "Total cholesterol level from blood test",
    "id": "Total kadar kolesterol dari tes darah"
}

bp_map = {
    "en": {"No": "No", "Not routine": "Not routine", "Yes routinely": "Yes routinely"},
    "id": {"No": "Tidak", "Not routine": "Tidak rutin", "Yes routinely": "Ya (rutin)"}
}

bp_map_help = {
    "en": "Regular use of antihypertensive medications",
    "id": "Penggunaan rutin obat anti hipertensi"
}

smoking_map = {
    "en": {"Non-smoker": "Non-smoker", "Passive smoker": "Passive smoker", "Active smoker": "Active smoker"},
    "id": {"Non-smoker": "Tidak merokok", "Passive smoker": "Perokok pasif", "Active smoker": "Perokok aktif"}
}

smoking_map_help = {
    "en": "Non-smoker: Never smoked; Passive: Exposed to secondhand smoke; Active: Current smoker",
    "id": "Tidak merokok: Tidak pernah merokok; Perokok pasif: Terpapar asap rokok orang lain; Perokok aktif: Saat ini merokok"
}

alcohol_map = {
    "en": {"No": "No", "Yes": "Yes"},
    "id": {"No": "Tidak", "Yes": "Ya"}
}

alcohol_map_help = {
    "en": "Regular alcohol consumption (weekly or more frequent)",
    "id": "Konsumsi alkohol secara teratur (mingguan atau lebih sering)"
}

hba1c_map = {
    "en": {
        "<5.7% (normal)": "<5.7% (normal)",
        "5.7-6.4% (prediabetes)": "5.7-6.4% (prediabetes)",
        ">6.5% (diabetes)": ">6.5% (diabetes)",
        "Unknown": "Unknown"
    },
    "id": {
        "<5.7% (normal)": "<5.7% (normal)",
        "5.7-6.4% (prediabetes)": "5.7-6.4% (prediabetes)",
        ">6.5% (diabetes)": ">6.5% (diabetes)",
        "Unknown": "Tidak diketahui"
    }
}

hba1c_map_help = {
    "en": "HbA1c level from blood test",
    "id": "HbA1c dari tes darah"
}

glucose_map = {
    "en": {
        "Normal: <100 mg/dL (5.6 mmol/L)": "Normal: <100 mg/dL (5.6 mmol/L)",
        "Prediabetes: 100-125 mg/dL (5.6-6.9 mmol/L)": "Prediabetes: 100-125 mg/dL (5.6-6.9 mmol/L)",
        "Diabetes: ≥126 mg/dL (7.0 mmol/L)": "Diabetes: ≥126 mg/dL (7.0 mmol/L)",
        "Unknown": "Unknown"
    },
    "id": {
        "Normal: <100 mg/dL (5.6 mmol/L)": "Normal: <100 mg/dL (5.6 mmol/L)",
        "Prediabetes: 100-125 mg/dL (5.6-6.9 mmol/L)": "Prediabetes: 100-125 mg/dL (5.6-6.9 mmol/L)",
        "Diabetes: ≥126 mg/dL (7.0 mmol/L)": "Diabetes: ≥126 mg/dL (7.0 mmol/L)",
        "Unknown": "Tidak diketahui"
    }
}

glucose_map_help = {
    "en": "Fasting glucose level from blood test",
    "id": "Kadar glukosa puasa dari tes darah"
}

symptom_scale = {
    "en": {
        "Never": "Never", 
        "Sometimes": "Sometimes", 
        "Often": "Often", 
        "Always": "Always"
    },
    "id": {
        "Never": "Tidak pernah", 
        "Sometimes": "Kadang-kadang", 
        "Often": "Sering", 
        "Always": "Selalu"
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
        "Grandparent": "Grandparent",
        "Parent": "Parent",
        "Sibling": "Sibling"
    },
    "id": {
        "None": "Tidak ada",
        "Grandparent": "Kakek/nenek",
        "Parent": "Orang tua",
        "Sibling": "Saudara kandung"
    }
}

genetic_test_map = {
    "en": {"No": "No", "Yes": "Yes"},
    "id": {"No": "Tidak", "Yes": "Ya"}
}

exercise_freq_map = {
    "en": {
        "Never": "Never",
        "1-2 times per week": "1-2 times per week",
        "3-4 times per week": "3-4 times per week",
        "5+ times per week": "5+ times per week"
    },
    "id": {
        "Never": "Tidak pernah",
        "1-2 times per week": "1-2 kali/minggu",
        "3-4 times per week": "3-4 kali/minggu",
        "5+ times per week": "Lebih dari 5 kali/minggu"
    }
}

exercise_freq_help = {
    "en": "Include all types of structured exercise and sports activities, excluding daily activities like walking or household chores",
    "id": "Termasuk semua jenis olahraga terstruktur dan aktivitas olahraga, tidak termasuk aktivitas sehari-hari seperti berjalan kaki atau pekerjaan rumah tangga"
}

duration_map = {
    "en": {
        "<15 minutes": "<15 minutes",
        "15-30 minutes": "15-30 minutes",
        "30-45 minutes": "30-45 minutes",
        "45-60 minutes": "45-60 minutes",
        "60+ minutes": "60+ minutes"
    },
    "id": {
        "<15 minutes": "<15 menit",
        "15-30 minutes": "15–30 menit",
        "30-45 minutes": "30–45 menit",
        "45-60 minutes": "45–60 menit",
        "60+ minutes": ">60 menit"
    }
}

duration_map_help = {
    "en": "Duration per exercise session",
    "id": "Durasi per sesi latihan"
}

intensity_map = {
    "en": {
        "Light": "Light",
        "Medium": "Medium",
        "Vigorous": "Vigorous",
        "Very vigorous": "Very vigorous"
    },
    "id": {
        "Light": "Ringan",
        "Medium": "Sedang",
        "Vigorous": "Berat",
        "Very vigorous": "Sangat berat"
    }
}
intensity_map_help = {
    "en": "Light: Can talk and manage breathing easily; Medium: Can talk but breathing is elevated; Vigorous: Difficult to talk; Very vigorous: Cannot maintain conversation",
    "id": "Ringan: Dapat berbicara dan mengatur pernapasan dengan mudah; Sedang: Dapat berbicara tetapi pernapasan meningkat; Berat: Sulit berbicara; Sangat berat: Tidak dapat mempertahankan percakapan"
}

WHATSAPP_LINKS = {
    "metabolic": "https://api.whatsapp.com/send?phone=6281510068080&text=Halo%20CR%20KALGen%20Innolab!%2C%20Setelah%20saya%20menggunakan%20DNA%20CARE%20Calculator%2C%20saya%20memiliki%20risiko%20tinggi%20atau%20menengah%20untuk%20penyakit%20metabolik%20dan%20gaya%20hidup.%20Apakah%20bisa%20diinfokan%20lebih%20lanjut%20mengenai%20tes%20Genme%20Life%3F",
    "diabetes": "https://api.whatsapp.com/send?phone=6281510068080&text=Halo%20CR%20KALGen%20Innolab!%2C%20Setelah%20saya%20menggunakan%20DNA%20CARE%20Calculator%2C%20saya%20memiliki%20risiko%20tinggi%20atau%20menengah%20untuk%20penyakit%20diabetes.%20Apakah%20bisa%20diinfokan%20lebih%20lanjut%20mengenai%20tes%20Medical%20Check%20Up%3F",
    "cvd": "https://api.whatsapp.com/send?phone=6281510068080&text=Halo%20CR%20KALGen%20Innolab!%2C%20Setelah%20saya%20menggunakan%20DNA%20CARE%20Calculator%2C%20saya%20memiliki%20risiko%20tinggi%20atau%20menengah%20untuk%20penyakit%20kardiovaskular.%20Apakah%20bisa%20diinfokan%20lebih%20lanjut%20mengenai%20tes%20StrokeGENME%3F",
    "cancer": "https://api.whatsapp.com/send?phone=6281510068080&text=Halo%20CR%20KALGen%20Innolab!%2C%20Setelah%20saya%20menggunakan%20DNA%20CARE%20Calculator%2C%20saya%20memiliki%20risiko%20menengah%20untuk%20penyakit%20kanker.%20Apakah%20bisa%20diinfokan%20lebih%20lanjut%20mengenai%20tes%20KalScreen%3F",
    "cancer_high_risk": "https://api.whatsapp.com/send?phone=6281510068080&text=Halo%20CR%20KALGen%20Innolab!%2C%20Setelah%20saya%20menggunakan%20DNA%20CARE%20Calculator%2C%20saya%20memiliki%20risiko%20tinggi%20%20untuk%20penyakit%20kanker.%20Apakah%20bisa%20diinfokan%20lebih%20lanjut%20mengenai%20tes%20SpotMas%3F"
}



RECOMMENDATIONS = {
    "metabolic": {
        "en": [
            "Follow Genme Life health recommendations for metabolic optimization",
            "Increase physical activity to 150 minutes of moderate exercise per week",
            "Implement stress management techniques like meditation or yoga",
            "Maintain consistent sleep schedule for 7-9 hours per night",
            "Medical Check-Up Recommended",
            "Focus on gradual, sustainable weight management",
            "Consider smoking cessation programs"
        ],
        "id": [
            "Ikuti rekomendasi kesehatan Genme Life untuk optimasi metabolik",
            "Tingkatkan aktivitas fisik hingga 150 menit olahraga sedang per minggu",
            "Lakukan manajemen stres seperti meditasi atau yoga",
            "Tidur teratur selama 7–9 jam per malam",
            "Pemeriksaan Medis Direkomendasikan",
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
            "Medical Check-Up Recommended",
            "Smoking cessation is critical for heart health",
            "Implement cardiovascular-protective stress management"
        ],
        "id": [
            "Ikuti panduan Strokegenme untuk kesehatan jantung",
            "Jadwalkan pemeriksaan darah panel lipid secara rutin",
            "Pantau tekanan darah secara teratur",
            "Tingkatkan frekuensi olahraga aerobik",
            "Pemeriksaan Medis Direkomendasikan",
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
            "Medical Check-Up Recommended",
            "Weight management is crucial for diabetes prevention",
            "Discuss diabetes symptoms with healthcare provider immediately"
        ],
        "id": [
            "Segera jadwalkan pemeriksaan medis dengan tes HbA1c dan glukosa puasa",
            "Pantau kadar gula darah secara rutin",
            "Ikuti panduan diet pencegahan diabetes",
            "Tingkatkan aktivitas fisik untuk meningkatkan sensitivitas insulin",
            "Pemeriksaan Medis Direkomendasikan",
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
            "Medical Check-Up Recommended",
            "Smoking cessation significantly reduces cancer risk",
            "Consider reducing alcohol consumption"
        ],
        "id": [
            "Pertimbangkan pemeriksaan SpotMas untuk deteksi dini kanker",
            "Jadwalkan panel tes KalScreen 69",
            "Lakukan skrining kanker secara rutin sesuai usia",
            "Terapkan gaya hidup pencegahan kanker",
            "Pemeriksaan Medis Direkomendasikan",
            "Berhenti merokok dapat secara signifikan menurunkan risiko kanker",
            "Pertimbangkan untuk mengurangi konsumsi alkohol"
        ]
    }
}

def map_selectbox(label, options_map, key=None, help=None):
    lang = st.session_state.lang
    display = list(options_map[lang].values())
    selected = st.selectbox(label, display, key=key, help=help)
    return [k for k, v in options_map[lang].items() if v == selected][0]

def map_radio(label, options_map, key=None, help=None):
    lang = st.session_state.lang
    display = list(options_map[lang].values())
    selected = st.radio(label, display, key=key, help=help)
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
        name = st.text_input(T['name'])
        sex = st.selectbox(T['sex'], T['sex_options'])
        age = st.number_input(T['age'], min_value=0, max_value=120)
        phone = st.text_input(T['phone'])
        waist_circumference = st.number_input(T['waist'], min_value=0, max_value=200)
    
    with col2:
        height = st.number_input(T['height'], min_value=0, max_value=300)
        weight = st.number_input(T['weight'], min_value=0, max_value=500)
        occupation = st.text_input(T['occupation'])
        activity_level = st.selectbox(T['activity_level'], T['activity_options'])
    
    return {
        "name": name,
        "phone": phone,
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "occupation": occupation,
        "activity_level": activity_level,
        "waist_circumference": waist_circumference
    }

def physical_activity_section():
    st.header(T['exercise_header'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        exercise_freq = map_selectbox(T['exercise_freq'], exercise_freq_map, help=exercise_freq_help[st.session_state.lang], key="exercise_freq")
    with col2:
        duration = map_selectbox(T['exercise_duration'], duration_map, help=duration_map_help[st.session_state.lang], key="exercise_duration")
        intensity = map_selectbox(T['exercise_intensity'], intensity_map, help=intensity_map_help[st.session_state.lang], key="exercise_intensity")
    return {
        "exercise_frequency": exercise_freq,
        "duration": duration,
        "intensity": intensity
    }

def lifestyle_section():
    st.header(T['lifestyle_header'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = map_selectbox(T['sleep_hours'], sleep_map, help=sleep_map_help[st.session_state.lang], key="sleep_hours")
        stress_level = map_selectbox(T['stress_level'], stress_map, help=stress_map_help[st.session_state.lang], key="stress_level")
        total_cholesterol = map_selectbox(T['cholesterol_level'], cholesterol_map, help=cholesterol_map_help[st.session_state.lang], key="cholesterol_level")
        blood_pressure_medication = map_selectbox(T['bp_meds'], bp_map, help=bp_map_help[st.session_state.lang], key="bp_meds")

    with col2:
        smoking = map_selectbox(T['smoking_status'], smoking_map, help=smoking_map_help[st.session_state.lang], key="smoking_status")
        alcohol = map_selectbox(T['alcohol_use'], alcohol_map, help=alcohol_map_help[st.session_state.lang], key="alcohol_use")
        hba1c = map_selectbox(T['hba1c_label'], hba1c_map, help=hba1c_map_help[st.session_state.lang], key="hba1c_label")
        fasting_glucose = map_selectbox(T['fasting_glucose'], glucose_map, help=glucose_map_help[st.session_state.lang], key="fasting_glucose")

    # Other symptoms
    st.subheader(T['symptoms_header'])
    col3, col4 = st.columns(2)
    
    with col3:
        hunger = map_radio(T['frequent_hunger'], symptom_scale, key="frequent_hunger")
        thirst = map_radio(T['frequent_thirst'], symptom_scale, key="frequent_thirst")
    
    with col4:
        urination = map_radio(T['frequent_urination'], symptom_scale, key="frequent_urination")
    
    return {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "smoking": smoking,
        "alcohol": alcohol,
        "total_cholesterol": total_cholesterol,
        "blood_pressure_medication": blood_pressure_medication,
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
    
    with col1:
        st.write(f"**{T['diabetes_label']}**")
        diabetes_history = map_selectbox(T['diabetes_history'], family_history_map, key="diabetes_history")

    with col2:
        st.write(f"**{T['cancer_label']}**")
        cancer_history = map_selectbox(T['cancer_history'], family_history_map, key="cancer_history")

    with col3:
        st.write(f"**{T['cvd_label']}**")
        cvd_history = map_selectbox(T['cvd_history'], family_history_map, key="cvd_history")
    
    st.subheader(T['wellfit_header'])
    col1, col2 = st.columns(2)
    
    symptoms = {}
    with col1:
        symptoms["fatigue"] = map_radio(T['symptom_fatigue'], symptom_scale, key="fatigue")
        symptoms["joint_pain"] = map_radio(T['symptom_joint_pain'], symptom_scale, key="joint_pain")
        symptoms["digestive"] = map_radio(T['symptom_digestive'], symptom_scale, key="digestive")
        symptoms["skin_issues"] = map_radio(T['symptom_skin_issues'], symptom_scale, key="skin_issues")

    with col2:
        symptoms["headaches"] = map_radio(T['symptom_headaches'], symptom_scale, key="headaches")
        symptoms["mood"] = map_radio(T['symptom_mood'], symptom_scale, key="mood")
        symptoms["cognitive"] = map_radio(T['symptom_cognitive'], symptom_scale, key="cognitive")
        symptoms["sleep_issues"] = map_radio(T['symptom_sleep'], symptom_scale, key="sleep_issues")
    
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
    
    had_testing = map_selectbox(T['had_testing'], genetic_test_map, key="had_testing")
    
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
    features['gender_male'] = 1 if data['personal']['sex'] in ['Male', 'Laki-laki'] else 0
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
    features['hba1c'] = map_hba1c_level(data['lifestyle']['hba1c'])
    features['fasting_glucose'] = map_fasting_glucose_level(data['lifestyle']['fasting_glucose'])
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
    stress_map_calc = {
        'Low': 0.2,
        'Moderate': 0.4,
        'High': 0.7,
        'Very high': 1.0
    }
    return stress_map_calc[lifestyle_data['stress_level']]

def calculate_smoking_risk(lifestyle_data):
    """Calculate smoking risk score (0-1)"""
    smoking_map_calc = {
        'Non-smoker': 0.0,
        'Passive smoker': 0.3,
        'Active smoker': 1.0
    }
    return smoking_map_calc[lifestyle_data['smoking']]

def map_cholesterol_level(cholesterol_str):
    """Map cholesterol level to numerical value"""
    cholesterol_map_calc = {
        'Low (<200 mg/dL)': 180,
        'Medium (200-239 mg/dL)': 220,
        'High (≥240 mg/dL)': 260,
        'Unknown': 200  # Use average value
    }
    return cholesterol_map_calc[cholesterol_str]

def map_bp_medication(bp_med_str):
    """Map BP medication to numerical value"""
    bp_map_calc = {
        'No': 0,
        'Not routine': 0.5,
        'Yes routinely': 1
    }
    return bp_map_calc[bp_med_str]

def map_hba1c_level(hba1c_str):
    """Map HbA1c dropdown to numerical value"""
    hba1c_map_calc = {
        '<5.7% (normal)': 5.4,  # Average normal value
        '5.7-6.4% (prediabetes)': 6.0,  # Midpoint
        '>6.5% (diabetes)': 7.5,  # Typical diabetic value
        'Unknown': 5.7  # Use threshold value
    }
    return hba1c_map_calc[hba1c_str]

def map_fasting_glucose_level(glucose_str):
    """Map fasting glucose dropdown to numerical value"""
    glucose_map_calc = {
        'Normal: <100 mg/dL (5.6 mmol/L)': 90,  # Average normal
        'Prediabetes: 100-125 mg/dL (5.6-6.9 mmol/L)': 112,  # Midpoint
        'Diabetes: ≥126 mg/dL (7.0 mmol/L)': 140,  # Typical diabetic
        'Unknown': 100  # Use threshold value
    }
    return glucose_map_calc[glucose_str]

def calculate_diabetes_symptoms(lifestyle_data):
    """Calculate diabetes symptoms score"""
    symptom_map_calc = {
        'Never': 0,
        'Sometimes': 0.5,
        'Often': 0.75,
        'Always': 1.0
    }
    
    hunger_score = symptom_map_calc[lifestyle_data['frequent_hunger']]
    thirst_score = symptom_map_calc[lifestyle_data['frequent_thirst']]
    urination_score = symptom_map_calc[lifestyle_data['frequent_urination']]
    
    return (hunger_score + thirst_score + urination_score) / 3

def map_family_history(history_str):
    """Map family history to weighted score"""
    history_map_calc = {
        'None': 0,
        'Grandparent': 1,
        'Parent': 2,
        'Sibling': 3
    }
    return history_map_calc[history_str]

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
    severity_map_calc = {
        'Never': 0,
        'Sometimes': 0.5,
        'Often': 0.75,
        'Always': 1.0
    }
    
    symptoms = health_data['symptoms']
    total_severity = sum(severity_map_calc[v] for v in symptoms.values())
    return total_severity / len(symptoms)

def calculate_framingham_risk_score(features):
    """Simplified Framingham 10-year CVD risk based on specified factors (without SBP)"""
    age = features['age']
    is_male = features['gender_male']
    total_chol = features['total_cholesterol']
    treated_bp = features['bp_medication'] > 0  # Treated if on meds (routine or not)
    smoking = features['smoking_risk'] > 0.5  # Active smoker
    diabetes = (features['hba1c'] >= 6.5 or features['fasting_glucose'] >= 126 or features['has_diabetes'])

    # Points system adapted from Framingham (simplified; no SBP/HDL; use BP meds as proxy)
    points = 0

    # Age points (male/female specific) - Slightly increased to compensate for no SBP
    if is_male:
        if age < 35: points += -8
        elif age <= 39: points += -3
        elif age <= 44: points += 1
        elif age <= 49: points += 4
        elif age <= 54: points += 7
        elif age <= 59: points += 9
        elif age <= 64: points += 11
        elif age <= 69: points += 12
        elif age <= 74: points += 13
        else: points += 14
    else:
        if age < 35: points += -6
        elif age <= 39: points += -2
        elif age <= 44: points += 1
        elif age <= 49: points += 4
        elif age <= 54: points += 7
        elif age <= 59: points += 9
        elif age <= 64: points += 11
        elif age <= 69: points += 13
        elif age <= 74: points += 15
        else: points += 17

    # Total Cholesterol points (age-adjusted, simplified) - Slightly increased
    if total_chol < 160: chol_points = 0
    elif total_chol < 200: chol_points = 2
    elif total_chol < 240: chol_points = 3
    elif total_chol < 280: chol_points = 4
    else: chol_points = 5
    if age >= 70: chol_points -= 1  # Adjust for older age
    points += chol_points

    # BP meds as proxy for hypertension (increased weight without direct SBP)
    if treated_bp:
        points += 4  # Higher penalty assuming treatment indicates elevated BP

    # Smoking: +3 if smoker (increased from 2 to compensate)
    if smoking: points += 3

    # Diabetes: +3 if present (increased from 2)
    if diabetes: points += 3

    # Convert points to approximate 10-year risk % (using exponential approximation for realism)
    import math
    risk = 1 - math.exp(-0.06 * (points + 8))  # Adjusted to give ~3-7% base for young/healthy, caps at ~80%
    return max(0.01, min(risk, 0.99))  # Ensure no 0% or 100%

def calculate_risk_scores(features):
    """Calculate risk scores for different health aspects with adjusted cutoffs"""
    risk_scores = {}
    
    # Metabolic and Lifestyle Risk - Adjusted to reduce default to ~46%
    metabolic_risk = (
        0.22 * max(0, (features['bmi'] - 18.5) / (32 - 18.5)) +  # Slightly lowered weight
        0.18 * (1 - min(features['met_hours'] / 35, 1)) +  # Slightly lowered
        0.18 * features['stress_score'] +  # Slightly lowered
        0.15 * features['smoking_risk'] +
        0.1 * features['alcohol_risk'] +
        0.1 * (1 - features['sleep_score'])
    )
    # Reduced multiplier
    metabolic_risk = min(metabolic_risk * 1.15, 1.0)
    risk_scores['metabolic_lifestyle'] = max(0.01, min(0.99, metabolic_risk))  # Avoid extremes
    
    # CVD & Stroke Risk (Revamped Framingham-based without SBP)
    if not features['has_cvd']:
        cvd_risk = calculate_framingham_risk_score(features)
        # Add family history
        cvd_risk += features['cvd_family_history'] * 0.08
        # Apply multiplier
        cvd_risk = min(cvd_risk * 1.2, 1.0)
        risk_scores['cvd_stroke'] = max(0.01, min(0.99, cvd_risk))
    
    # Diabetes Risk - Unchanged from previous adjustment
    if not features['has_diabetes']:
        # Adjust waist circumference if zero
        waist_adj = features['waist_circumference'] if features['waist_circumference'] > 0 else 80
        
        diabetes_risk = (
            0.25 * max(0, (features['bmi'] - 18.5) / (32 - 18.5)) +  # Lower BMI threshold
            0.2 * max(0, (waist_adj - 65) / (110 - 65)) +  # Lower waist threshold
            0.15 * min(max( (features['hba1c'] - 4.5) / (6.5 - 4.5), 0), 1) +  # Adjusted continuous scaling for HbA1c
            0.15 * min(max( (features['fasting_glucose'] - 70) / (126 - 70), 0), 1) +  # Adjusted continuous scaling for glucose
            0.1 * (1 - min(features['met_hours'] / 35, 1)) +
            0.05 * features['diabetes_family_history'] * 0.1 +
            0.1 * features['diabetes_symptoms']
        )
        # Apply multiplier to increase scores
        diabetes_risk = min(diabetes_risk * 1.25, 1.0)
        risk_scores['diabetes'] = max(0.01, min(0.99, diabetes_risk))
    
    # Cancer Risk - Minor adjustment to avoid 0%
    if not features['has_cancer']:
        cancer_risk = (
            0.3 * (features['age'] - 18) / (75 - 18) +  # Lower age threshold
            0.25 * features['smoking_risk'] +
            0.2 * features['alcohol_risk'] +
            0.15 * max(0, (features['bmi'] - 18.5) / (32 - 18.5)) +  # Lower BMI threshold
            0.1 * features['cancer_family_history'] * 0.1
        )
        # Apply multiplier to increase scores
        cancer_risk = min(cancer_risk * 1.2, 1.0)
        risk_scores['cancer'] = max(0.01, min(0.99, cancer_risk))
    
    return risk_scores


def generate_recommendations(risk_scores, features):
    """Generate personalized recommendations based on risk assessment"""
    lang = st.session_state.lang
    recommendations = []
    
    # Metabolic & Lifestyle recommendations - Lower threshold for recommendations
    if 'metabolic_lifestyle' in risk_scores and risk_scores['metabolic_lifestyle'] >= 0.3:  # Lowered from 0.4
        recs = RECOMMENDATIONS["metabolic"][lang][:5]  # First 5 recommendations
        if features['bmi'] > 25:
            recs.append(RECOMMENDATIONS["metabolic"][lang][5])
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["metabolic"][lang][6])
        recommendations.append({
            'category': T['category_metabolic'],
            'recommendations': recs
        })
    
    # CVD & Stroke recommendations - Lower threshold
    if 'cvd_stroke' in risk_scores and risk_scores['cvd_stroke'] >= 0.25:  # Lowered from 0.3
        recs = RECOMMENDATIONS["cvd"][lang][:5]  # First 5 recommendations
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cvd"][lang][5])
        if features['stress_score'] > 0.6:
            recs.append(RECOMMENDATIONS["cvd"][lang][6])
        recommendations.append({
            'category': T['category_cvd'],
            'recommendations': recs
        })
    
    # Diabetes recommendations - Lower threshold
    if 'diabetes' in risk_scores and risk_scores['diabetes'] >= 0.3:  # Lowered from 0.4
        recs = RECOMMENDATIONS["diabetes"][lang][:5]  # First 5 recommendations
        if features['bmi'] > 25:
            recs.append(RECOMMENDATIONS["diabetes"][lang][5])
        if features['diabetes_symptoms'] > 0.5:
            recs.append(RECOMMENDATIONS["diabetes"][lang][6])
        recommendations.append({
            'category': T['category_diabetes'],
            'recommendations': recs
        })
    
    # Cancer recommendations - Lower threshold
    if 'cancer' in risk_scores and risk_scores['cancer'] >= 0.25:  # Lowered from 0.3
        recs = RECOMMENDATIONS["cancer"][lang][:5]  # First 5 recommendations
        if features['smoking_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cancer"][lang][5])
        if features['alcohol_risk'] > 0.5:
            recs.append(RECOMMENDATIONS["cancer"][lang][6])
        recommendations.append({
            'category': T['category_cancer'],
            'recommendations': recs
        })
    
    return recommendations

def display_results(risk_scores, recommendations, features):
    """Display risk scores and recommendations"""
    st.header(T['result_header'])
    st.write(T['result_subtext'])
    
    # Always display all 4 categories in the same order
    all_categories = [
        (T['category_metabolic'], 'metabolic_lifestyle'),
        (T['category_cvd'], 'cvd_stroke'),
        (T['category_diabetes'], 'diabetes'),
        (T['category_cancer'], 'cancer')
    ]
    
    # Create 4 columns for the 4 categories
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    def display_risk_metric(label, risk_key, col):
        with col:
            if risk_key in risk_scores:
                value = risk_scores[risk_key]
                st.metric(label, f"{value*100:.1f}%")
                # Updated thresholds
                if value < 0.3:
                    st.success(T['risk_level_low'])
                elif value < 0.5:
                    st.warning(T['risk_level_moderate'])
                else:
                    st.error(T['risk_level_high'])
            else:
                # Show N/A for categories that don't apply
                st.metric(label, "N/A")
                st.info(T['risk_na'])
    
    # Display all 4 categories
    for i, (label, risk_key) in enumerate(all_categories):
        display_risk_metric(label, risk_key, cols[i])
    
    st.header(T['recommendation_header'])
    
    # Create sections for each category - Only show recommendations for moderate/high risk
    if recommendations:
        for rec_cat in recommendations:
            category_name = rec_cat['category']
            category_recommendations = rec_cat['recommendations']
            
            st.subheader(f"🎯 {category_name}")
            
            # Create 2 columns for recommendations and product image
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**{T['recommendations_label']}**")
                for i, rec in enumerate(category_recommendations, 1):
                    st.write(f"{i}. {rec}")
            
            with col2:
                st.write(f"**{T['recommended_product']}**")
                
                # Determine risk key for this category
                risk_key = None
                for cat_name, key in all_categories:
                    if cat_name == category_name:
                        risk_key = key
                        break
                
                # Simple logic for image display
                 # Logic for image display and CTA link based on risk category
                image_path = 'assets/MCU.jpg'  # Default
                caption = "General Health Screening"
                whatsapp_link = WHATSAPP_LINKS['metabolic'] # Default link
                
                if risk_key == 'diabetes':
                    image_path = 'assets/MCU.jpg'
                    caption = "MCU Health Screening" if st.session_state.lang == 'en' else "MCU – Pemeriksaan Kesehatan"
                    whatsapp_link = WHATSAPP_LINKS['diabetes']
                elif risk_key == 'cvd_stroke':
                    image_path = 'assets/StrokeGENME.png'
                    caption = "StrokeGENME - CVD Prevention" if st.session_state.lang == 'en' else "StrokeGENME – Pencegahan Penyakit Jantung"
                    whatsapp_link = WHATSAPP_LINKS['cvd']
                elif risk_key == 'cancer':
                    # Conditional logic for cancer based on risk and age
                    is_high_risk = risk_scores.get('cancer', 0) > 0.5
                    is_older = features['age'] > 40
                    if is_high_risk and is_older:
                        image_path = 'assets/spotmas.jpeg'
                        caption = "SpotMas - High Risk Cancer Screening" if st.session_state.lang == 'en' else "SpotMas – Skrining Kanker Risiko Tinggi"
                        whatsapp_link = WHATSAPP_LINKS['cancer_high_risk']
                    else:
                        image_path = 'assets/Kalscanner69.png'
                        caption = "Kalscanner69 - Cancer Screening" if st.session_state.lang == 'en' else "Kalscanner69 – Deteksi Kanker"
                        whatsapp_link = WHATSAPP_LINKS['cancer']
                elif risk_key == 'metabolic_lifestyle': 
                    image_path = 'assets/GENME_LIFE.png'
                    caption = "GENME Life - Metabolic Health" if st.session_state.lang == 'en' else "GENME Life – Kesehatan Metabolik"
                    whatsapp_link = WHATSAPP_LINKS['metabolic']
                
                try:
                    st.image(image_path, caption=caption, use_container_width=True)
                except:
                    st.error(f"Image not found: {image_path}")
                
                # Add CTA button for each recommendation category
                # if st.button(T['check_promo'], key=f"promo_{risk_key}", use_container_width=True):
                #     st.markdown(T['contact_whatsapp'])
                st.link_button(T['check_promo'], whatsapp_link, use_container_width=True)
            
            st.divider()
    else:
        st.success(T['low_risk_success'])
        st.write(f"**{T['general_maintenance']}**")
        st.write(f"1. {T['maintain_habits']}")
        st.write(f"2. {T['regular_checkups']}")
        st.write(f"3. {T['stay_active']}")
        st.write(f"4. {T['monitor_changes']}")
    
    # Contact Us section
    st.header(T['take_action_header'])
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(T['promo_button'], use_container_width=True):
            st.markdown(T['contact_whatsapp'])
    
    with col2:
        if st.button(T['inquiry_button'], use_container_width=True):
            st.markdown(T['contact_whatsapp'])

DRIVE_FOLDER_ID = '1NrnIvAUszGLMahXanXjgLQ9u0_0oshDZ' 
GOOGLE_SHEET_ID = '13M-qFhz9qVdvgoSu2iRuYBkBaWzqYZaUy9BZzl32eAQ'
#https://docs.google.com/spreadsheets/d/13M-qFhz9qVdvgoSu2iRuYBkBaWzqYZaUy9BZzl32eAQ/edit?gid=0#gid=0

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
        display_results(risk_scores, recommendations, features)
    
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
            submitted = st.form_submit_button(T['submit_button'], icon=":material/check_circle:")
            
            if submitted:
                # # Store the collected data
                # questionnaire_data = {
                #     'personal': personal_data,
                #     'activity': activity_data,
                #     'lifestyle': lifestyle_data,
                #     'health': health_data,
                #     'genetic': genetic_data,
                #     'timestamp': datetime.now().isoformat()  # Add timestamp for uniqueness
                # }
                # st.session_state.questionnaire_data = questionnaire_data
                # st.session_state.show_results = True

                error_messages = []
                if not personal_data['name']:
                    error_messages.append(T['name'])
                # For number inputs, a value <= 0 is considered empty as we removed default values.
                if personal_data['age'] <= 0:
                    error_messages.append(T['age'])
                if personal_data['waist_circumference'] <= 0:
                    error_messages.append(T['waist'])
                if personal_data['height'] <= 0:
                    error_messages.append(T['height'])
                if personal_data['weight'] <= 0:
                    error_messages.append(T['weight'])

                if error_messages:
                    # Display a single error message with all missing fields.
                    # A new translation key 'mandatory_fields_error' was added to the LANG dictionary.
                    error_str = T['mandatory_fields_error'].format(fields=', '.join(error_messages))
                    st.error(error_str)
                    return
                else:
                    # If validation passes, proceed with data processing and storage.
                    # Store the collected data
                    questionnaire_data = {
                    'personal': personal_data,
                    'activity': activity_data,
                    'lifestyle': lifestyle_data,
                    'health': health_data,
                    'genetic': genetic_data,
                    'timestamp': datetime.now().isoformat()  # Add timestamp for uniqueness
                    }
                    st.session_state.questionnaire_data = questionnaire_data
                    st.session_state.show_results = True
                
                # New: Save to local files
                try:
                    # Create submissions directory if it doesn't exist
                    os.makedirs('submissions', exist_ok=True)
                    
                    # Compute features and risk scores (moved here for CSV inclusion)
                    features = process_questionnaire_data(questionnaire_data)
                    risk_scores = calculate_risk_scores(features)
                    
                    # Flatten all data for CSV
                    flat_data = {
                        'timestamp': questionnaire_data['timestamp'],
                        # Personal section
                        'name': questionnaire_data['personal']['name'],
                        'phone': questionnaire_data['personal']['phone'],
                        'age': questionnaire_data['personal']['age'],
                        'sex': questionnaire_data['personal']['sex'],
                        'height': questionnaire_data['personal']['height'],
                        'weight': questionnaire_data['personal']['weight'],
                        'occupation': questionnaire_data['personal']['occupation'],
                        'activity_level': questionnaire_data['personal']['activity_level'],
                        'waist_circumference': questionnaire_data['personal']['waist_circumference'],
                        # Activity section
                        'exercise_frequency': questionnaire_data['activity']['exercise_frequency'],
                        'duration': questionnaire_data['activity']['duration'],
                        'intensity': questionnaire_data['activity']['intensity'],
                        # Lifestyle section
                        'sleep_hours': questionnaire_data['lifestyle']['sleep_hours'],
                        'stress_level': questionnaire_data['lifestyle']['stress_level'],
                        'smoking': questionnaire_data['lifestyle']['smoking'],
                        'alcohol': questionnaire_data['lifestyle']['alcohol'],
                        'total_cholesterol': questionnaire_data['lifestyle']['total_cholesterol'],
                        'blood_pressure_medication': questionnaire_data['lifestyle']['blood_pressure_medication'],
                        'hba1c': questionnaire_data['lifestyle']['hba1c'],
                        'fasting_glucose': questionnaire_data['lifestyle']['fasting_glucose'],
                        'frequent_hunger': questionnaire_data['lifestyle']['frequent_hunger'],
                        'frequent_thirst': questionnaire_data['lifestyle']['frequent_thirst'],
                        'frequent_urination': questionnaire_data['lifestyle']['frequent_urination'],
                        # Health section
                        'conditions': ','.join(questionnaire_data['health']['conditions']),  # Join list as comma-separated string
                        'medications': questionnaire_data['health']['medications'],
                        'diabetes_history': questionnaire_data['health']['diabetes_history'],
                        'cancer_history': questionnaire_data['health']['cancer_history'],
                        'cvd_history': questionnaire_data['health']['cvd_history'],
                        # Symptoms (flattened from dict)
                        'symptom_fatigue': questionnaire_data['health']['symptoms']['fatigue'],
                        'symptom_joint_pain': questionnaire_data['health']['symptoms']['joint_pain'],
                        'symptom_digestive': questionnaire_data['health']['symptoms']['digestive'],
                        'symptom_skin_issues': questionnaire_data['health']['symptoms']['skin_issues'],
                        'symptom_headaches': questionnaire_data['health']['symptoms']['headaches'],
                        'symptom_mood': questionnaire_data['health']['symptoms']['mood'],
                        'symptom_cognitive': questionnaire_data['health']['symptoms']['cognitive'],
                        'symptom_sleep_issues': questionnaire_data['health']['symptoms']['sleep_issues'],
                        # Genetic section
                        'had_testing': questionnaire_data['genetic']['had_testing'],
                        'findings': questionnaire_data['genetic']['findings'],
                        # Calculated BMI (optional, but included as per original)
                        'bmi': questionnaire_data['personal']['weight'] / ((questionnaire_data['personal']['height']/100) ** 2) if questionnaire_data['personal']['height'] > 0 else 0,
                        # New: Risk scores as percentages (N/A if not calculated, e.g., due to existing condition)
                        'metabolic_risk': round(risk_scores.get('metabolic_lifestyle', 0) * 100, 1) if 'metabolic_lifestyle' in risk_scores else 'N/A',
                        'cvd_risk': round(risk_scores.get('cvd_stroke', 0) * 100, 1) if 'cvd_stroke' in risk_scores else 'N/A',
                        'diabetes_risk': round(risk_scores.get('diabetes', 0) * 100, 1) if 'diabetes' in risk_scores else 'N/A',
                        'cancer_risk': round(risk_scores.get('cancer', 0) * 100, 1) if 'cancer' in risk_scores else 'N/A'
                    }
                    
                     # Save to CSV (append mode) - unchanged
                    csv_path = 'submissions/submissions.csv'
                    file_exists = os.path.isfile(csv_path)
                    with open(csv_path, 'a', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=flat_data.keys())
                        if not file_exists:
                            writer.writeheader()  # Write header only once
                        writer.writerow(flat_data)
                    
                    # Save to JSON (new file per submission)
                    json_path = f'submissions/submission_{questionnaire_data["timestamp"].replace(":", "-")}.json'
                    with open(json_path, 'w') as jsonfile:
                        json.dump(questionnaire_data, jsonfile, indent=4)
                    
                     # --- NEW: Append data to Google Sheets ---
                    print("DEBUG: Starting Google Sheets authentication...")
                    
                    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                    
                    # Check for local credentials file FIRST
                    if os.path.exists('dnacare.json'):
                        print("DEBUG: Using local file 'dnacare.json' for credentials.")
                        creds = ServiceAccountCredentials.from_json_keyfile_name('dnacare.json', scopes)
                    # If no local file, check for Streamlit secrets (for deployment)
                    elif 'GOOGLE_CREDENTIALS' in st.secrets:
                        print("DEBUG: Using Streamlit secrets for credentials.")
                        #creds_dict = json.loads(st.secrets['GOOGLE_CREDENTIALS'])
                        creds_dict = st.secrets['GOOGLE_CREDENTIALS']
                        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
                    # If neither is found, raise an error
                    else:
                        raise FileNotFoundError("Could not find 'dnacare.json' for local development or GOOGLE_CREDENTIALS secret for deployment.")

                    client = gspread.authorize(creds)
                    print("DEBUG: Authentication successful.")
                    
                    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
                    worksheet = spreadsheet.sheet1
                    print(f"DEBUG: Opened worksheet '{worksheet.title}'.")
                    
                    if not worksheet.row_values(1):
                        worksheet.append_row(list(flat_data.keys()))
                        print("DEBUG: Added header row to empty sheet.")
                    
                    worksheet.append_row(list(flat_data.values()))
                    print("DEBUG: Appended new row to Google Sheet.")
                    
                    # On success, set state and rerun to show results
                    st.session_state.show_results = True
                    st.success(T['success_msg'])
                    st.balloons()
                    st.components.v1.html("""
                    <script>
                    setTimeout(function() {
                        // Try scrolling the window
                        window.scrollTo({top: 0, left: 0, behavior: 'smooth'});
                        // Try scrolling the document
                        document.body.scrollTop = 0;
                        document.documentElement.scrollTop = 0;
                        // Try focusing the first Streamlit element
                        var firstInput = document.querySelector('input, textarea, select, button');
                        if (firstInput) { firstInput.focus(); }
                        // Try scrolling the first element into view
                        if (document.body.firstElementChild) {
                            document.body.firstElementChild.scrollIntoView({behavior: 'smooth', block: 'start'});
                        }
                    }, 100);
                    </script>
                    """, height=0)
                    st.rerun()
                
                except Exception as e:
                    # Show a user-friendly error message instead of technical details
                    if st.session_state.lang == 'en':
                        st.error("There was a problem saving your data. Please try again.")
                    else:
                        st.error("Terjadi masalah saat menyimpan data Anda. Silakan coba lagi.")
                # except Exception as e:
                #     # On error, this message will now stay on the screen
                #     st.error(f"An error occurred: {str(e)}")
                #     # Ensure we don't try to show results on failure
                #     st.session_state.show_results = False
                    
                    # New: Upload JSON to Google Drive using service account
                    # Set up authentication
                #     gauth = GoogleAuth()
                #     print("DEBUG: Starting authentication...")  # Will show in runtime logs
                    
                #     local_credentials_file = 'dnacare.json'
                #     if os.path.exists(local_credentials_file):  # Prefer local file if it exists (for testing)
                #         print("DEBUG: Local credentials file found - using local loading")
                #         try:
                #             gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                #                 local_credentials_file,
                #                 scopes=['https://www.googleapis.com/auth/drive']
                #             )
                #             print("DEBUG: Local credentials loaded successfully")
                #         except Exception as local_auth_err:
                #             print(f"DEBUG: Local credentials loading failed: {str(local_auth_err)}")
                #             raise
                #     elif 'GOOGLE_CREDENTIALS' in st.secrets:  # For Streamlit Cloud deployment
                #         print("DEBUG: Using Streamlit secrets for credentials")
                #         try:
                #             credentials_dict = json.loads(st.secrets['GOOGLE_CREDENTIALS'])
                #             gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                #                 credentials_dict,
                #                 scopes=['https://www.googleapis.com/auth/drive']
                #             )
                #             print("DEBUG: Credentials loaded from secrets successfully")
                #         except Exception as auth_err:
                #             print(f"DEBUG: Secrets loading failed: {str(auth_err)}")
                #             raise  # Re-raise to catch in outer except
                #     else:
                #         raise ValueError("DEBUG: No credentials found - place 'dnacare.json' locally or set secrets for deployment")
                    
                #     if gauth.credentials is None:
                #         raise ValueError("DEBUG: Authentication failed - credentials are None")
                    
                #     print("DEBUG: Creating GoogleDrive instance")
                #     drive = GoogleDrive(gauth)
                    
                #     print("DEBUG: Preparing file metadata")
                #     file_metadata = {
                #         'title': os.path.basename(json_path),  # e.g., submission_2023-10-01T12-00-00.json
                #         'parents': [{'id': DRIVE_FOLDER_ID}],  # Upload to specific folder
                #         'driveId': DRIVE_FOLDER_ID
                #     }
                #     upload_file = drive.CreateFile(file_metadata)
                #     upload_file.metadata['supportsAllDrives'] = True 
                #     upload_file.SetContentFile(json_path)
                    
                #     print(f"DEBUG: Uploading file: {json_path}")
                #     try:
                #         upload_file.Upload()
                #         print("DEBUG: Upload completed successfully")
                #     except Exception as upload_err:
                #         print(f"DEBUG: Upload failed: {str(upload_err)}")
                #         raise  # Re-raise to show in st.error
                    
                #     st.success(f"Data saved locally to CSV/JSON and uploaded to Google Drive as {file_metadata['title']}!")
                # except Exception as e:
                #     st.error(f"Error saving/uploading data: {str(e)}")
                
                # # Show success message and rerun to show results
                # st.success(T['success_msg'])
                # st.balloons()
                # st.rerun()


# def main():
#     # Initialize session state
#     if 'show_results' not in st.session_state:
#         st.session_state.show_results = False
    
#     # Check if results should be shown and auto-select Results tab
#     if st.session_state.show_results:
#         # Show results directly without tabs when calculation is complete
#         st.header(T['results_title'])
        
#         # Add a button to go back to questionnaire
#         if st.button(T['back_button']):
#             st.session_state.show_results = False
#             st.rerun()
        
#         # Process and display results
#         features = process_questionnaire_data(st.session_state.questionnaire_data)
#         risk_scores = calculate_risk_scores(features)
#         recommendations = generate_recommendations(risk_scores, features)
#         display_results(risk_scores, recommendations)
        
#     else:
#         # Show questionnaire form
#         st.header(T['form_title'])
        
#         with st.form("health_questionnaire"):
#             # Collect data from each section
#             personal_data = personal_info_section()
#             activity_data = physical_activity_section()
#             lifestyle_data = lifestyle_section()
#             health_data = health_conditions_section()
#             genetic_data = genetic_testing_section()
            
#             # Submit button
#             submitted = st.form_submit_button(T['submit_button'], icon=":material/check_circle:")
            
#             if submitted:
#                 # Store the collected data
#                 st.session_state.questionnaire_data = {
#                     'personal': personal_data,
#                     'activity': activity_data,
#                     'lifestyle': lifestyle_data,
#                     'health': health_data,
#                     'genetic': genetic_data
#                 }
#                 st.session_state.show_results = True
                
#                 # Show success message and rerun to show results
#                 st.success(T['success_msg'])
#                 st.balloons()
#                 st.rerun()

if __name__ == "__main__":
    main()
