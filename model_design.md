# Prediction Model Design and Implementation

Based on the genetic data and questionnaire, this document outlines the prediction model architecture and implementation approach.

## 1. Model Architecture Overview

The system will use a multi-model approach where specialized models focus on different disease/condition categories. This approach is more accurate than a single monolithic model since different genetic markers and lifestyle factors influence different health outcomes.

```
┌───────────────────────────────────────────────────────┐
│                                                       │
│                   Feature Processing                  │
│                                                       │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                                                       │
│                  Risk Score Calculator                │
│                                                       │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│             │  │             │  │             │  │             │
│ Nutritional │  │ Metabolic   │  │ Fitness &   │  │ Other       │
│ Risk Models │  │ Risk Models │  │ Recovery    │  │ Specialized │
│             │  │             │  │ Models      │  │ Models      │
│             │  │             │  │             │  │             │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┼────────────────┼────────────────┘
                        │                │
                        ▼                ▼
┌───────────────────────────────────────────────────────┐
│                                                       │
│               Model Ensemble & Calibration            │
│                                                       │
└──────────────────────────┬────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────┐
│                                                       │
│           Personalized Recommendation Engine           │
│                                                       │
└───────────────────────────────────────────────────────┘
```

## 2. Data Preprocessing and Feature Engineering

### 2.1 Genetic Data Processing

```python
def process_genetic_data(genetic_data):
    """
    Process raw genetic data into features usable by prediction models.
    """
    # Create gene-specific features
    processed_features = {}
    
    # Group by phenotype
    phenotype_groups = genetic_data.groupby('Phenotype')
    
    for phenotype, group in phenotype_groups:
        # Calculate risk scores for each phenotype based on gene results and impacts
        risk_score = calculate_phenotype_risk(group)
        processed_features[f"{phenotype}_risk"] = risk_score
        
        # Create gene-specific binary features
        for _, row in group.iterrows():
            gene_name = row['GeneNames']
            gene_result = row['GeneResult']
            gene_impact = row['GeneImpact']
            
            # Create binary features for high-impact variants
            if 'High Impact' in gene_impact:
                feature_name = f"{gene_name}_{gene_result}_high_impact"
                processed_features[feature_name] = 1
    
    return processed_features

def calculate_phenotype_risk(phenotype_group):
    """
    Calculate risk score for a phenotype based on gene variants and their impacts.
    """
    risk_score = 0
    max_score = 0
    
    impact_weights = {
        'No Impact': 0,
        'Low Impact': 1,
        'Moderate Impact': 2,
        'High Impact': 3,
        'Beneficial Impact': -1
    }
    
    for _, row in phenotype_group.iterrows():
        impact = row['GeneImpact']
        # Handle composite impacts (e.g., "High Impact|No Impact")
        if '|' in impact:
            impacts = impact.split('|')
            weight = max(impact_weights.get(imp, 0) for imp in impacts)
        else:
            weight = impact_weights.get(impact, 0)
        
        risk_score += weight
        max_score += 3  # Maximum possible weight
    
    # Normalize to 0-1 scale
    if max_score > 0:
        normalized_score = (risk_score + max_score) / (2 * max_score)  # Scale to 0-1
    else:
        normalized_score = 0.5  # Default to moderate risk if no data
        
    return normalized_score
```

### 2.2 Questionnaire Data Processing

