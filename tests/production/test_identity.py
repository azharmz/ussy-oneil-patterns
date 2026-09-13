from datetime import date

from oneil_patterns.production.identity import (
    base_identity_signature,
    lineage_anchor_signature,
    stable_base_id,
    stable_lineage_id,
)
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction


def _prediction(*, candidate_id="a", semantics="CONFIRMED_STRUCTURE", handle_low="2024-09-10"):
    return MorphologyPrediction(
        candidate_id=candidate_id,
        pattern="CUP_WITH_HANDLE",
        start_date=date(2024, 2, 12),
        end_date=date(2024, 9, 20),
        pivot_source_date=date(2024, 8, 26),
        pivot_level=84.26,
        depth_pct=0.29,
        detector_status="CUP_WITH_HANDLE_AMBIGUOUS",
        detector_faults=("DEEP_HANDLE_EXCEPTIONAL",),
        candidate_semantics=semantics,
        structural_signature=(
            "LEFT_RIM:2024-02-12",
            "CUP_LOW:2024-04-25",
            "RIGHT_RIM:2024-08-26",
            f"HANDLE_LOW:{handle_low}",
        ),
    )


def test_base_id_ignores_candidate_id_and_right_edge_semantics():
    confirmed = _prediction(candidate_id="confirmed", semantics="CONFIRMED_STRUCTURE")
    right_edge = _prediction(candidate_id="right", semantics="OPEN_RIGHT_EDGE_HANDLE:v1")

    assert base_identity_signature(confirmed) == base_identity_signature(right_edge)
    assert stable_base_id("sec-1", confirmed) == stable_base_id("sec-1", right_edge)


def test_different_handle_low_is_new_base_identity_but_same_cwh_lineage():
    first = _prediction(handle_low="2024-09-10")
    second = _prediction(handle_low="2024-09-16")

    assert stable_base_id("sec-1", first) != stable_base_id("sec-1", second)
    assert lineage_anchor_signature(first) == (
        "LEFT_RIM:2024-02-12",
        "CUP_LOW:2024-04-25",
    )
    assert stable_lineage_id("sec-1", first) == stable_lineage_id("sec-1", second)


def test_security_is_part_of_both_stable_ids():
    prediction = _prediction()
    assert stable_base_id("sec-1", prediction) != stable_base_id("sec-2", prediction)
    assert stable_lineage_id("sec-1", prediction) != stable_lineage_id("sec-2", prediction)


def test_db_lineage_allows_second_trough_evolution_without_fuzzy_matching():
    common = dict(
        pattern="DOUBLE_BOTTOM",
        start_date=date(2024, 7, 30),
        end_date=date(2024, 9, 20),
        pivot_source_date=date(2024, 8, 30),
        pivot_level=12.74,
        depth_pct=0.19,
        detector_status="DOUBLE_BOTTOM_RECOGNIZED",
    )
    first = MorphologyPrediction(
        candidate_id="db1",
        structural_signature=(
            "LEFT_HIGH:2024-07-30",
            "TROUGH_1:2024-08-05",
            "MIDDLE_PEAK:2024-08-30",
            "TROUGH_2:2024-09-12",
        ),
        **common,
    )
    second = MorphologyPrediction(
        candidate_id="db2",
        structural_signature=(
            "LEFT_HIGH:2024-07-30",
            "TROUGH_1:2024-08-05",
            "MIDDLE_PEAK:2024-08-30",
            "TROUGH_2:2024-09-18",
        ),
        **common,
    )

    assert stable_base_id("sec-1", first) != stable_base_id("sec-1", second)
    assert stable_lineage_id("sec-1", first) == stable_lineage_id("sec-1", second)
