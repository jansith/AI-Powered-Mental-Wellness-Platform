from django.db import models
from app_users.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Module 1: ADHD Related Models
class ADHDQuestionnaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='adhd_questionnaires')
    
    # Core ADHD Symptoms (0-3 scale)
    difficulty_sustaining_attention = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → No attention issues, 1 → Mild difficulty, 2 → Moderate difficulty, 3 → Severe difficulty focusing"
    )
    easily_distracted = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → Not distracted, 1 → Mild distraction, 2 → Gets distracted often, 3 → Very easily distracted"
    )
    forgetful_daily_tasks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → Never forgets, 1 → Sometimes forgets, 2 → Often forgets, 3 → Forgets very often"
    )
    poor_organization = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → Very organized, 1 → Slightly disorganized, 2 → Moderately poor organization, 3 → Very poor organization"
    )
    restlessness = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → Calm, 1 → Mild restlessness, 2 → Often restless, 3 → Very restless"
    )
    impulsivity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="0 → Not impulsive, 1 → Slightly impulsive, 2 → Often impulsive, 3 → Very impulsive"
    )
    
    # Behavioral Metrics
    screen_time_daily = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        help_text="Daily screen time in hours (1.0-10.0)"
    )
    phone_unlocks_per_day = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(200)],
        help_text="Number of phone unlocks per day (20-200)"
    )
    working_memory_score = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(80)],
        help_text="Memory ability score (20-80)"
    )
    
    # Results
    adhd_score = models.FloatField(null=True, blank=True)
    adhd_label = models.IntegerField(
        null=True, blank=True,
        choices=[
            (0, 'No ADHD'),
            (1, 'ADHD')
        ],
        help_text="0 = No ADHD, 1 = ADHD"
    )
    adhd_risk_level = models.CharField(
        max_length=20, 
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk')
        ], 
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_adhd_score(self):
        """Calculate weighted ADHD score based on symptoms and behavioral metrics"""
        # Symptom score (0-18 scale, normalized to 0-3)
        symptom_total = sum([
            self.difficulty_sustaining_attention,
            self.easily_distracted,
            self.forgetful_daily_tasks,
            self.poor_organization,
            self.restlessness,
            self.impulsivity_score
        ])
        symptom_score = symptom_total / 6.0  # Normalize to 0-3 scale
        
        # Behavioral metrics contribution
        # Screen time contribution (normalized to 0-1)
        screen_time_contribution = (self.screen_time_daily - 1.0) / 9.0
        
        # Phone unlocks contribution (normalized to 0-1)
        phone_unlocks_contribution = (self.phone_unlocks_per_day - 20) / 180.0
        
        # Working memory contribution (inverse, normalized to 0-1)
        # Lower memory score = higher ADHD risk
        memory_contribution = 1.0 - ((self.working_memory_score - 20) / 60.0)
        
        # Weighted final score (0-3 scale)
        # Symptoms weight: 60%, Behavioral metrics: 40%
        behavioral_avg = (screen_time_contribution + phone_unlocks_contribution + memory_contribution) / 3.0
        behavioral_score = behavioral_avg * 3.0  # Scale to 0-3
        
        final_score = (symptom_score * 0.6) + (behavioral_score * 0.4)
        
        return round(final_score, 2)
    
    def determine_adhd_label(self, score):
        """Determine ADHD label based on calculated score"""
        # Threshold can be adjusted based on clinical validation
        # Using 1.5 as threshold (midpoint of 0-3 scale)
        return 1 if score >= 1.5 else 0
    
    def determine_risk_level(self, score):
        """Determine risk level based on calculated score"""
        if score < 1.0:
            return 'LOW'
        elif score < 2.0:
            return 'MEDIUM'
        else:
            return 'HIGH'
    
    def save(self, *args, **kwargs):
        if not self.adhd_score:
            self.adhd_score = self.calculate_adhd_score()
            self.adhd_label = self.determine_adhd_label(self.adhd_score)
            self.adhd_risk_level = self.determine_risk_level(self.adhd_score)
        super().save(*args, **kwargs)
    
    def get_symptom_summary(self):
        """Return a summary of symptom scores"""
        return {
            'difficulty_sustaining_attention': self.difficulty_sustaining_attention,
            'easily_distracted': self.easily_distracted,
            'forgetful_daily_tasks': self.forgetful_daily_tasks,
            'poor_organization': self.poor_organization,
            'restlessness': self.restlessness,
            'impulsivity_score': self.impulsivity_score,
            'symptom_total': sum([
                self.difficulty_sustaining_attention,
                self.easily_distracted,
                self.forgetful_daily_tasks,
                self.poor_organization,
                self.restlessness,
                self.impulsivity_score
            ])
        }
    
    def get_behavioral_metrics_summary(self):
        """Return a summary of behavioral metrics"""
        return {
            'screen_time_daily': self.screen_time_daily,
            'phone_unlocks_per_day': self.phone_unlocks_per_day,
            'working_memory_score': self.working_memory_score,
            'screen_time_category': self.get_screen_time_category(),
            'phone_usage_category': self.get_phone_usage_category(),
            'memory_category': self.get_memory_category()
        }
    
    def get_screen_time_category(self):
        """Categorize screen time"""
        if self.screen_time_daily <= 3:
            return "Low"
        elif self.screen_time_daily <= 6:
            return "Medium"
        else:
            return "High"
    
    def get_phone_usage_category(self):
        """Categorize phone usage"""
        if self.phone_unlocks_per_day <= 60:
            return "Low usage"
        elif self.phone_unlocks_per_day <= 120:
            return "Medium usage"
        else:
            return "Very high / restless usage"
    
    def get_memory_category(self):
        """Categorize working memory"""
        if self.working_memory_score <= 40:
            return "Weak memory"
        elif self.working_memory_score <= 60:
            return "Average memory"
        else:
            return "Strong memory"
    
    def __str__(self):
        adhd_status = "ADHD" if self.adhd_label == 1 else "No ADHD"
        return f"ADHD Assessment - {self.user.full_name} - {adhd_status} - Score: {self.adhd_score} - {self.created_at.date()}"
    


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