```python
def process_questionnaire_data(questionnaire_responses):
    """
    Process questionnaire responses into numerical features.
    """
    features = {}
    
    # Demographic features
    features['age'] = questionnaire_responses.get('age', 0)
    features['bmi'] = calculate_bmi(
        questionnaire_responses.get('weight', 0), 
        questionnaire_responses.get('height', 0)
    )
    
    # Convert categorical to numerical
    features['gender_male'] = 1 if questionnaire_responses.get('gender') == 'Male' else 0
    
    # Process dietary patterns
    diet_type = questionnaire_responses.get('diet_pattern', '')
    features['diet_mediterranean'] = 1 if 'Mediterranean' in diet_type else 0
    features['diet_lowcarb'] = 1 if any(x in diet_type for x in ['Low-carb', 'Keto']) else 0
    features['diet_plant_based'] = 1 if any(x in diet_type for x in ['Vegetarian', 'Vegan']) else 0
    
    # Calculate dietary quality score
    features['diet_quality'] = calculate_diet_quality(questionnaire_responses)
    
    # Process physical activity
    features['met_hours'] = calculate_met_hours(questionnaire_responses)
    features['strength_training_freq'] = convert_frequency_to_numeric(
        questionnaire_responses.get('strength_training_freq', 'Never')
    )
    
    # Process sleep patterns
    features['sleep_hours'] = map_sleep_hours(questionnaire_responses.get('sleep_hours', '7-8'))
    features['sleep_quality'] = map_quality_scale(questionnaire_responses.get('sleep_quality', 'Good'))
    
    # Process stress
    features['stress_level'] = map_stress_level(questionnaire_responses.get('stress_level', 'Moderate'))
    
    # Process other lifestyle factors
    features['smoking_status'] = map_smoking_status(questionnaire_responses.get('smoking_status', 'Never smoked'))
    features['alcohol_consumption'] = calculate_alcohol_consumption(questionnaire_responses)
    
    # Create composite scores for different domains
    features['cardiovascular_lifestyle_score'] = calculate_cv_lifestyle_score(questionnaire_responses)
    features['metabolic_lifestyle_score'] = calculate_metabolic_lifestyle_score(questionnaire_responses)
    features['inflammation_lifestyle_score'] = calculate_inflammation_score(questionnaire_responses)
    
    return features

def calculate_met_hours(responses):
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
        '<15': 0.25,
        '15-30': 0.375,
        '30-45': 0.625,
        '45-60': 0.875,
        '60+': 1.25
    }
    
    # Get values from responses with defaults
    intensity = responses.get('exercise_intensity', 'Moderate')
    frequency = responses.get('exercise_frequency', 'Never')
    duration = responses.get('exercise_duration', '30-45')
    
    # Calculate MET hours per week
    met_value = intensity_to_met.get(intensity, 4.5)
    times_per_week = freq_to_num.get(frequency, 0)
    hours_per_session = duration_to_hours.get(duration, 0.625)
    
    met_hours = met_value * times_per_week * hours_per_session
    
    return met_hours
```

### 2.3 Feature Integration

```python
def integrate_features(genetic_features, questionnaire_features):
    """
    Integrate genetic and questionnaire features, including interaction terms.
    """
    integrated_features = {}
    
    # Combine all features
    integrated_features.update(genetic_features)
    integrated_features.update(questionnaire_features)
    
    # Create interaction terms for known gene-environment interactions
    
    # Example: Caffeine metabolism genes × caffeine consumption
    if 'CYP1A2_AA_high_impact' in genetic_features and 'caffeine_cups_daily' in questionnaire_features:
        integrated_features['caffeine_metabolism_risk'] = (
            genetic_features['CYP1A2_AA_high_impact'] * 
            questionnaire_features['caffeine_cups_daily']
        )
    
    # Example: Vitamin D genes × sun exposure and supplementation
    if 'Vitamin D_risk' in genetic_features:
        vit_d_genetic_risk = genetic_features['Vitamin D_risk']
        sun_exposure = questionnaire_features.get('sun_exposure_hours', 0.5)
        vitamin_d_suppl = questionnaire_features.get('vitamin_d_supplementation', 0)
        
        # Lower risk if adequate sun exposure or supplementation despite genetic risk
        integrated_features['vitamin_d_adjusted_risk'] = (
            vit_d_genetic_risk * 
            (1 - 0.3 * min(sun_exposure / 2.0, 1)) *  # Sun exposure reduces risk by up to 30%
            (1 - 0.5 * vitamin_d_suppl)  # Supplementation reduces risk by 50% if taken
        )
    
    # Example: Weight-related genes × dietary patterns
    if 'FTO_AA_high_impact' in genetic_features and 'diet_quality' in questionnaire_features:
        # The FTO gene effect is modified by diet quality
        integrated_features['obesity_adjusted_risk'] = (
            genetic_features.get('FTO_AA_high_impact', 0) * 
            (2 - questionnaire_features['diet_quality'])  # Higher diet quality reduces genetic risk
        )
    
    return integrated_features
```

## 3. Model Development

### 3.1 Model Types for Different Risk Categories

