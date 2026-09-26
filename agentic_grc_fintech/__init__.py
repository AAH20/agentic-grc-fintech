"""
agentic-grc-fintech: Autonomous Multi-Cloud GRC & Regulatory Exam OS for FinTech beyond PCI DSS.
Covers EU DORA, ISO/IEC 42001, SEC 96h Materiality, and FFIEC BaaS Continuous Supervision.
"""

from .models import (
    DORAICTDependency,
    DORARegisterOfInformation,
    AIGovernanceEvent,
    SECMaterialityAssessment,
    FFIECBaaSAttestation,
    UnifiedGRCReceipt
)
from .dora_register_engine import DORARegisterEngine
from .iso42001_agent_governor import ISO42001AgentGovernor
from .sec_materiality_quantifier import SECMaterialityQuantifier
from .ffiec_baas_attestor import FFIECBaaSAttestor
from .a2zsoc_master_grc_bridge import A2ZSOCMasterGRCBridge

__version__ = "1.0.0"
__all__ = [
    "DORAICTDependency",
    "DORARegisterOfInformation",
    "AIGovernanceEvent",
    "SECMaterialityAssessment",
    "FFIECBaaSAttestation",
    "UnifiedGRCReceipt",
    "DORARegisterEngine",
    "ISO42001AgentGovernor",
    "SECMaterialityQuantifier",
    "FFIECBaaSAttestor",
    "A2ZSOCMasterGRCBridge",
]
