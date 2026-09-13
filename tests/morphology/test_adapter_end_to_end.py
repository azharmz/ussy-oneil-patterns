from oneil_patterns.morphology.adapters import (
    normalize_ascending_base,
    normalize_base_on_base,
    normalize_cup_body,
    normalize_double_bottom,
)
from oneil_patterns.morphology.ascending_base_detector import assess_ascending_base
from oneil_patterns.morphology.base_on_base import (
    BaseOnBaseGeometry,
    BaseOnBaseState,
    BaseRegionSummary,
    assess_base_on_base,
)
from oneil_patterns.morphology.cup_body_detector import assess_cup_body
from oneil_patterns.morphology.double_bottom_detector import assess_double_bottom
from oneil_patterns.morphology.faults import NormalizedStatus, RuleProvenance
from tests.fixtures.ascending_bases import ascending_base_fixtures
from tests.fixtures.cup_bodies import cup_body_fixtures
from tests.fixtures.double_bottoms import double_bottom_fixtures


def _by_name(fixtures):
    return {fixture.name: fixture for fixture in fixtures}


def test_double_bottom_research_ambiguity_preserves_provenance():
    native = assess_double_bottom(_by_name(double_bottom_fixtures())["shallow_undercut"].geometry)
    envelope = normalize_double_bottom(native)
    assert envelope.status == NormalizedStatus.AMBIGUOUS
    assert envelope.contract_version == "double-bottom-v3"
    assert envelope.faults[0].provenance == RuleProvenance.RESEARCH


def test_cup_research_ambiguity_preserves_provenance():
    native = assess_cup_body(_by_name(cup_body_fixtures())["sharp_v"].geometry)
    envelope = normalize_cup_body(native)
    assert envelope.status == NormalizedStatus.AMBIGUOUS
    assert envelope.contract_version == "cup-family-v2"
    assert any(f.code == "SHARP_V" and f.provenance == RuleProvenance.RESEARCH for f in envelope.faults)


def test_ascending_rejection_and_source_guardrail_ambiguity_remain_distinct():
    fixtures = _by_name(ascending_base_fixtures())
    hard = normalize_ascending_base(assess_ascending_base(fixtures["nonascending_trough"].geometry))
    soft = normalize_ascending_base(assess_ascending_base(fixtures["irregular_depth"].geometry))

    assert hard.status == NormalizedStatus.REJECTED
    assert any(f.provenance == RuleProvenance.THEORY for f in hard.faults)
    assert soft.status == NormalizedStatus.AMBIGUOUS
    assert all(f.provenance == RuleProvenance.THEORY for f in soft.faults)
    assert soft.contract_version == "ascending-base-v2"


def test_base_on_base_adapter_uses_advanced_contract_v2():
    from datetime import date

    b1 = BaseRegionSummary("CUP_WITH_HANDLE", date(2026, 1, 1), date(2026, 1, 20), date(2026, 1, 20), 100.0, 75.0)
    b2 = BaseRegionSummary("FLAT_BASE", date(2026, 1, 25), date(2026, 2, 10), date(2026, 2, 10), 108.0, 97.0)
    geometry = BaseOnBaseGeometry(
        base_1=b1,
        base_2=b2,
        confirmed_date=date(2026, 2, 10),
        relation_sessions=4,
        combined_duration_sessions=41,
        second_low_to_first_high_ratio=0.97,
        second_close_fraction_above_first_high=0.60,
    )
    native = assess_base_on_base(geometry)
    assert native.state == BaseOnBaseState.AMBIGUOUS

    envelope = normalize_base_on_base(native)
    assert envelope.status == NormalizedStatus.AMBIGUOUS
    assert envelope.contract_version == "advanced-patterns-v2"
    assert envelope.faults[0].provenance == RuleProvenance.THEORY