Based on the data analysis, we'll implement different model types for various health categories:

#### 3.1.1 Nutrient Metabolism Models

```python
def build_nutrient_models(training_data):
    """
    Build models for predicting risks related to nutrient metabolism.
    """
    models = {}
    
    # List of nutrients from data analysis
    nutrients = [
        'Vitamin A', 'Vitamin B2', 'Vitamin B6', 'Vitamin B12', 
        'Vitamin C', 'Vitamin D', 'Vitamin E', 'Folate',
        'Calcium', 'Magnesium', 'Iron', 'Zinc'
    ]
    
    for nutrient in nutrients:
        # Prepare data for this specific nutrient
        X, y = prepare_nutrient_data(training_data, nutrient)
        
        if len(X) < 50:  # Not enough data for complex model
            # Use simpler logistic regression model
            models[nutrient] = LogisticRegression()
        else:
            # Use gradient boosting for more complex patterns
            models[nutrient] = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3
            )
        
        # Train the model
        models[nutrient].fit(X, y)
    
    return models
```

#### 3.1.2 Metabolic Health Models

```python
def build_metabolic_models(training_data):
    """
    Build models for predicting metabolic health risks.
    """
    models = {}
    
    # Metabolic conditions
    conditions = [
        'Type 2 Diabetes', 
        'Cardiovascular Disease',
        'Obesity',
        'Hypercholesterolemia',
        'Hypertriglyceridemia'
    ]
    
    for condition in conditions:
        # Prepare data
        X, y = prepare_condition_data(training_data, condition)
        
        # Random Forest for complex interactions
        models[condition] = RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            min_samples_leaf=10
        )
        
        # Train with cross-validation for hyperparameter tuning
        cv_params = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7],
            'min_samples_leaf': [5, 10, 20]
        }
        
        grid_search = GridSearchCV(
            models[condition],
            cv_params,
            cv=5,
            scoring='roc_auc'
        )
        
        grid_search.fit(X, y)
        models[condition] = grid_search.best_estimator_
    
    return models
```

#### 3.1.3 Fitness and Recovery Models

```python
def build_fitness_models(training_data):
    """
    Build models for fitness-related predictions.
    """
    models = {}
    
    # Fitness-related aspects
    aspects = [
        'Power_vs_Endurance',
        'Injury_Risk',
        'Recovery_Rate'
    ]
    
    for aspect in aspects:
        # Prepare data
        X, y = prepare_fitness_data(training_data, aspect)
        
        if aspect == 'Power_vs_Endurance':
            # This is more of a continuum, so use regression
            models[aspect] = XGBRegressor(
                n_estimators=100,
                learning_rate=0.05,
                max_depth=4
            )
        else:
            # Classification for binary outcomes
            models[aspect] = XGBClassifier(
                n_estimators=100,
                learning_rate=0.05,
                max_depth=4
            )
        
        # Train the model
        models[aspect].fit(X, y)
    
    return models
```

### 3.2 Model Ensemble and Calibration

```python
def create_model_ensemble(individual_models, calibration_data):
    """
    Create an ensemble of models with proper calibration.
    """
    ensemble = {}
    
    # For each condition/aspect, create a calibrated version
    for condition, model in individual_models.items():
        # Prepare calibration data
        X_cal, y_cal = prepare_calibration_data(calibration_data, condition)
        
        # Apply calibration to get well-calibrated probabilities
        calibrated_model = CalibratedClassifierCV(
            base_estimator=model,
            method='isotonic',
            cv='prefit'
        )
        
        # Fit calibration
        calibrated_model.fit(X_cal, y_cal)
        ensemble[condition] = calibrated_model
    
    return ensemble
```

### 3.3 Feature Importance and Interpretability

```python
def extract_feature_importance(models):
    """
    Extract and process feature importance from trained models.
    """
    importance_dict = {}
    
    for condition, model in models.items():
        # Check if model has feature_importances_ attribute (tree-based models)
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            feature_names = model.feature_names_in_
            
            # Create sorted importance tuples
            importance_tuples = sorted(
                zip(feature_names, importances),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Store top 10 most important features
            importance_dict[condition] = importance_tuples[:10]
        
        # For linear models, use coefficients
        elif hasattr(model, 'coef_'):
            coefs = model.coef_[0] if model.coef_.ndim > 1 else model.coef_
            feature_names = model.feature_names_in_
            
            # Create sorted importance tuples
            importance_tuples = sorted(
                zip(feature_names, abs(coefs)),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Store top 10 most important features
            importance_dict[condition] = importance_tuples[:10]
    
    return importance_dict
```

