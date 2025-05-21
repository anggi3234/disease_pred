# Disease Risk Prediction System Documentation

## System Overview

The disease risk prediction system is a comprehensive health assessment tool that combines various lifestyle, environmental, and health factors to generate personalized risk scores and recommendations. The system follows a modular approach with distinct components for data collection, processing, risk calculation, and recommendation generation.

## Architecture

```d2
direction: down

questionnaire: Questionnaire Data Collection {
  personal: Personal Information
  diet: Dietary Patterns
  activity: Physical Activity
  lifestyle: Lifestyle Factors
  environmental: Environmental Factors
  health: Health Conditions
  weight: Weight Management
  eating: Eating Behaviors
  genetic: Genetic Testing History
}

processing: Data Processing Layer {
  features: Feature Engineering
  scoring: Risk Score Calculation
  recommendations: Recommendation Engine
}

display: Results Display {
  scores: Risk Scores
  advice: Personalized Recommendations
}

questionnaire -> processing: Raw Data
processing -> display: Processed Results

style {
  fill: "#f5f5f5"
  stroke: "#333"
  stroke-width: 2
  font-size: 14
}
```

## Data Collection and Processing

### 1. Feature Engineering

The system processes raw questionnaire data into numerical features through several specialized functions:

#### 1.1 Demographic Features
```python
features['age'] = data['personal']['age']
features['bmi'] = data['personal']['weight'] / ((data['personal']['height']/100) ** 2)
features['gender_male'] = 1 if data['personal']['sex'] == 'Male' else 0
```

BMI calculation follows WHO standards:
- Underweight: < 18.5
- Normal: 18.5 - 24.9
- Overweight: 25 - 29.9
- Obese: ≥ 30

### 2. Risk Score Calculations

#### 2.1 Diet Quality Score
```python
def calculate_diet_quality(diet_data):
    score = 0
    max_score = 8
    
    # Healthy food contributions
    score += min(convert_portion(diet_data['fruits']) / 3, 1)
    score += min(convert_portion(diet_data['vegetables']) / 3, 1)
    score += min(convert_portion(diet_data['whole_grains']) / 3, 1)
    score += min(convert_portion(diet_data['fish']) / 2, 1)
    score += min(convert_portion(diet_data['legumes']) / 2, 1)
```

Based on:
- Mediterranean Diet Score components
- Harvard Healthy Eating Plate guidelines
- WHO dietary recommendations

#### 2.2 Physical Activity Score (MET Hours)
```python
def calculate_met_hours(activity_data):
    intensity_to_met = {
        'Light': 2.5,
        'Moderate': 4.5,
        'Vigorous': 7.0,
        'Very vigorous': 10.0
    }
```

MET values based on:
- Compendium of Physical Activities (Ainsworth et al., 2011)
- WHO Global Recommendations on Physical Activity for Health

#### 2.3 Sleep Score
```python
def calculate_sleep_score(lifestyle_data):
    sleep_hours_map = {
        '<5': 0.2,
        '5-6': 0.4,
        '6-7': 0.6,
        '7-8': 1.0,
        '8-9': 0.8,
        '9+': 0.6
    }
```

Based on:
- National Sleep Foundation guidelines
- Sleep duration recommendations by age group

### 3. Risk Score Components

#### 3.1 Metabolic Health Risk
```python
metabolic_risk = (
    0.25 * (features['bmi'] - 18.5) / (30 - 18.5) +  # BMI contribution
    0.2 * (1 - features['diet_quality']) +           # Diet contribution
    0.15 * (1 - min(features['met_hours'] / 40, 1)) + # Activity contribution
    0.15 * features['eating_behavior_score'] +       # Eating behavior
    0.15 * features['stress_score'] +                # Stress contribution
    0.1 * features['smoking_risk']                   # Smoking contribution
)
```

Weightings based on:
- WHO risk factor studies
- Meta-analyses of lifestyle factors in metabolic health
- Clinical guidelines for metabolic syndrome

#### 3.2 Cardiovascular Risk
```python
cv_risk = (
    0.2 * (features['age'] - 20) / (80 - 20) +      # Age contribution
    0.2 * (1 - features['diet_quality']) +          # Diet contribution
    0.15 * (1 - min(features['met_hours'] / 40, 1)) + # Activity contribution
    0.15 * features['stress_score'] +               # Stress contribution
    0.15 * features['smoking_risk'] +               # Smoking contribution
    0.15 * features['health_condition_score']       # Existing conditions
)
```

Based on:
- Framingham Risk Score components
- ACC/AHA Cardiovascular Risk Calculator
- European SCORE risk estimation

#### 3.3 Environmental Health Risk
```python
env_risk = (
    0.4 * features['environmental_risk'] +          # Environmental exposures
    0.3 * (1 - features['sun_exposure_score']) +    # Sun exposure
    0.3 * features['symptom_severity']              # Symptoms contribution
)
```

Factors considered from:
- WHO Environmental Health Risk Assessment Guidelines
- EPA Environmental Risk Assessment frameworks

### 4. Implementation Details

#### 4.1 Data Normalization
All risk scores are normalized to a 0-1 scale where:
- 0 represents minimal risk
- 1 represents maximum risk

#### 4.2 Score Thresholds
```python
if risk_scores['metabolic_health'] > 0.6:  # High risk threshold
    recommendations.append({
        'category': 'Metabolic Health',
        'recommendations': [...]
    })
```

Threshold values based on:
- Clinical risk assessment guidelines
- Population health statistics
- Expert consensus on risk stratification

#### 4.3 Recommendation Generation
Recommendations are generated using a rule-based system that considers:
- Individual risk scores
- Specific contributing factors
- Current health conditions
- Lifestyle patterns

### 5. Validation and Limitations

The current system has several limitations:
1. Simplified risk calculations compared to full clinical models
2. Self-reported data limitations
3. No longitudinal tracking
4. Limited genetic data integration

Future improvements could include:
1. Machine learning model integration
2. Real-time biometric data
3. Integration with electronic health records
4. Expanded genetic risk factors

## References

1. World Health Organization. (2020). WHO Guidelines on Physical Activity and Sedentary Behaviour.
2. Ainsworth BE, et al. (2011). Compendium of Physical Activities: A Second Update of Codes and MET Values.
3. National Sleep Foundation. (2015). Sleep Duration Recommendations.
4. American Heart Association. (2019). Cardiovascular Risk Assessment Guidelines.
5. WHO. (2016). Environmental Health Risk Assessment Guidelines.

## Technical Implementation

The system is implemented using:
- Python 3.x
- Streamlit for UI
- Pandas for data processing
- NumPy for numerical computations

Key files:
- `app.py`: Main application file
- `system_documentation.md`: This documentation
- `requirements.txt`: Dependencies

The application follows a modular design pattern with separate functions for:
1. Data collection (questionnaire sections)
2. Data processing (feature engineering)
3. Risk calculation (score computation)
4. Recommendation generation
5. Results display

This modular approach allows for:
- Easy maintenance and updates
- Independent testing of components
- Future expansion of functionality
- Integration with other systems
