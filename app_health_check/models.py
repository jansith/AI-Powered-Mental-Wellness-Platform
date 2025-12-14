from django.db import models
from app_users.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Module 1: ADHD Related Models
class ADHDQuestionnaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='adhd_questionnaires')
    
    # Attention & Focus
    difficulty_focusing = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    easily_distracted = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    forgetfulness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Hyperactivity & Impulsivity
    restlessness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    difficulty_sitting = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impulsivity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Daily Life Impact
    organization_difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    time_management = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    task_completion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Additional Info
    sleep_patterns = models.TextField(blank=True)
    study_work_patterns = models.TextField(blank=True)
    daily_habits = models.TextField(blank=True)
    
    # Results
    adhd_score = models.FloatField(null=True, blank=True)
    adhd_risk_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk')
    ], null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_score(self):
        
        total = sum([
            self.difficulty_focusing, self.easily_distracted, self.forgetfulness,
            self.restlessness, self.difficulty_sitting, self.impulsivity,
            self.organization_difficulty, self.time_management, self.task_completion
        ])
        return total / 9.0
    
    def save(self, *args, **kwargs):
        if not self.adhd_score:
            self.adhd_score = self.calculate_score()
            if self.adhd_score <= 2.0:
                self.adhd_risk_level = 'LOW'
            elif self.adhd_score <= 3.5:
                self.adhd_risk_level = 'MEDIUM'
            else:
                self.adhd_risk_level = 'HIGH'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"ADHD Questionnaire - {self.user.full_name} - {self.created_at.date()}"
    


class DepressionQuestionnaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='depression_questionnaires')
    
    # PHQ-9 Adapted Questions (1-4 scale)
    interest_pleasure = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    feeling_depressed = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    sleep_problems = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    energy_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    appetite_changes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    self_esteem = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    concentration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    psychomotor_changes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    suicidal_thoughts = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    
    # Additional Info
    physical_symptoms = models.TextField(blank=True)
    emotional_state = models.TextField(blank=True)
    life_events = models.TextField(blank=True)
    
    # Results
    depression_score = models.FloatField(null=True, blank=True)
    depression_level = models.CharField(max_length=20, choices=[
        ('MINIMAL', 'Minimal Depression'),
        ('MILD', 'Mild Depression'),
        ('MODERATE', 'Moderate Depression'),
        ('MODERATELY_SEVERE', 'Moderately Severe Depression'),
        ('SEVERE', 'Severe Depression')
    ], null=True, blank=True)
    recommendation = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_score(self):
        total = sum([
            self.interest_pleasure, self.feeling_depressed, self.sleep_problems,
            self.energy_level, self.appetite_changes, self.self_esteem,
            self.concentration, self.psychomotor_changes, self.suicidal_thoughts
        ])
        return total
    
    def get_recommendation(self):
        score = self.depression_score
        if score <= 4:
            return "Your symptoms suggest minimal depression. Consider maintaining healthy habits."
        elif score <= 9:
            return "Mild depression symptoms detected. Consider talking to a counselor or therapist."
        elif score <= 14:
            return "Moderate depression symptoms. Professional consultation with a psychologist recommended."
        elif score <= 19:
            return "Moderately severe depression. Consultation with a psychiatrist is recommended."
        else:
            return "Severe depression symptoms detected. Please seek immediate professional help."
    
    def save(self, *args, **kwargs):
        if not self.depression_score:
            self.depression_score = self.calculate_score()
            if self.depression_score <= 4:
                self.depression_level = 'MINIMAL'
            elif self.depression_score <= 9:
                self.depression_level = 'MILD'
            elif self.depression_score <= 14:
                self.depression_level = 'MODERATE'
            elif self.depression_score <= 19:
                self.depression_level = 'MODERATELY_SEVERE'
            else:
                self.depression_level = 'SEVERE'
            self.recommendation = self.get_recommendation()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Depression Questionnaire - {self.user.full_name} - {self.created_at.date()}"