## 4. Risk Score Calculation

```python
def calculate_risk_scores(patient_features, ensemble_models):
    """
    Calculate risk scores for a patient across all conditions.
    """
    risk_scores = {}
    confidence_levels = {}
    relevant_factors = {}
    
    # For each condition/aspect, predict risk
    for condition, model in ensemble_models.items():
        # Prepare feature vector for this condition
        X = prepare_prediction_features(patient_features, condition)
        
        # Get prediction probability (risk score)
        if hasattr(model, 'predict_proba'):
            # For classifiers
            proba = model.predict_proba(X)[0]
            risk_scores[condition] = proba[1]  # Probability of positive class
        else:
            # For regressors, normalize output to 0-1 scale
            prediction = model.predict(X)[0]
            risk_scores[condition] = scale_prediction_to_risk(prediction, condition)
        
        # Calculate confidence based on data coverage
        confidence_levels[condition] = calculate_confidence(X, model)
        
        # Extract most relevant factors for this prediction
        relevant_factors[condition] = extract_relevant_factors(X, model, condition)
    
    return {
        'risk_scores': risk_scores,
        'confidence': confidence_levels,
        'relevant_factors': relevant_factors
    }

def scale_prediction_to_risk(raw_prediction, condition):
    """
    Scale a raw prediction value to a risk score between 0 and 1.
    """
    # Condition-specific scaling logic
    if condition == 'Power_vs_Endurance':
        # Convert -1 (power) to 1 (endurance) scale to 0-1 risk scale
        return (raw_prediction + 1) / 2
    
    # Default min-max scaling with domain knowledge
    condition_ranges = {
        'Recovery_Rate': (0, 100),  # 0 to 100 hours
        'VO2Max': (20, 80)  # mL/(kg·min)
    }
    
    if condition in condition_ranges:
        min_val, max_val = condition_ranges[condition]
        normalized = (raw_prediction - min_val) / (max_val - min_val)
        return max(0, min(1, normalized))
    
    # Default normalization if no specific range
    return max(0, min(1, raw_prediction))
```

## 5. Personalized Recommendation Engine

```python
def generate_recommendations(risk_assessment, patient_features):
    """
    Generate personalized recommendations based on risk assessment.
    """
    recommendations = []
    
    # Prioritize high-risk areas
    prioritized_risks = sorted(
        risk_assessment['risk_scores'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Generate recommendations for top risks
    for condition, risk_score in prioritized_risks[:5]:  # Focus on top 5 risks
        if risk_score > 0.7:  # High risk
            severity = "high"
        elif risk_score > 0.4:  # Moderate risk
            severity = "moderate"
        else:  # Low risk
            severity = "low"
        
        # Get condition-specific recommendations
        condition_recs = get_condition_recommendations(
            condition, 
            severity,
            risk_assessment['relevant_factors'][condition],
            patient_features
        )
        
        recommendations.extend(condition_recs)
    
    # Add general health recommendations
    general_recs = get_general_recommendations(patient_features)
    recommendations.extend(general_recs)
    
    # Deduplicate and prioritize recommendations
    final_recommendations = deduplicate_recommendations(recommendations)
    prioritized_recommendations = prioritize_recommendations(final_recommendations)
    
    return prioritized_recommendations

def get_condition_recommendations(condition, severity, factors, patient_features):
    """
    Get specific recommendations for a condition based on severity and relevant factors.
    """
    recommendations = []
    
    # Example recommendation logic for Vitamin D
    if condition == 'Vitamin D':
        if severity == "high":
            if patient_features.get('sun_exposure_hours', 0) < 0.5:
                recommendations.append({
                    'category': 'Lifestyle',
                    'recommendation': 'Increase sun exposure to 15-30 minutes daily',
                    'priority': 'high',
                    'rationale': 'Your genetic profile indicates higher vitamin D needs, while your current sun exposure is limited.'
                })
            
            recommendations.append({
                'category': 'Supplementation',
                'recommendation': 'Consider vitamin D supplementation of 2000-4000 IU daily',
                'priority': 'high',
                'rationale': 'Your genetic variants in VDR and GC genes indicate you may need higher vitamin D intake.'
            })
    
    # Example recommendation logic for Type 2 Diabetes
    elif condition == 'Type 2 Diabetes':
        if severity in ["moderate", "high"]:
            if 'TCF7L2' in str(factors):
                recommendations.append({
                    'category': 'Diet',
                    'recommendation': 'Reduce refined carbohydrate intake and focus on low glycemic index foods',
                    'priority': 'high',
                    'rationale': 'Your TCF7L2 genetic variant is associated with glucose metabolism issues that can be managed with dietary changes.'
                })
            
            if patient_features.get('met_hours', 0) < 10:
                recommendations.append({
                    'category': 'Exercise',
                    'recommendation': 'Increase physical activity to at least 150 minutes of moderate exercise weekly',
                    'priority': 'high',
                    'rationale': 'Regular physical activity improves insulin sensitivity and can significantly reduce your genetic risk.'
                })
    
    # Add more condition-specific recommendation logic here
    
    return recommendations
```

