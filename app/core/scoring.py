"""
Smart Government Scoring Engine
======================
Smart scoring model that analyzes government service priorities based on:
1. Urgency (time until service expiration)
2. Seasonality (is the service in high demand now?)
3. Category Importance (how critical is this service type?)
4. User Activity (how active is the user?)

Developer: Ghadeer (AI/ML Engineer)
"""

from datetime import datetime
from typing import Dict, List, Tuple
import math


class ServiceScorer:
    """
    Priority calculation engine
    """
    
    # Weights - based on user behavior pattern analysis
    WEIGHTS = {
        'urgency': 0.40,        # Most important - how much time left?
        'seasonality': 0.25,    # Seasonal demand
        'importance': 0.20,     # Category importance
        'activity': 0.15        # User activity level
    }
    
    def __init__(self):
        """
        Initialize the model
        """
        self.current_date = datetime.now()
        self.current_month = self.current_date.month
    
    def calculate_urgency_score(self, days_left: int) -> Tuple[float, str]:
        """
        Calculate urgency score based on days remaining
        
        Logic:
        - 0-7 days: Critical (95-100)
        - 8-14 days: Critical (85-95)
        - 15-30 days: Important (70-85)
        - 31-60 days: Medium (50-70)
        - 61-90 days: Low (30-50)
        - 90+ days: Future planning (10-30)
        
        Args:
            days_left: Days until service expiration
        
        Returns:
            (score, urgency_level_ar): Score and urgency level in Arabic
        """
        if days_left <= 0:
            return 100.0, "منتهية - إجراء فوري"  # Expired - immediate action
        elif days_left <= 7:
            score = 95 + (7 - days_left)  # 95-100
            return score, "حرج جداً"  # Very critical
        elif days_left <= 14:
            score = 85 + (14 - days_left) * 0.7
            return score, "حرج"  # Critical
        elif days_left <= 30:
            score = 70 + (30 - days_left) * 0.5
            return score, "مهم"  # Important
        elif days_left <= 60:
            score = 50 + (60 - days_left) * 0.33
            return score, "متوسط"  # Medium
        elif days_left <= 90:
            score = 30 + (90 - days_left) * 0.33
            return score, "منخفض"  # Low
        else:
            # Exponential decay after 90 days
            score = max(10, 100 * math.exp(-days_left / 200))
            return score, "تخطيط مستقبلي"  # Future planning
    
    def calculate_seasonality_score(self, 
                                   category: str, 
                                   seasonality_flag: str = None) -> Tuple[float, str]:
        """
        Calculate seasonality impact
        
        Some services are more in-demand during specific seasons:
        - Passport: Summer (May-August) - travel season
        - Vehicle: Beginning/end of year
        - Identity: Stable year-round
        
        Args:
            category: Service type
            seasonality_flag: 'in_season' or 'out_of_season' from data
        
        Returns:
            (score, explanation_ar): Score and explanation in Arabic
        """
        # If we have a pre-calculated flag
        if seasonality_flag == "in_season":
            return 90.0, "موسم ذروة الطلب"  # Peak demand season
        elif seasonality_flag == "out_of_season":
            return 50.0, "خارج موسم الذروة"  # Off-peak season
        
        # Automatic calculation based on month and category
        seasonal_patterns = {
            'travel': {
                'peak_months': [5, 6, 7, 8],  # Summer
                'peak_score': 90,
                'normal_score': 50,
                'reason': 'موسم السفر والإجازات'  # Travel and vacation season
            },
            'passport': {
                'peak_months': [5, 6, 7, 8],
                'peak_score': 90,
                'normal_score': 50,
                'reason': 'موسم السفر والإجازات'
            },
            'vehicle': {
                'peak_months': [1, 2, 11, 12],  # Year start/end
                'peak_score': 85,
                'normal_score': 60,
                'reason': 'موسم تجديد الاستمارات'  # Registration renewal season
            },
            'identity': {
                'peak_months': [],  # Stable
                'peak_score': 70,
                'normal_score': 70,
                'reason': 'طلب ثابت طوال السنة'  # Stable demand year-round
            },
            'civil': {
                'peak_months': [6, 7, 8],  # Summer - marriage season
                'peak_score': 80,
                'normal_score': 60,
                'reason': 'موسم الأحوال المدنية'  # Civil affairs season
            }
        }
        
        pattern = seasonal_patterns.get(category.lower(), {
            'peak_months': [],
            'peak_score': 60,
            'normal_score': 60,
            'reason': 'طلب عادي'  # Normal demand
        })
        
        is_peak = self.current_month in pattern['peak_months']
        score = pattern['peak_score'] if is_peak else pattern['normal_score']
        reason = pattern['reason'] if is_peak else 'خارج موسم الذروة'
        
        return score, reason
    
    def calculate_importance_score(self, category: str) -> Tuple[float, str]:
        """
        Classify service importance based on type
        
        Priority hierarchy:
        1. Identity/Civil - Essential for daily life
        2. Passport - Important for travel
        3. License - Important for mobility
        4. Vehicle - Maintenance services
        5. Other
        
        Args:
            category: Service category
        
        Returns:
            (score, reason_ar): Score and reason in Arabic
        """
        importance_map = {
            'identity': (95, 'وثيقة أساسية - لا غنى عنها'),  # Essential document
            'civil': (95, 'وثيقة أساسية - لا غنى عنها'),
            'passport': (90, 'مهمة للسفر والمعاملات الخارجية'),  # Important for travel
            'travel': (90, 'مهمة للسفر والمعاملات الخارجية'),
            'driving_license': (85, 'ضرورية للتنقل اليومي'),  # Essential for daily mobility
            'vehicle': (75, 'مطلوبة قانونياً للمركبة'),  # Legally required for vehicle
            'health': (80, 'مهمة للخدمات الصحية'),  # Important for health services
            'education': (75, 'مطلوبة للدراسة'),  # Required for education
            'business': (70, 'مهمة للأعمال'),  # Important for business
            'housing': (70, 'خدمات إسكان'),  # Housing services
            'other': (60, 'خدمات عامة')  # General services
        }
        
        return importance_map.get(category.lower(), (60, 'خدمات عامة'))
    
    def calculate_activity_score(self, 
                                 activity_level: str,
                                 usage_count: int = 0) -> Tuple[float, str]:
        """
        Analyze user activity level
        
        Active users need more reminders because they:
        1. Use services frequently
        2. Are more responsive to notifications
        
        Args:
            activity_level: User activity level (high/medium/low/inactive)
            usage_count: Number of times service was used
        
        Returns:
            (score, reason_ar): Score and reason in Arabic
        """
        # Activity level from user profile
        activity_map = {
            'high': (90, 'مستخدم نشط - يحتاج تنبيهات مبكرة'),  # Active user - needs early alerts
            'medium': (70, 'مستخدم عادي'),  # Regular user
            'low': (50, 'مستخدم قليل النشاط'),  # Low activity user
            'inactive': (30, 'مستخدم غير نشط')  # Inactive user
        }
        
        base_score, base_reason = activity_map.get(
            activity_level.lower() if activity_level else 'medium',
            (60, 'نشاط متوسط')  # Medium activity
        )
        
        # Bonus: If service used multiple times
        if usage_count >= 3:
            base_score = min(100, base_score + 10)
            base_reason += ' - خدمة متكررة'  # Recurring service
        
        return base_score, base_reason
    
    def calculate_priority(self, service: Dict, user: Dict) -> Dict:
        """
        Final priority calculation for a service
        
        Args:
            service: Service data
            user: User data
        
        Returns:
            dict: Final result with detailed breakdown
        """
        # Extract data
        days_left = service.get('days_left', 365)
        category = service.get('category', 'other')
        seasonality_flag = service.get('seasonality')
        usage_count = service.get('usage_count', 0)
        activity_level = user.get('activity_level', 'medium')
        
        # Calculate components
        urgency_score, urgency_level = self.calculate_urgency_score(days_left)
        seasonality_score, season_reason = self.calculate_seasonality_score(
            category, seasonality_flag
        )
        importance_score, importance_reason = self.calculate_importance_score(category)
        activity_score, activity_reason = self.calculate_activity_score(
            activity_level, usage_count
        )
        
        # Weighted sum
        final_score = (
            urgency_score * self.WEIGHTS['urgency'] +
            seasonality_score * self.WEIGHTS['seasonality'] +
            importance_score * self.WEIGHTS['importance'] +
            activity_score * self.WEIGHTS['activity']
        )
        
        # Generate human-readable reasons (in Arabic for demo)
        reasons = []
        
        # Urgency reasons
        if days_left <= 14:
            reasons.append(f"⚠️ باقي {days_left} يوم فقط")  # Only X days left
        elif days_left <= 30:
            reasons.append(f"📅 باقي {days_left} يوم")  # X days left
        
        # High urgency
        if urgency_score >= 85:
            reasons.append("🔴 عاجل - يحتاج إجراء فوري")  # Urgent - needs immediate action
        elif urgency_score >= 70:
            reasons.append("🟡 مهم - ينصح بالإجراء قريباً")  # Important - action advised soon
        
        # Seasonality
        if seasonality_score >= 80:
            reasons.append(f"📈 {season_reason}")
        
        # Importance
        if importance_score >= 85:
            reasons.append(f"⭐ {importance_reason}")
        
        # Activity
        if usage_count >= 3:
            reasons.append(f"🔄 استخدمت {usage_count} مرات")  # Used X times
        
        return {
            'service_id': service.get('service_id'),
            'service_name': service.get('name'),
            'final_score': round(final_score, 2),
            'priority_level': self._get_priority_level(final_score),
            'components': {
                'urgency': {
                    'score': round(urgency_score, 2),
                    'level': urgency_level,
                    'weight': self.WEIGHTS['urgency']
                },
                'seasonality': {
                    'score': round(seasonality_score, 2),
                    'reason': season_reason,
                    'weight': self.WEIGHTS['seasonality']
                },
                'importance': {
                    'score': round(importance_score, 2),
                    'reason': importance_reason,
                    'weight': self.WEIGHTS['importance']
                },
                'activity': {
                    'score': round(activity_score, 2),
                    'reason': activity_reason,
                    'weight': self.WEIGHTS['activity']
                }
            },
            'reasons': reasons,
            'days_left': days_left,
            'expiry_date': service.get('expiry_date')
        }
    
    def _get_priority_level(self, score: float) -> str:
        """
        Determine priority level
        
        Args:
            score: Final score (0-100)
        
        Returns:
            str: Priority level (critical/high/medium/low)
        """
        if score >= 80:
            return 'critical'
        elif score >= 65:
            return 'high'
        elif score >= 50:
            return 'medium'
        else:
            return 'low'


# Helper function for quick usage
def score_service(service: Dict, user: Dict) -> Dict:
    """
    Quick helper function
    
    Args:
        service: Service data dict
        user: User data dict
    
    Returns:
        dict: Scored service with priority
    """
    scorer = ServiceScorer()
    return scorer.calculate_priority(service, user)