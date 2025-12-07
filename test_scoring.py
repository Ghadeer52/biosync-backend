"""
Test the Scoring Engine
========================
Verify that the priority calculation works correctly
"""

from app.core.scoring import ServiceScorer

# Test data - Same as Reem's frontend
test_user = {
    "id": 1,
    "name": "Ghadeer Sameer",
    "activity_level": "high"
}

test_service = {
    "service_id": 101,
    "name": "Passport Renewal",
    "category": "travel",
    "expiry_date": "2026-01-25",
    "days_left": 28,
    "usage_count": 4,
    "seasonality": "in_season"
}

# Initialize scorer
scorer = ServiceScorer()

# Calculate priority
result = scorer.calculate_priority(test_service, test_user)

# Display results
print("=" * 70)
print(" Smart Government Scoring Engine Test")
print("=" * 70)

print(f"\n Service: {result['service_name']}")
print(f" Final Score: {result['final_score']}/100")
print(f" Priority Level: {result['priority_level'].upper()}")

print(f"\n Reasons (Why this score?):")
for reason in result['reasons']:
    print(f"   {reason}")

print(f"\n Component Breakdown:")
for component, data in result['components'].items():
    print(f"\n   {component.upper()}:")
    print(f"   - Score: {data['score']}/100")
    print(f"   - Weight: {data['weight'] * 100}%")
    print(f"   - Contribution: {data['score'] * data['weight']:.2f} points")
    
    if 'level' in data:
        print(f"   - Level: {data['level']}")
    if 'reason' in data:
        print(f"   - Reason: {data['reason']}")

print(f"\n Service Details:")
print(f"   - Days Left: {result['days_left']}")
print(f"   - Expiry Date: {result['expiry_date']}")

print("\n" + "=" * 70)
print(" Test completed successfully!")
print("=" * 70)