"""
Data models and regulatory schemas for agentic-grc-fintech.
Normalized multi-framework schemas covering EU DORA, ISO/IEC 42001, SEC 96h, and FFIEC BaaS.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time


@dataclass
class DORAICTDependency:
    """Represents a third-party ICT service provider under EU DORA Articles 28-44."""
    provider_id: str
    provider_name: str
    service_type: str
    criticality: str  # "CRITICAL_FUNCTION" | "IMPORTANT" | "STANDARD"
    country_code: str
    sub_processors: List[str]
    has_exit_strategy: bool
    rto_minutes: int
    contract_start: str
    last_audit_date: str


@dataclass
class DORARegisterOfInformation:
    """EBA/ESMA Annex I standardized Register of Information."""
    register_id: str
    reporting_entity: str
    lei_code: str
    total_providers: int
    critical_providers: int
    register_xml_hash: str
    generated_at: float = field(default_factory=time.time)


@dataclass
class AIGovernanceEvent:
    """Autonomous AI Agent action audit trace under ISO/IEC 42001 & EU AI Act."""
    event_id: str
    agent_id: str
    model_name: str  # "Claude Opus 5.5" | "GPT-6 Astra" | "GPT-6 Sol"
    task_scope: str
    prompt_injection_tested: bool
    bias_metric_parity: float  # Demographic / Lending Parity (0.0 to 1.0)
    mandate_hash: str
    is_compliant: bool
    rejection_reason: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class SECMaterialityAssessment:
    """SEC Form 8-K Item 1.05 & Regulation S-P Materiality Assessment."""
    incident_id: str
    asset_compromised: str
    records_impacted: int
    regulatory_fine_exposure_usd: float
    contractual_sla_exposure_usd: float
    reputation_churn_exposure_usd: float
    total_dollar_exposure_usd: float
    materiality_threshold_usd: float
    is_material: bool
    hours_since_detection: float
    filing_deadline_hours_remaining: float
    form_8k_item_1_05_draft: str
    reg_sp_notice_required: bool
    timestamp: float = field(default_factory=time.time)


@dataclass
class FFIECBaaSAttestation:
    """Sponsor bank continuous supervision attestation under FFIEC & FDIC Part 370."""
    attestation_id: str
    sponsor_bank_name: str
    fintech_partner_name: str
    omnibus_fbo_parity_delta_usd: float
    cat_maturity_level: str  # "Baseline" | "Evolving" | "Intermediate" | "Advanced" | "Innovative"
    fdic_part_370_qualified: bool
    suspense_balance_usd: float
    is_certified: bool
    timestamp: float = field(default_factory=time.time)


@dataclass
class UnifiedGRCReceipt:
    """Consolidated compliance attestation sealed to a2zsoc.com Evidence Vault."""
    receipt_id: str
    tenant_id: str
    total_controls_evaluated: int
    compliance_score: float
    dora_compliant: bool
    iso42001_compliant: bool
    sec_reporting_ready: bool
    ffiec_baas_compliant: bool
    pci_dss_level_1_sealed: bool
    a2zsoc_merkle_seal: str
    timestamp: float = field(default_factory=time.time)
