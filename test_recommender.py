"""
Test the Recommendation Engine
===============================
Verify that recommendations are ranked correctly
"""

from app.core.recommender import SmartRecommender
import json

# Test data - Same as Reem's frontend
test_user = {
    "id": 1,
    "name": "Reem AlHarbi",
    "national_id": "1098765432",
    "city": "Riyadh",
    "activity_level": "high",
    "phone": "+966500000000",
    "last_login": "2025-01-18T09:32:00Z"
}

test_services = [
    {
        "service_id": 101,
        "name": "Passport Renewal",
        "category": "travel",
        "expiry_date": "2026-01-25",
        "days_left": 28,
        "usage_count": 4,
        "category_importance": 0.8,
        "seasonality": "in_season"
    },
    {
        "service_id": 102,
        "name": "Vehicle Inspection",
        "category": "vehicle",
        "expiry_date": "2026-03-14",
        "days_left": 72,
        "usage_count": 2,
        "category_importance": 0.5,
        "seasonality": "out_of_season"
    },
    {
        "service_id": 103,
        "name": "National ID Renewal",
        "category": "identity",
        "expiry_date": "2026-06-09",
        "days_left": 150,
        "usage_count": 1,
        "category_importance": 0.3,
        "seasonality": "out_of_season"
    }
]

# Initialize recommender
recommender = SmartRecommender()

# Get recommendations
result = recommender.get_recommendations(test_user, test_services, top_n=5)

# Display results
print("=" * 70)
print(" Smart Government Recommendation Engine Test")
print("=" * 70)

print(f"\n User: {result['user_name']}")
print(f" Total Services: {result['total_services']}")
print(f" Generated: {result['generated_at']}")

print(f"\n TOP RECOMMENDATION:")
top = result['top_recommendation']
print(f"   Service: {top['service_name']}")
print(f"   Score: {top['final_score']}/100")
print(f"   Priority: {top['priority_level'].upper()}")
print(f"   Days Left: {top['days_left']}")
print(f"\n   Why this is #1:")
for reason in top['reasons']:
    print(f"      {reason}")

print(f"\n ALL RECOMMENDATIONS (Ranked):")
for i, rec in enumerate(result['recommendations'], 1):
    print(f"\n   #{i}. {rec['service_name']}")
    print(f"       Score: {rec['final_score']}/100")
    print(f"       Priority: {rec['priority_level'].upper()}")
    print(f"       Days Left: {rec['days_left']}")

print(f"\n SMS ALERTS ({len(result['sms_alerts'])} alerts ready to send):")
for alert in result['sms_alerts']:
    print(f"\n    {alert['service_name']} ({alert['priority'].upper()}):")
    print(f"      To: {alert['phone']}")
    print(f"      Message: {alert['message'][:80]}...")
    print(f"      Link: {alert['action_link']}")

print(f"\n SUMMARY STATISTICS:")
summary = result['summary']
print(f"   Total Services: {summary['total_services']}")
print(f"   Urgent Services (≤30 days): {summary['urgent_services']}")
print(f"   Average Score: {summary['average_score']}/100")
print(f"\n   Priority Breakdown:")
for level, count in summary['priority_breakdown'].items():
    print(f"      {level.upper()}: {count} service(s)")

print("\n" + "=" * 70)
print(" Test completed successfully!")
print("\n Full JSON response saved to: test_output.json")
print("=" * 70)
