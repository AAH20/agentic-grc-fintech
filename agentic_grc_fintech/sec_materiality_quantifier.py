"""
SEC Form 8-K Item 1.05 & Regulation S-P 96-Hour Materiality Quantification Engine.
Translates security incident blast radius into defensible dollar-denominated exposure.
"""

import secrets
import time
from typing import Dict, Any, Tuple
from .models import SECMaterialityAssessment


class SECMaterialityQuantifier:
    """
    Algorithmic materiality assessment for SEC Form 8-K Item 1.05.
    Calculates blast-radius liability and monitors the 96-hour statutory disclosure countdown.
    """

    STATUTORY_DEADLINE_HOURS = 96.0  # 4 business days under SEC Rule 1.05

    def __init__(self, corporate_materiality_threshold_usd: float = 1_000_000.0):
        self.materiality_threshold = corporate_materiality_threshold_usd

    def assess_incident(
        self,
        incident_id: str,
        asset_compromised: str,
        records_impacted: int,
        outage_duration_hours: float,
        direct_funds_diverted_usd: float,
        hours_since_detection: float
    ) -> SECMaterialityAssessment:
        """
        Computes multi-dimensional financial liability and determines Form 8-K filing necessity.
        """
        # 1. Statutory notification & regulatory fines ($150 / impacted customer record)
        reg_exposure = float(records_impacted) * 150.0

        # 2. Contractual SLA penalties ($25,000 / hour of production outage)
        sla_exposure = outage_duration_hours * 25_000.0

        # 3. Direct financial loss + expected reputation churn (15% multiplier)
        reputation_exposure = direct_funds_diverted_usd * 0.15
        total_exposure = reg_exposure + sla_exposure + direct_funds_diverted_usd + reputation_exposure

        is_material = total_exposure >= self.materiality_threshold
        deadline_remaining = max(0.0, self.STATUTORY_DEADLINE_HOURS - hours_since_detection)

        # Generate Form 8-K Item 1.05 Draft if Material
        if is_material:
            draft_8k = (
                f"UNITED STATES SECURITIES AND EXCHANGE COMMISSION\n"
                f"FORM 8-K | CURRENT REPORT PURSUANT TO SECTION 13 OR 15(d)\n"
                f"Item 1.05: Material Cybersecurity Incidents.\n"
                f"On {time.strftime('%Y-%m-%d', time.gmtime())}, the Registrant determined that a cybersecurity incident "
                f"impacting '{asset_compromised}' is material. Estimated exposure: ${total_exposure:,.2f} USD. "
                f"Records involved: {records_impacted:,}. Immediate containment protocols deployed."
            )
        else:
            draft_8k = "INCIDENT_EVALUATED_NON_MATERIAL: Exposure below corporate threshold. No 8-K required."

        # Reg S-P triggers when customer records exceed 500
        reg_sp_notice = records_impacted >= 500

        return SECMaterialityAssessment(
            incident_id=incident_id,
            asset_compromised=asset_compromised,
            records_impacted=records_impacted,
            regulatory_fine_exposure_usd=reg_exposure,
            contractual_sla_exposure_usd=sla_exposure,
            reputation_churn_exposure_usd=reputation_exposure,
            total_dollar_exposure_usd=total_exposure,
            materiality_threshold_usd=self.materiality_threshold,
            is_material=is_material,
            hours_since_detection=hours_since_detection,
            filing_deadline_hours_remaining=deadline_remaining,
            form_8k_item_1_05_draft=draft_8k,
            reg_sp_notice_required=reg_sp_notice,
        )
