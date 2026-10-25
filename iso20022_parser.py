"""
ISO 20022 Message Parser for AML Compliance Engine
Handles parsing of simulated XML payloads (pacs.008 / pain.001) into clean transaction dictionaries.
"""

import xml.etree.ElementTree as ET

class ISO20022Parser:
    @staticmethod
    def parse_payment_xml(xml_string):
        """
        Parses basic ISO 20022 XML payloads (like pacs.008 or pain.001 structures)
        and extracts data required for AML evaluation.
        """
        try:
            root = ET.fromstring(xml_string)
            
            amount = 0.0
            currency = "USD"
            origin = "USA"
            destination = "Canada"
            
            for elem in root.iter():
                tag_name = elem.tag.split('}')[-1] # Strip namespace if present
                
                # Added IntrBkSttlmAmt for pacs.008 settlement amounts
                if tag_name in ["InstdAmt", "Amount", "IntrBkSttlmAmt"]:
                    try:
                        amount = float(elem.text)
                    except (ValueError, TypeError):
                        pass
                elif tag_name == "Ccy":
                    currency = elem.text or "USD"

            return {
                "amount_usd": amount,
                "currency": currency,
                "origin_jurisdiction": origin,
                "destination_jurisdiction": destination,
                "is_structured_deposits": False
            }
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML payload format: {e}")

