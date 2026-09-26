"""
ISO/IEC 42001:2023 & EU AI Act Autonomous Agent Governance Engine.
Enforces non-repudiation, prompt injection verification, and algorithmic fairness metrics.
"""

import hashlib
import secrets
import time
from typing import Optional, Tuple
from .models import AIGovernanceEvent


class ISO42001AgentGovernor:
    """
    Continuous runtime governor for autonomous financial AI agents.
    Assesses model execution traces against ISO/IEC 42001 Annex A controls.
    """

    ALLOWED_FRONTIER_MODELS = {
        "Claude Opus 5.5",
        "GPT-6 Astra",
        "GPT-6 Sol",
        "DeepSeek V4.1-Flash"
    }

    MIN_FAIRNESS_PARITY = 0.80  # Four-fifths rule for lending/credit underwriting parity

    def evaluate_agent_action(
        self,
        agent_id: str,
        model_name: str,
        task_scope: str,
        prompt_injection_tested: bool,
        bias_metric_parity: float,
        mandate_hash: str
    ) -> AIGovernanceEvent:
        """
        Validates an agent decision against ISO 42001 & EU AI Act High-Risk parameters.
        """
        reasons = []

        # 1. Model authorization check
        if model_name not in self.ALLOWED_FRONTIER_MODELS:
            reasons.append(f"Model '{model_name}' is not in approved ISO 42001 frontier registry")

        # 2. Prompt injection safety validation
        if not prompt_injection_tested:
            reasons.append("Agent invocation bypassed OWASP LLM01 prompt injection verification")

        # 3. Demographic & lending fairness parity check
        if bias_metric_parity < self.MIN_FAIRNESS_PARITY:
            reasons.append(f"Algorithmic fairness parity ({bias_metric_parity:.2f}) violates 80% threshold")

        # 4. Non-repudiation mandate binding
        if not mandate_hash or len(mandate_hash) < 16:
            reasons.append("Missing cryptographic non-repudiation mandate hash")

        is_compliant = len(reasons) == 0
        event_id = f"ai_gov_{secrets.token_hex(8)}"

        return AIGovernanceEvent(
            event_id=event_id,
            agent_id=agent_id,
            model_name=model_name,
            task_scope=task_scope,
            prompt_injection_tested=prompt_injection_tested,
            bias_metric_parity=bias_metric_parity,
            mandate_hash=mandate_hash,
            is_compliant=is_compliant,
            rejection_reason="; ".join(reasons) if reasons else None,
        )
