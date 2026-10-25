"""
Comprehensive Unit Test Suite for AML Compliance Engine
"""

import unittest
from aml_engine import AMLComplianceEngine

class TestAMLComplianceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AMLComplianceEngine()

    def test_normal_transaction(self):
        tx = {
            "amount_usd": 1500,
            "origin_jurisdiction": "USA",
            "destination_jurisdiction": "Canada",
            "is_structured_deposits": False
        }
        result = self.engine.evaluate_transaction(tx)
        self.assertEqual(result["status"], "APPROVED")
        self.assertFalse(result["requires_str"])
        self.assertEqual(len(result["flags"]), 0)

    def test_threshold_exceeded(self):
        tx = {
            "amount_usd": 12500,
            "origin_jurisdiction": "USA",
            "destination_jurisdiction": "Canada",
            "is_structured_deposits": False
        }
        result = self.engine.evaluate_transaction(tx)
        self.assertEqual(result["status"], "FLAGGED")
        self.assertTrue(result["requires_str"])
        self.assertIn("THRESHOLD_EXCEEDED", result["flags"])

    def test_high_risk_jurisdiction(self):
        tx = {
            "amount_usd": 500,
            "origin_jurisdiction": "HighRiskLand",
            "destination_jurisdiction": "Canada",
            "is_structured_deposits": False
        }
        result = self.engine.evaluate_transaction(tx)
        self.assertEqual(result["status"], "FLAGGED")
        self.assertTrue(result["requires_str"])
        self.assertIn("HIGH_RISK_JURISDICTION_MATCH", result["flags"])

    def test_suspicious_structuring(self):
        tx = {
            "amount_usd": 3000,
            "origin_jurisdiction": "USA",
            "destination_jurisdiction": "Canada",
            "is_structured_deposits": True
        }
        result = self.engine.evaluate_transaction(tx)
        self.assertEqual(result["status"], "FLAGGED")
        self.assertTrue(result["requires_str"])
        self.assertIn("SUSPICIOUS_STRUCTURING_DETECTED", result["flags"])

    def test_ubo_screening(self):
        ownership = [
            {"name": "Alice Smith", "ownership_percentage": 30.0},
            {"name": "Bob Jones", "ownership_percentage": 10.0}
        ]
        result = self.engine.evaluate_ubo(ownership)
        self.assertTrue(result["compliant_screening"])
        self.assertEqual(len(result["identified_ubos"]), 1)
        self.assertEqual(result["identified_ubos"][0]["name"], "Alice Smith")

if __name__ == "__main__":
    unittest.main()

