import unittest
from iso20022_parser import ISO20022Parser
from aml_engine import AMLComplianceEngine

class TestISO20022Integration(unittest.TestCase):
    def test_xml_parsing_to_aml(self):
        sample_xml = """
        <Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
            <FIToFICstmrCdtTrf>
                <CdtTrfTxInf>
                    <IntrBkSttlmAmt Ccy="USD">15000.00</IntrBkSttlmAmt>
                    <Dbtr><Pty><Nm>Acme Corp</Nm></Pty></Dbtr>
                    <Cdtr><Pty><Nm>Global Trade LLC</Nm></Pty></Cdtr>
                </CdtTrfTxInf>
            </FIToFICstmrCdtTrf>
        </Document>
        """
        parsed_tx = ISO20022Parser.parse_payment_xml(sample_xml)
        self.assertEqual(parsed_tx["amount_usd"], 15000.00)

        # Run through AML Engine
        engine = AMLComplianceEngine()
        result = engine.evaluate_transaction(parsed_tx)
        self.assertTrue(result["requires_str"])
        self.assertIn("THRESHOLD_EXCEEDED", result["flags"])

if __name__ == "__main__":
    unittest.main()