## 6. Implementation Strategy

### 6.1 Technology Stack

```python
# Key libraries for model implementation
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier, XGBRegressor
import shap  # For model explainability

# Web framework for API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Database interaction
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For frontend
# React + TypeScript will be used
```

### 6.2 API Design

```python
# FastAPI implementation
app = FastAPI(title="Disease Risk Prediction API")

class GeneticData(BaseModel):
    barcode_id: str
    gene_data: list

class QuestionnaireData(BaseModel):
    user_id: str
    responses: dict

class PredictionRequest(BaseModel):
    user_id: str
    genetic_data_id: str
    questionnaire_data_id: str

@app.post("/api/v1/predictions")
async def generate_prediction(request: PredictionRequest):
    # Retrieve genetic and questionnaire data from database
    genetic_data = get_genetic_data(request.genetic_data_id)
    questionnaire_data = get_questionnaire_data(request.questionnaire_data_id)
    
    # Process features
    genetic_features = process_genetic_data(genetic_data)
    questionnaire_features = process_questionnaire_data(questionnaire_data)
    integrated_features = integrate_features(genetic_features, questionnaire_features)
    
    # Load models
    models = load_prediction_models()
    
    # Generate risk assessment
    risk_assessment = calculate_risk_scores(integrated_features, models)
    
    # Generate recommendations
    recommendations = generate_recommendations(risk_assessment, integrated_features)
    
    # Create response
    response = {
        "user_id": request.user_id,
        "prediction_id": generate_unique_id(),
        "timestamp": get_current_timestamp(),
        "risk_assessment": risk_assessment,
        "recommendations": recommendations
    }
    
    # Store prediction in database
    store_prediction(response)
    
    return response
```

### 6.3 Database Schema

```sql
-- PostgreSQL schema

-- User table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_of_birth DATE,
    gender VARCHAR(20),
    height NUMERIC,
    weight NUMERIC
);

-- Genetic data table
CREATE TABLE genetic_data (
    genetic_data_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    barcode_id VARCHAR(100),
    date_of_report DATE,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Gene results table
CREATE TABLE gene_results (
    gene_result_id SERIAL PRIMARY KEY,
    genetic_data_id INTEGER REFERENCES genetic_data(genetic_data_id),
    phenotype VARCHAR(100),
    gene_name VARCHAR(100),
    rsid VARCHAR(50),
    gene_result VARCHAR(20),
    gene_impact VARCHAR(100),
    result VARCHAR(100)
);

-- Questionnaire responses table
CREATE TABLE questionnaire_responses (
    response_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Questionnaire answers table
CREATE TABLE questionnaire_answers (
    answer_id SERIAL PRIMARY KEY,
    response_id INTEGER REFERENCES questionnaire_responses(response_id),
    question_id VARCHAR(100),
    answer TEXT,
    numeric_value NUMERIC
);

-- Risk predictions table
CREATE TABLE risk_predictions (
    prediction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    genetic_data_id INTEGER REFERENCES genetic_data(genetic_data_id),
    questionnaire_id INTEGER REFERENCES questionnaire_responses(response_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    prediction_data JSONB
);

-- Recommendations table
CREATE TABLE recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    prediction_id INTEGER REFERENCES risk_predictions(prediction_id),
    category VARCHAR(100),
    recommendation TEXT,
    priority VARCHAR(20),
    rationale TEXT,
    followed BOOLEAN DEFAULT FALSE
);
```

