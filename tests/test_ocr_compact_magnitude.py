"""Regression: compact magnitudes (1.2B / 926.6M) must survive digit repair."""
from cogs.bear_track import repair_ocr_digits
from cogs.attendance_ocr_parsers import _parse_player_value_rows, _ALLIANCE_RANK_RE


def test_repair_keeps_billion_suffix():
    raw = "MONI 1.2B R5 Magiko 1.1B R4 Santisomo 926.6M"
    fixed = repair_ocr_digits(raw)
    assert "1.2B" in fixed
    assert "1.1B" in fixed
    assert "1.28" not in fixed
    assert "1.18" not in fixed
    rows = _parse_player_value_rows(fixed)
    by_name = {r["name"]: r["value"] for r in rows}
    assert by_name["MONI"] == 1_200_000_000
    assert by_name["Magiko"] == 1_100_000_000
    assert by_name["Santisomo"] == 926_600_000


def test_alliance_rank_no_space_after_dot():
    text = "Congratulations, [Legion 1] of your alliance ranked No.3 in [Canyon Clash]!"
    m = _ALLIANCE_RANK_RE.search(text)
    assert m is not None
    assert int(m.group(1)) == 3
