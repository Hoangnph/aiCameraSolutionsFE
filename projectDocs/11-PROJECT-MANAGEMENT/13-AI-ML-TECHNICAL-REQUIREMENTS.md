# AI/ML Technical Requirements
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này định nghĩa các yêu cầu kỹ thuật chi tiết cho AI/ML development của hệ thống AI Camera Counting, bao gồm model versioning, performance monitoring, fallback mechanisms, training pipeline, data quality validation, và model explainability.

### 🎯 Mục tiêu kỹ thuật

#### Mục tiêu chính
- Xây dựng scalable và maintainable AI/ML architecture
- Đảm bảo model performance tối ưu với high accuracy
- Cung cấp robust fallback mechanisms
- Tuân thủ ML best practices
- Tối ưu hóa model inference performance

#### Mục tiêu kỹ thuật
- Model inference time <100ms
- Model accuracy >95%
- Model availability 99.9%
- Comprehensive model monitoring
- Automated retraining pipeline

### 🏗️ Architecture Patterns

#### 1. Model Versioning Strategy

##### MLflow Implementation

```python
# Model Versioning with MLflow
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
import os

class ModelVersionManager:
    def __init__(self, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
    
    def register_model(self, model, model_name: str, version: str):
        """Register model with versioning"""
        with mlflow.start_run():
            mlflow.pytorch.log_model(model, model_name)
            mlflow.set_tag("version", version)
            mlflow.set_tag("model_type", "people_counter")
    
    def load_model(self, model_name: str, version: str = "latest"):
        """Load specific model version"""
        model_uri = f"models:/{model_name}/{version}"
        return mlflow.pytorch.load_model(model_uri)
    
    def list_models(self):
        """List all registered models"""
        return self.client.list_registered_models()
```

#### 2. Model Performance Monitoring

##### Performance Tracking Implementation

```python
# Model Performance Monitoring
import time
import numpy as np
from datetime import datetime
import logging

class ModelPerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "inference_time": [],
            "accuracy": [],
            "confidence": [],
            "throughput": []
        }
        self.logger = logging.getLogger(__name__)
    
    def track_inference(self, start_time: float, end_time: float, 
                       prediction: int, ground_truth: int = None):
        """Track model inference performance"""
        inference_time = end_time - start_time
        self.metrics["inference_time"].append(inference_time)
        
        if ground_truth is not None:
            accuracy = 1 if prediction == ground_truth else 0
            self.metrics["accuracy"].append(accuracy)
        
        self.logger.info(f"Inference time: {inference_time:.3f}s")
    
    def get_performance_summary(self):
        """Get performance summary"""
        return {
            "avg_inference_time": np.mean(self.metrics["inference_time"]),
            "avg_accuracy": np.mean(self.metrics["accuracy"]) if self.metrics["accuracy"] else 0,
            "total_inferences": len(self.metrics["inference_time"])
        }
```

#### 3. Fallback Mechanisms

##### Rule-based Fallback Implementation

```python
# Fallback Mechanisms
class FallbackSystem:
    def __init__(self):
        self.primary_model = None
        self.backup_model = None
        self.rule_based_fallback = RuleBasedCounter()
    
    def predict_with_fallback(self, image):
        """Predict with fallback mechanisms"""
        try:
            # Try primary model
            if self.primary_model:
                result = self.primary_model.predict(image)
                if result.confidence > 0.8:
                    return result
            
            # Try backup model
            if self.backup_model:
                result = self.backup_model.predict(image)
                if result.confidence > 0.7:
                    return result
            
            # Use rule-based fallback
            return self.rule_based_fallback.count(image)
            
        except Exception as e:
            logging.error(f"All models failed: {e}")
            return self.rule_based_fallback.count(image)

class RuleBasedCounter:
    def count(self, image):
        """Simple rule-based counting"""
        # Basic blob detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size
        valid_contours = [c for c in contours if cv2.contourArea(c) > 100]
        return CountResult(len(valid_contours), 0.5)  # Lower confidence
```

#### 4. Automated Training Pipeline

##### CI/CD for ML Implementation