### 6.4 Deployment Architecture

```
# Docker Compose configuration for deployment

version: '3'

services:
  # Web application
  web:
    build: ./web
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/riskprediction
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - MODEL_PATH=/app/models/
    volumes:
      - ./models:/app/models
    restart: always

  # Frontend application
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - web
    restart: always

  # Database
  db:
    image: postgres:14
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=riskprediction
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  # Redis for caching
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    restart: always

  # ML model service (optional microservice)
  ml_service:
    build: ./ml_service
    ports:
      - "8001:8001"
    volumes:
      - ./models:/app/models
    restart: always

volumes:
  postgres_data:
```

## 7. Testing and Validation Strategy

```python
def validate_system(test_data, models):
    """
    Validate the entire prediction system.
    """
    # Split data
    train_data, test_data = train_test_split(test_data, test_size=0.2, random_state=42)
    
    # Train models
    trained_models = train_all_models(train_data)
    
    # Validate each model
    model_metrics = {}
    for condition, model in trained_models.items():
        # Prepare test data
        X_test, y_test = prepare_test_data(test_data, condition)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        metrics = calculate_model_metrics(y_test, y_pred, y_prob)
        model_metrics[condition] = metrics
        
        # Generate calibration curve
        if y_prob is not None:
            calibration_curve = generate_calibration_curve(y_test, y_prob)
            model_metrics[condition]['calibration'] = calibration_curve
    
    # Validate recommendations
    recommendation_quality = validate_recommendations(test_data, trained_models)
    
    return {
        'model_metrics': model_metrics,
        'recommendation_quality': recommendation_quality
    }

def calculate_model_metrics(y_true, y_pred, y_prob=None):
    """
    Calculate comprehensive model evaluation metrics.
    """
    metrics = {}
    
    # Basic classification metrics
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    metrics['precision'] = precision_score(y_true, y_pred, average='weighted')
    metrics['recall'] = recall_score(y_true, y_pred, average='weighted')
    metrics['f1'] = f1_score(y_true, y_pred, average='weighted')
    
    # Confusion matrix
    metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()
    
    # If probability scores available
    if y_prob is not None:
        metrics['auc_roc'] = roc_auc_score(y_true, y_prob)
        metrics['log_loss'] = log_loss(y_true, y_prob)
        
        # Calculate brier score for calibration quality
        metrics['brier_score'] = brier_score_loss(y_true, y_prob)
        
    return metrics

def validate_recommendations(test_data, models):
    """
    Validate the quality of recommendations generated by the system.
    """
    recommendation_metrics = {}
    
    # Sample a subset of test data
    sample_size = min(100, len(test_data))
    test_sample = test_data.sample(n=sample_size, random_state=42)
    
    # For each test case, generate recommendations
    coverage_count = 0
    relevance_scores = []
    diversity_scores = []
    
    for _, test_case in test_sample.iterrows():
        # Process features
        features = extract_features_from_test_case(test_case)
        
        # Generate risk assessment
        risk_assessment = calculate_risk_scores(features, models)
        
        # Generate recommendations
        recommendations = generate_recommendations(risk_assessment, features)
        
        # Evaluate recommendation quality
        if len(recommendations) > 0:
            coverage_count += 1
        
        relevance_score = evaluate_recommendation_relevance(recommendations, risk_assessment)
        relevance_scores.append(relevance_score)
        
        diversity_score = evaluate_recommendation_diversity(recommendations)
        diversity_scores.append(diversity_score)
    
    # Calculate metrics
    recommendation_metrics['coverage'] = coverage_count / sample_size
    recommendation_metrics['avg_relevance'] = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
    recommendation_metrics['avg_diversity'] = sum(diversity_scores) / len(diversity_scores) if diversity_scores else 0
    
    return recommendation_metrics