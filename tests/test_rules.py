from dataclasses import replace

from contract import Case, CaseInput
from plugin.read_case import read_case
from verifier.rules import expected


def test_http_failure_precedes_empty_excerpt(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    claim = replace(data.claims[1], excerpt="", url="wrong")
    assert expected(replace(data, claims=[claim])) == {"rows": [{"claim_id": "C2", "reason": "http_error"}]}


def test_unicode_and_whitespace_are_literal(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    claim = replace(data.claims[7], excerpt="Cafe\u0301 demand rose 8%.")
    assert expected(replace(data, claims=[claim]))["rows"][0]["reason"] == "nonverbatim"


def test_empty_claim_set(tmp_path):
    data = read_case(CaseInput(Case.STANDARD), tmp_path)
    assert expected(replace(data, claims=[])) == {"rows": []}