```python
# Automated Training Pipeline
import subprocess
import yaml
from pathlib import Path

class MLTrainingPipeline:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def trigger_training(self, trigger_type: str = "scheduled"):
        """Trigger model training"""
        if trigger_type == "scheduled":
            self._run_scheduled_training()
        elif trigger_type == "data_drift":
            self._run_drift_training()
        elif trigger_type == "performance_degradation":
            self._run_performance_training()
    
    def _run_scheduled_training(self):
        """Run scheduled training"""
        script_path = Path(__file__).parent / "train_model.py"
        subprocess.run([
            "python", str(script_path),
            "--config", self.config["training_config"],
            "--data_path", self.config["data_path"],
            "--output_path", self.config["output_path"]
        ])
    
    def evaluate_model(self, model_path: str):
        """Evaluate trained model"""
        # Run evaluation script
        eval_script = Path(__file__).parent / "evaluate_model.py"
        result = subprocess.run([
            "python", str(eval_script),
            "--model_path", model_path,
            "--test_data", self.config["test_data_path"]
        ], capture_output=True, text=True)
        
        return self._parse_evaluation_results(result.stdout)
```

#### 5. Data Quality Validation

##### Data Quality Monitoring

```python
# Data Quality Validation
import pandas as pd
from typing import Dict, List
import numpy as np

class DataQualityValidator:
    def __init__(self):
        self.quality_metrics = {}
    
    def validate_image_quality(self, image):
        """Validate image quality"""
        metrics = {
            "brightness": self._check_brightness(image),
            "contrast": self._check_contrast(image),
            "blur": self._check_blur(image),
            "noise": self._check_noise(image)
        }
        
        # Calculate overall quality score
        quality_score = np.mean(list(metrics.values()))
        return quality_score > 0.7, metrics
    
    def _check_brightness(self, image):
        """Check image brightness"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        return 1.0 if 50 <= mean_brightness <= 200 else 0.0
    
    def _check_contrast(self, image):
        """Check image contrast"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        std_dev = np.std(gray)
        return min(1.0, std_dev / 50.0)
    
    def _check_blur(self, image):
        """Check image blur using Laplacian variance"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return min(1.0, laplacian_var / 100.0)
    
    def _check_noise(self, image):
        """Check image noise"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Simple noise estimation
        noise_level = np.std(gray)
        return max(0.0, 1.0 - noise_level / 50.0)
```

#### 6. Model Explainability

##### SHAP Integration

```python
# Model Explainability with SHAP
import shap
import matplotlib.pyplot as plt

class ModelExplainer:
    def __init__(self, model):
        self.model = model
        self.explainer = None
    
    def create_explainer(self, background_data):
        """Create SHAP explainer"""
        self.explainer = shap.DeepExplainer(self.model, background_data)
    
    def explain_prediction(self, image):
        """Explain model prediction"""
        if self.explainer is None:
            raise ValueError("Explainer not initialized")
        
        shap_values = self.explainer.shap_values(image)
        
        # Create explanation visualization
        plt.figure(figsize=(10, 6))
        shap.image_plot(shap_values, image)
        plt.title("Model Prediction Explanation")
        plt.show()
        
        return {
            "shap_values": shap_values,
            "prediction": self.model.predict(image),
            "feature_importance": np.abs(shap_values).mean(axis=0)
        }
    
    def generate_explanation_report(self, image, prediction):
        """Generate explanation report"""
        explanation = self.explain_prediction(image)
        
        report = {
            "prediction": prediction,
            "confidence": explanation["prediction"].confidence,
            "key_features": self._identify_key_features(explanation["feature_importance"]),
            "explanation_visualization": "explanation_plot.png"
        }
        
        return report
```

#### 7. A/B Testing Framework

##### Model Comparison Implementation

```python
# A/B Testing Framework
import random
from typing import Dict, Any

class ABTestingFramework:
    def __init__(self):
        self.models = {}
        self.traffic_splits = {}
        self.results = {}
    
    def add_model(self, model_id: str, model, traffic_percentage: float):
        """Add model to A/B test"""
        self.models[model_id] = model
        self.traffic_splits[model_id] = traffic_percentage
        self.results[model_id] = {
            "predictions": [],
            "accuracies": [],
            "inference_times": []
        }
    
    def route_request(self, image):
        """Route request to model based on traffic split"""
        rand = random.random()
        cumulative = 0
        
        for model_id, percentage in self.traffic_splits.items():
            cumulative += percentage
            if rand <= cumulative:
                return self._predict_with_model(model_id, image)
        
        # Fallback to first model
        return self._predict_with_model(list(self.models.keys())[0], image)
    
    def _predict_with_model(self, model_id: str, image):
        """Predict with specific model and track results"""
        start_time = time.time()
        prediction = self.models[model_id].predict(image)
        inference_time = time.time() - start_time
        
        # Track results
        self.results[model_id]["predictions"].append(prediction)
        self.results[model_id]["inference_times"].append(inference_time)
        
        return prediction
    
    def get_comparison_results(self):
        """Get A/B testing comparison results"""
        comparison = {}
        
        for model_id, results in self.results.items():
            comparison[model_id] = {
                "avg_inference_time": np.mean(results["inference_times"]),
                "total_predictions": len(results["predictions"]),
                "avg_confidence": np.mean([p.confidence for p in results["predictions"]])
            }
        
        return comparison
```

