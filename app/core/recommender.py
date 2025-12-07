"""
Smart Government Recommendation Engine
==============================
Smart recommendation engine - analyzes all user services and ranks by priority

Developer: Ghadeer (AI/ML Engineer)
"""

from typing import Dict, List, Optional
from datetime import datetime
from .scoring import ServiceScorer


class SmartRecommender:
    """
    Smart recommendation engine
    """
    
    def __init__(self):
        self.scorer = ServiceScorer()
    
    def get_recommendations(self,
                          user: Dict,
                          services: List[Dict],
                          top_n: int = 5) -> Dict:
        """
        Main function - analyze and rank all services
        
        Args:
            user: User data
            services: List of user services
            top_n: Number of recommendations to return
        
        Returns:
            dict: Recommendations with full details
        """
        if not services:
            return {
                'status': 'no_services',
                'message': 'لا توجد خدمات نشطة حالياً',  # No active services currently
                'user_id': user.get('id'),
                'user_name': user.get('name'),
                'total_services': 0,
                'recommendations': [],
                'top_recommendation': None,
                'generated_at': datetime.now().isoformat()
            }
        
        # Score all services
        scored_services = []
        for service in services:
            try:
                score_result = self.scorer.calculate_priority(service, user)
                scored_services.append(score_result)
            except Exception as e:
                print(f" Error scoring service {service.get('service_id')}: {e}")
                continue
        
        # Sort by score (descending)
        scored_services.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Get top N
        top_recommendations = scored_services[:top_n]
        
        # Identify the #1 recommendation
        top_one = top_recommendations[0] if top_recommendations else None
        
        # Generate SMS alerts for critical/high priority
        sms_alerts = self._generate_sms_alerts(top_recommendations, user)
        
        # Generate summary statistics
        summary = self._generate_summary(scored_services)
        
        return {
            'status': 'success',
            'user_id': user.get('id'),
            'user_name': user.get('name'),
            'total_services': len(services),
            'recommendations': top_recommendations,
            'top_recommendation': top_one,
            'sms_alerts': sms_alerts,
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_sms_alerts(self,
                            recommendations: List[Dict],
                            user: Dict) -> List[Dict]:
        """
        Generate ready-to-send SMS messages
        
        Send SMS only for services that are:
        - Critical (score >= 80)
        - High (score >= 65)
        
        Args:
            recommendations: List of top recommendations
            user: User data
        
        Returns:
            List[Dict]: SMS alerts ready to send
        """
        alerts = []
        
        for rec in recommendations:
            priority = rec['priority_level']
            
            if priority in ['critical', 'high']:
                # Generate action link (mock for now)
                # In production, this would come from Absher API
                action_link = f"https://absher.sa/service/{rec['service_id']}"
                
                # Build SMS message
                if priority == 'critical':
                    emoji = "🔴"
                    urgency_text = "عاجل"  # Urgent
                else:
                    emoji = "🟡"
                    urgency_text = "مهم"  # Important
                
                message = (
                    f"{emoji} {urgency_text}: {rec['service_name']}\n"
                    f"{rec['reasons'][0] if rec['reasons'] else 'يحتاج إجراء'}\n"  # Needs action
                    f"أنهِ الإجراء الآن: {action_link}"  # Complete action now
                )
                
                alerts.append({
                    'service_id': rec['service_id'],
                    'service_name': rec['service_name'],
                    'priority': priority,
                    'message': message,
                    'action_link': action_link,
                    'phone': user.get('phone', '+966500000000')
                })
        
        return alerts
    
    def _generate_summary(self, all_services: List[Dict]) -> Dict:
        """
        Generate statistical summary of services
        
        Args:
            all_services: List of all scored services
        
        Returns:
            Dict: Summary statistics
        """
        if not all_services:
            return {}
        
        # Count by priority
        priority_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for service in all_services:
            level = service.get('priority_level', 'low')
            priority_counts[level] += 1
        
        # Find urgent services (expires in 30 days)
        urgent_count = sum(1 for s in all_services if s.get('days_left', 999) <= 30)
        
        return {
            'total_services': len(all_services),
            'urgent_services': urgent_count,
            'priority_breakdown': priority_counts,
            'average_score': round(
                sum(s['final_score'] for s in all_services) / len(all_services),
                2
            )
        }
    
    def get_service_details(self, 
                           service_id: int,
                           user: Dict,
                           services: List[Dict]) -> Optional[Dict]:
        """
        Get details for a specific service
        
        Args:
            service_id: Service ID to lookup
            user: User data
            services: List of all services
        
        Returns:
            Optional[Dict]: Service details or None if not found
        """
        service = next((s for s in services if s.get('service_id') == service_id), None)
        
        if not service:
            return None
        
        return self.scorer.calculate_priority(service, user)


# Helper function for quick usage
def recommend_for_user(user: Dict, services: List[Dict]) -> Dict:
    """
    Quick helper function
    
    Args:
        user: User data dict
        services: List of service dicts
    
    Returns:
        dict: Recommendations
    """
    recommender = SmartRecommender()
    return recommender.get_recommendations(user, services)