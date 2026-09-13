from datetime import date

from oneil_patterns.validation.candidate_identity import audit_candidate_identities
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction


def _prediction(candidate_id, *, end, status, semantics):
    return MorphologyPrediction(
        candidate_id=candidate_id,
        pattern="DOUBLE_BOTTOM",
        start_date=date(2024, 7, 30),
        end_date=end,
        pivot_source_date=date(2024, 8, 30),
        pivot_level=12.74,
        depth_pct=0.19,
        detector_status=status,
        candidate_semantics=semantics,
        structural_signature=(
            "LEFT_HIGH:2024-07-30",
            "TROUGH_1:2024-08-05",
            "MIDDLE_PEAK:2024-08-30",
            "TROUGH_2:2024-09-12",
        ),
    )


def test_core_and_right_edge_candidates_share_identity_but_keep_status_conflict():
    core = _prediction(
        "core",
        end=date(2024, 9, 12),
        status="DOUBLE_BOTTOM_REJECTED",
        semantics="CONFIRMED_STRUCTURE",
    )
    right = _prediction(
        "right",
        end=date(2024, 9, 20),
        status="DOUBLE_BOTTOM_RECOGNIZED",
        semantics="OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:v0",
    )

    audit = audit_candidate_identities([right, core])

    assert len(audit) == 1
    item = audit[0]
    assert item.member_count == 2
    assert item.identity_state == "STATUS_CONFLICT"
    assert item.detector_statuses == ("DOUBLE_BOTTOM_RECOGNIZED", "DOUBLE_BOTTOM_REJECTED")
    assert item.candidate_semantics == ("CONFIRMED_STRUCTURE", "OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:v0")
    assert item.end_dates == ("2024-09-12", "2024-09-20")
    assert item.structural_signature[-1] == "TROUGH_2:2024-09-12"


def test_different_structural_signatures_are_different_identities_even_with_same_pivot():
    first = _prediction(
        "first",
        end=date(2024, 9, 20),
        status="DOUBLE_BOTTOM_RECOGNIZED",
        semantics="CONFIRMED_STRUCTURE",
    )
    second = MorphologyPrediction(
        candidate_id="second",
        pattern="DOUBLE_BOTTOM",
        start_date=date(2024, 7, 30),
        end_date=date(2024, 9, 20),
        pivot_source_date=date(2024, 8, 30),
        pivot_level=12.74,
        depth_pct=0.19,
        detector_status="DOUBLE_BOTTOM_RECOGNIZED",
        structural_signature=(
            "LEFT_HIGH:2024-07-30",
            "TROUGH_1:2024-08-12",
            "MIDDLE_PEAK:2024-08-30",
            "TROUGH_2:2024-09-12",
        ),
    )

    audit = audit_candidate_identities([first, second])
    assert len(audit) == 2
    assert len({item.identity_id for item in audit}) == 2


def test_different_cwh_handle_lows_do_not_collapse_into_one_identity():
    common = dict(
        pattern="CUP_WITH_HANDLE",
        start_date=date(2024, 2, 12),
        pivot_source_date=date(2024, 8, 26),
        pivot_level=84.26,
        depth_pct=0.29,
        detector_status="CUP_WITH_HANDLE_AMBIGUOUS",
    )
    first = MorphologyPrediction(
        candidate_id="h1",
        end_date=date(2024, 9, 20),
        structural_signature=(
            "LEFT_RIM:2024-02-12",
            "CUP_LOW:2024-04-25",
            "RIGHT_RIM:2024-08-26",
            "HANDLE_LOW:2024-09-10",
        ),
        **common,
    )
    second = MorphologyPrediction(
        candidate_id="h2",
        end_date=date(2024, 9, 20),
        structural_signature=(
            "LEFT_RIM:2024-02-12",
            "CUP_LOW:2024-04-25",
            "RIGHT_RIM:2024-08-26",
            "HANDLE_LOW:2024-09-16",
        ),
        **common,
    )

    audit = audit_candidate_identities([first, second])
    assert len(audit) == 2
