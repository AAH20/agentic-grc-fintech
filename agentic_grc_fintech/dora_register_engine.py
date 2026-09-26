"""
EU DORA (Regulation EU 2022/2554) ICT Third-Party Dependency & Register Engine.
Manages ICT concentration risk and synthesizes EBA/ESMA Annex I Register of Information.
"""

import hashlib
import json
import secrets
import time
from typing import List, Dict, Tuple
from .models import DORAICTDependency, DORARegisterOfInformation


class DORARegisterEngine:
    """
    Automates EU DORA ICT supply-chain compliance across Articles 28-44.
    Tracks critical ICT service providers, sub-processor depth, and exit strategies.
    """

    def __init__(self, reporting_entity: str, lei_code: str):
        self.reporting_entity = reporting_entity
        self.lei_code = lei_code
        self.dependencies: Dict[str, DORAICTDependency] = {}

    def register_provider(
        self,
        provider_name: str,
        service_type: str,
        criticality: str,
        country_code: str,
        sub_processors: List[str],
        has_exit_strategy: bool,
        rto_minutes: int,
        contract_start: str = "2024-01-01",
        last_audit_date: str = "2026-06-15"
    ) -> DORAICTDependency:
        """Enrolls an ICT provider into the continuous DORA registry."""
        provider_id = f"dora_ict_{secrets.token_hex(6)}"
        dep = DORAICTDependency(
            provider_id=provider_id,
            provider_name=provider_name,
            service_type=service_type,
            criticality=criticality,
            country_code=country_code,
            sub_processors=sub_processors,
            has_exit_strategy=has_exit_strategy,
            rto_minutes=rto_minutes,
            contract_start=contract_start,
            last_audit_date=last_audit_date,
        )
        self.dependencies[provider_id] = dep
        return dep

    def evaluate_concentration_risk(self) -> Tuple[bool, List[str]]:
        """
        Evaluates systemic concentration risk under DORA Article 29.
        Returns: (is_compliant, list_of_deficiencies)
        """
        deficiencies = []
        for dep in self.dependencies.values():
            # Critical functions require validated exit strategy and strict RTO <= 60 mins
            if dep.criticality == "CRITICAL_FUNCTION":
                if not dep.has_exit_strategy:
                    deficiencies.append(f"Provider '{dep.provider_name}' is CRITICAL but lacks documented exit strategy")
                if dep.rto_minutes > 60:
                    deficiencies.append(f"Provider '{dep.provider_name}' RTO ({dep.rto_minutes}m) exceeds 60-minute DORA threshold")
                if len(dep.sub_processors) > 4:
                    deficiencies.append(f"Provider '{dep.provider_name}' has excessive 4th-party sub-processor depth ({len(dep.sub_processors)})")

        is_compliant = len(deficiencies) == 0
        return is_compliant, deficiencies

    def synthesize_annex_i_register(self) -> DORARegisterOfInformation:
        """
        Compiles the standardized Register of Information for the European Supervisory Authorities (EBA/ESMA).
        """
        critical_count = sum(1 for d in self.dependencies.values() if d.criticality == "CRITICAL_FUNCTION")
        
        # Build canonical payload
        payload_items = []
        for d in sorted(self.dependencies.values(), key=lambda x: x.provider_id):
            payload_items.append({
                "id": d.provider_id,
                "name": d.provider_name,
                "service": d.service_type,
                "criticality": d.criticality,
                "rto": d.rto_minutes,
                "exit_ready": d.has_exit_strategy,
                "sub_processors": d.sub_processors
            })
            
        raw_repr = json.dumps(payload_items, sort_keys=True)
        xml_hash = hashlib.sha256(raw_repr.encode("utf-8")).hexdigest()

        return DORARegisterOfInformation(
            register_id=f"dora_reg_{secrets.token_hex(8)}",
            reporting_entity=self.reporting_entity,
            lei_code=self.lei_code,
            total_providers=len(self.dependencies),
            critical_providers=critical_count,
            register_xml_hash=xml_hash,
        )
