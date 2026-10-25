"""
AML Compliance Engine - Core Module
"""

class AMLComplianceEngine:
    def __init__(self):
        self.rules = {
            "str_threshold_usd": 10000,
            "high_risk_jurisdictions": ["JurisdictionA", "JurisdictionB", "HighRiskLand"],
            "ubo_threshold_percentage": 25.0
        }

    def evaluate_transaction(self, transaction_data):
        amount = transaction_data.get("amount_usd", 0)
        origin = transaction_data.get("origin_jurisdiction", "")
        destination = transaction_data.get("destination_jurisdiction", "")
        is_structured = transaction_data.get("is_structured_deposits", False)

        flags = []
        requires_str = False

        if amount >= self.rules["str_threshold_usd"]:
            flags.append("THRESHOLD_EXCEEDED")
            requires_str = True

        if origin in self.rules["high_risk_jurisdictions"] or destination in self.rules["high_risk_jurisdictions"]:
            flags.append("HIGH_RISK_JURISDICTION_MATCH")
            requires_str = True

        if is_structured:
            flags.append("SUSPICIOUS_STRUCTURING_DETECTED")
            requires_str = True

        return {
            "status": "FLAGGED" if requires_str else "APPROVED",
            "flags": flags,
            "requires_str": requires_str,
            "audit_trail_note": f"Evaluated under digital compliance standards. Flags found: {len(flags)}."
        }

    def evaluate_ubo(self, ownership_structure):
        identified_ubos = []
        for entity in ownership_structure:
            shareholding = entity.get("ownership_percentage", 0.0)
            if shareholding >= self.rules["ubo_threshold_percentage"]:
                identified_ubos.append({
                    "name": entity.get("name"),
                    "ownership_percentage": shareholding,
                    "status": "VERIFIED_UBO"
                })
        
        return {
            "compliant_screening": len(identified_ubos) > 0,
            "identified_ubos": identified_ubos,
            "audit_trail_note": f"UBO threshold set at {self.rules['ubo_threshold_percentage']}%. Found {len(identified_ubos)} qualifying entities."
        }
print('AML Engine Initialized')
