"""
Command Line Interface & Multi-Framework Audit Sprint for agentic-grc-fintech.
Simulates autonomous multi-framework compliance evaluation across DORA, ISO 42001, SEC 96h, and FFIEC.
"""

import argparse
import sys
import time
from .dora_register_engine import DORARegisterEngine
from .iso42001_agent_governor import ISO42001AgentGovernor
from .sec_materiality_quantifier import SECMaterialityQuantifier
from .ffiec_baas_attestor import FFIECBaaSAttestor
from .a2zsoc_master_grc_bridge import A2ZSOCMasterGRCBridge


def run_demo() -> None:
    print("\n" + "=" * 80)
    print("🛡️  AGENTIC-GRC-FINTECH v1.0.0 (Frontier September 2026)")
    print("    Autonomous Multi-Cloud GRC & Regulatory Exam OS for FinTech (Beyond PCI DSS)")
    print("    Integrated with a2zsoc.com Evidence Vault & 867-Control Unified Lattice")
    print("=" * 80)

    # 1. EU DORA ICT Concentration & Register Evaluation
    print("\n[1/5] EU DORA (Reg 2022/2554) ICT Third-Party Concentration Audit...")
    dora_engine = DORARegisterEngine(
        reporting_entity="Apex Sovereign Financial Technologies Corp",
        lei_code="5493001KJTIIGC8Y1R12"
    )

    dora_engine.register_provider(
        provider_name="AWS Cloud Infrastructure (eu-central-1)",
        service_type="Cloud Compute & KMS Enclaves",
        criticality="CRITICAL_FUNCTION",
        country_code="DE",
        sub_processors=["Equinix Frankfurt", "Datadog EU"],
        has_exit_strategy=True,
        rto_minutes=15
    )
    dora_engine.register_provider(
        provider_name="Stripe Technology Europe",
        service_type="Card Acquiring & Tokenization Gateway",
        criticality="CRITICAL_FUNCTION",
        country_code="IE",
        sub_processors=["VisaNet", "Mastercard Banknet"],
        has_exit_strategy=True,
        rto_minutes=25
    )

    dora_ok, dora_deficiencies = dora_engine.evaluate_concentration_risk()
    dora_reg = dora_engine.synthesize_annex_i_register()
    print(f"   • Registered ICT Providers: {dora_reg.total_providers} (Critical: {dora_reg.critical_providers})")
    print(f"   • DORA Concentration Risk:  {'PASSED (0 Deficiencies)' if dora_ok else 'FAILED'}")
    print(f"   • Annex I Register Hash:    {dora_reg.register_xml_hash[:24]}...")

    # 2. ISO/IEC 42001 & EU AI Act Autonomous Agent Governance
    print("\n[2/5] ISO/IEC 42001 & EU AI Act Autonomous Agent Governance...")
    ai_gov = ISO42001AgentGovernor()
    ai_event = ai_gov.evaluate_agent_action(
        agent_id="agent_credit_underwriter_04",
        model_name="Claude Opus 5.5",
        task_scope="Autonomous Commercial Underwriting & Multi-Rail Disbursement",
        prompt_injection_tested=True,
        bias_metric_parity=0.88,  # > 0.80 four-fifths rule
        mandate_hash="mandate_sig_a10f82c918efbc92"
    )
    print(f"   • Evaluated Agent Model:    {ai_event.model_name}")
    print(f"   • Prompt Injection Defense: {'VERIFIED (OWASP LLM01 Resilient)' if ai_event.prompt_injection_tested else 'FAILED'}")
    print(f"   • Lending Fairness Parity:  {ai_event.bias_metric_parity * 100:.1f}% (Threshold: 80.0%)")
    print(f"   • Non-Repudiation Mandate:  {ai_event.mandate_hash}")
    print(f"   • AI Governance Status:     {'PASSED (ISO 42001 Approved)' if ai_event.is_compliant else 'REJECTED'}")

    # 3. SEC Form 8-K Item 1.05 & Regulation S-P Materiality Assessment
    print("\n[3/5] SEC Form 8-K Item 1.05 & Reg S-P 96-Hour Materiality Clock...")
    sec_quantifier = SECMaterialityQuantifier(corporate_materiality_threshold_usd=1_000_000.0)
    sec_assessment = sec_quantifier.assess_incident(
        incident_id="inc_api_key_leak_0821",
        asset_compromised="Non-Production Analytics Read Replica",
        records_impacted=250,
        outage_duration_hours=0.5,
        direct_funds_diverted_usd=0.0,
        hours_since_detection=2.5
    )
    print(f"   • Evaluated Incident:       {sec_assessment.incident_id}")
    print(f"   • Calculated Exposure:      ${sec_assessment.total_dollar_exposure_usd:,.2f} USD")
    print(f"   • Materiality Ceiling:      ${sec_assessment.materiality_threshold_usd:,.2f} USD")
    print(f"   • Materiality Finding:      {'NON-MATERIAL (Below $1.0M Threshold)' if not sec_assessment.is_material else 'CRITICAL: MATERIAL'}")
    print(f"   • 96h Statutory Deadline:   {sec_assessment.filing_deadline_hours_remaining:.1f} hours remaining")

    # 4. FFIEC CAT & FDIC Part 370 BaaS Continuous Supervision
    print("\n[4/5] FFIEC CAT & FDIC Part 370 Continuous Sponsor-Bank Supervision...")
    ffiec_attestor = FFIECBaaSAttestor()
    ffiec_att = ffiec_attestor.attest_baas_program(
        sponsor_bank_name="Cross River / Evolve Sponsor Bank Core",
        fintech_partner_name="Apex Growth Systems FinTech Enclave",
        omnibus_fbo_parity_delta_usd=0.00,  # Strict zero-drift invariant
        cat_maturity_level="Advanced",
        fdic_part_370_qualified=True,
        suspense_balance_usd=120.00
    )
    print(f"   • Sponsor Bank Partner:     {ffiec_att.sponsor_bank_name}")
    print(f"   • FBO Omnibus Parity Delta: ${ffiec_att.omnibus_fbo_parity_delta_usd:.2f} USD (Zero-Drift Proved)")
    print(f"   • FFIEC CAT Maturity:       {ffiec_att.cat_maturity_level} (Exceeds Intermediate)")
    print(f"   • FDIC Part 370 Recordkeep: {'QUALIFIED (Automated Partitioning)' if ffiec_att.fdic_part_370_qualified else 'DEFICIENT'}")
    print(f"   • BaaS Supervision Status:  {'CERTIFIED (No Consent Order Risk)' if ffiec_att.is_certified else 'DEFICIENT'}")

    # 5. Master Sealing to a2zsoc.com Evidence Vault
    print("\n[5/5] Consolidating & Sealing to a2zsoc.com Evidence Vault...")
    master_bridge = A2ZSOCMasterGRCBridge()
    unified_receipt = master_bridge.seal_master_grc_receipt(
        tenant_id="tenant_apex_sovereign_01",
        dora_reg=dora_reg,
        dora_compliant=dora_ok,
        ai_event=ai_event,
        sec_assessment=sec_assessment,
        ffiec_attestation=ffiec_att,
        pci_dss_level_1_sealed=True
    )
    print(f"   • a2zsoc Receipt ID:        {unified_receipt.receipt_id}")
    print(f"   • Controls Cross-Walked:    {unified_receipt.total_controls_evaluated} unified controls")
    print(f"   • Overall Compliance Score: {unified_receipt.compliance_score * 100:.1f}%")
    print(f"   • Cryptographic Seal:       {unified_receipt.a2zsoc_merkle_seal}")
    print(f"   • Frameworks Validated:     EU DORA, ISO 42001, SEC 96h, FFIEC CAT, PCI DSS 4.0")

    print("\n" + "=" * 80)
    print("✅ MULTI-FRAMEWORK AGENTIC GRC SPRINT COMPLETED: Zero Audit Theater.")
    print("=" * 80 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic GRC FinTech CLI")
    parser.add_argument("--demo", action="store_true", help="Run end-to-end multi-framework GRC audit sprint")
    args = parser.parse_args()

    if args.demo or len(sys.argv) == 1:
        run_demo()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
