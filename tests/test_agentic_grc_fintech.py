"""
Unit tests for agentic_grc_fintech multi-framework engines.
"""

import unittest
from agentic_grc_fintech.dora_register_engine import DORARegisterEngine
from agentic_grc_fintech.iso42001_agent_governor import ISO42001AgentGovernor
from agentic_grc_fintech.sec_materiality_quantifier import SECMaterialityQuantifier
from agentic_grc_fintech.ffiec_baas_attestor import FFIECBaaSAttestor
from agentic_grc_fintech.a2zsoc_master_grc_bridge import A2ZSOCMasterGRCBridge


class TestAgenticGRCFinTech(unittest.TestCase):

    def setUp(self):
        self.dora = DORARegisterEngine("Apex Test Corp", "LEI_998877665544332211")
        self.ai_gov = ISO42001AgentGovernor()
        self.sec = SECMaterialityQuantifier(1_000_000.0)
        self.ffiec = FFIECBaaSAttestor()
        self.bridge = A2ZSOCMasterGRCBridge()

    def test_dora_concentration_and_register(self):
        self.dora.register_provider(
            provider_name="AWS Cloud",
            service_type="Compute",
            criticality="CRITICAL_FUNCTION",
            country_code="DE",
            sub_processors=["Sub1"],
            has_exit_strategy=True,
            rto_minutes=15
        )
        ok, defs = self.dora.evaluate_concentration_risk()
        self.assertTrue(ok)
        self.assertEqual(len(defs), 0)

        reg = self.dora.synthesize_annex_i_register()
        self.assertEqual(reg.total_providers, 1)
        self.assertEqual(reg.critical_providers, 1)
        self.assertTrue(len(reg.register_xml_hash) > 10)

    def test_dora_deficiency_detection(self):
        self.dora.register_provider(
            provider_name="Fragile SaaS",
            service_type="OCR",
            criticality="CRITICAL_FUNCTION",
            country_code="US",
            sub_processors=["Sub1", "Sub2", "Sub3", "Sub4", "Sub5"],  # Depth > 4
            has_exit_strategy=False,  # Missing exit strategy
            rto_minutes=120  # Exceeds 60m
        )
        ok, defs = self.dora.evaluate_concentration_risk()
        self.assertFalse(ok)
        self.assertEqual(len(defs), 3)

    def test_iso42001_agent_governance(self):
        ev = self.ai_gov.evaluate_agent_action(
            agent_id="test_agent",
            model_name="Claude Opus 5.5",
            task_scope="Payment Underwriting",
            prompt_injection_tested=True,
            bias_metric_parity=0.92,
            mandate_hash="mandate_sig_1234567890abcdef"
        )
        self.assertTrue(ev.is_compliant)
        self.assertIsNone(ev.rejection_reason)

        # Test failure case (unauthorized model & low bias parity)
        bad_ev = self.ai_gov.evaluate_agent_action(
            agent_id="bad_agent",
            model_name="Legacy-LLM-v1",
            task_scope="Payment Underwriting",
            prompt_injection_tested=False,
            bias_metric_parity=0.60,
            mandate_hash=""
        )
        self.assertFalse(bad_ev.is_compliant)
        self.assertIn("not in approved ISO 42001", bad_ev.rejection_reason)
        self.assertIn("violates 80%", bad_ev.rejection_reason)

    def test_sec_materiality_quantifier(self):
        # Non-material incident
        m1 = self.sec.assess_incident("inc_01", "dev_db", 100, 1.0, 0.0, 5.0)
        self.assertFalse(m1.is_material)
        self.assertIn("NON_MATERIAL", m1.form_8k_item_1_05_draft)

        # Material incident
        m2 = self.sec.assess_incident("inc_02", "prod_db", 15_000, 10.0, 250_000.0, 12.0)
        self.assertTrue(m2.is_material)
        self.assertTrue(m2.total_dollar_exposure_usd > 1_000_000.0)
        self.assertIn("Item 1.05: Material Cybersecurity Incidents", m2.form_8k_item_1_05_draft)
        self.assertEqual(m2.filing_deadline_hours_remaining, 84.0)

    def test_ffiec_baas_attestor(self):
        att = self.ffiec.attest_baas_program(
            sponsor_bank_name="Test Sponsor Bank",
            fintech_partner_name="Test FinTech",
            omnibus_fbo_parity_delta_usd=0.00,
            cat_maturity_level="Intermediate",
            fdic_part_370_qualified=True,
            suspense_balance_usd=50.0
        )
        self.assertTrue(att.is_certified)

        # Drift breach
        bad_att = self.ffiec.attest_baas_program(
            sponsor_bank_name="Test Sponsor Bank",
            fintech_partner_name="Test FinTech",
            omnibus_fbo_parity_delta_usd=25000.00,
            cat_maturity_level="Baseline",
            fdic_part_370_qualified=False,
            suspense_balance_usd=8000.0
        )
        self.assertFalse(bad_att.is_certified)

    def test_a2zsoc_master_receipt_sealing(self):
        reg = self.dora.synthesize_annex_i_register()
        ai_ev = self.ai_gov.evaluate_agent_action("a", "Claude Opus 5.5", "t", True, 0.9, "1234567890abcdef")
        sec_m = self.sec.assess_incident("i", "a", 10, 0.1, 0.0, 1.0)
        ffiec_a = self.ffiec.attest_baas_program("b", "f", 0.0, "Advanced", True, 0.0)

        receipt = self.bridge.seal_master_grc_receipt(
            tenant_id="tenant_01",
            dora_reg=reg,
            dora_compliant=True,
            ai_event=ai_ev,
            sec_assessment=sec_m,
            ffiec_attestation=ffiec_a
        )
        self.assertEqual(receipt.total_controls_evaluated, 867)
        self.assertEqual(receipt.compliance_score, 1.0)
        self.assertTrue(receipt.a2zsoc_merkle_seal.startswith("a2z_grc_seal_"))


if __name__ == "__main__":
    unittest.main()