#### 8. Model Security

##### Adversarial Attack Prevention

```python
# Model Security Implementation
import cv2
import numpy as np
from typing import Tuple

class ModelSecurity:
    def __init__(self):
        self.attack_detectors = {
            "noise_detection": self._detect_noise_attack,
            "perturbation_detection": self._detect_perturbation,
            "adversarial_detection": self._detect_adversarial
        }
    
    def validate_input(self, image):
        """Validate input for security threats"""
        security_report = {
            "is_safe": True,
            "threats_detected": [],
            "confidence": 1.0
        }
        
        for detector_name, detector_func in self.attack_detectors.items():
            is_threat, confidence = detector_func(image)
            if is_threat:
                security_report["is_safe"] = False
                security_report["threats_detected"].append(detector_name)
                security_report["confidence"] *= confidence
        
        return security_report
    
    def _detect_noise_attack(self, image):
        """Detect noise-based attacks"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        noise_level = np.std(gray)
        
        # High noise levels might indicate adversarial noise
        is_threat = noise_level > 30
        confidence = min(1.0, noise_level / 50.0)
        
        return is_threat, confidence
    
    def _detect_perturbation(self, image):
        """Detect image perturbations"""
        # Check for unusual pixel value distributions
        pixel_std = np.std(image)
        is_threat = pixel_std > 100
        confidence = min(1.0, pixel_std / 150.0)
        
        return is_threat, confidence
    
    def _detect_adversarial(self, image):
        """Detect adversarial examples"""
        # Simple adversarial detection based on image statistics
        # In practice, use more sophisticated methods
        return False, 1.0
```

### 📋 Implementation Checklist

#### Phase 1: Foundation Setup (Week 1)
- [ ] Setup MLflow for model versioning
- [ ] Implement basic model inference pipeline
- [ ] Setup performance monitoring
- [ ] Configure fallback mechanisms
- [ ] Setup data quality validation

#### Phase 2: Model Development (Week 2)
- [ ] Implement model training pipeline
- [ ] Add model explainability features
- [ ] Setup A/B testing framework
- [ ] Implement security measures
- [ ] Configure automated retraining

#### Phase 3: Performance Optimization (Week 3)
- [ ] Optimize model inference speed
- [ ] Implement advanced fallback mechanisms
- [ ] Enhance monitoring capabilities
- [ ] Setup model performance alerts
- [ ] Implement data drift detection

#### Phase 4: Production Readiness (Week 4)
- [ ] Setup production model deployment
- [ ] Implement comprehensive testing
- [ ] Configure security monitoring
- [ ] Setup model performance dashboards
- [ ] Implement automated model updates

### 🎯 Success Metrics

#### Performance Metrics
- **Model Inference Time**: <100ms average
- **Model Accuracy**: >95%
- **Model Availability**: 99.9%
- **Data Quality Score**: >90%
- **Security Threat Detection**: 100%

#### Quality Metrics
- **Model Explainability**: Complete
- **A/B Testing Coverage**: 100%
- **Fallback Success Rate**: >99%
- **Training Pipeline Reliability**: 100%

### 🚨 Risk Mitigation

#### Model Performance Risks
- **Risk**: Model accuracy degradation
- **Mitigation**: Continuous monitoring, automated retraining

#### Security Risks
- **Risk**: Adversarial attacks
- **Mitigation**: Input validation, security monitoring

#### Data Quality Risks
- **Risk**: Poor quality input data
- **Mitigation**: Data validation, quality monitoring

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Next Review**: [Date + 2 weeks]  
**Status**: Ready for Implementation
