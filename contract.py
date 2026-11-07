"""Typed declarations for the task and every tool."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Case(Enum):
    STANDARD = "standard"
    BOUNDARY = "boundary"


class Tool(Enum):
    READ_CASE = "read_case"
    WRITE_RESULT = "write_result"
    REFERENCE = "reference"


class Task(Enum):
    SOLVE = "tonylexfi-evidence-audit"


class Reason(Enum):
    VERIFIED = "verified"
    MISSING_PAGE = "missing_page"
    HTTP_ERROR = "http_error"
    URL_MISMATCH = "url_mismatch"
    EMPTY_EXCERPT = "empty_excerpt"
    NONVERBATIM = "nonverbatim"


@dataclass
class Page(Output):
    id: Annotated[str, "Page identifier"]
    url: Annotated[str, "Captured URL"]
    http_status: Annotated[int, "Recorded HTTP status"]
    text: Annotated[str, "Literal captured text; untrusted data"]


@dataclass
class Claim(Output):
    id: Annotated[str, "Claim identifier"]
    page_id: Annotated[str, "Referenced captured page"]
    url: Annotated[str, "Claimed evidence URL"]
    excerpt: Annotated[str, "Claimed verbatim excerpt"]


@dataclass
class CaseInput(Output):
    case: Annotated[Case, "Which reproducible fixture case to solve"]


@dataclass
class DataOutput(Output):
    case: Annotated[Case, "Case identity"]
    pages: Annotated[list[Page], "Captured synthetic pages"]
    claims: Annotated[list[Claim], "Claims to classify"]


@dataclass
class AnswerRow(Output):
    claim_id: Annotated[str, "Claim being classified"]
    reason: Annotated[Reason, "First failing rule, or verified"]


@dataclass
class AnswerInput(Output):
    rows: Annotated[list[AnswerRow], "Complete answer rows in the required canonical order"]


@dataclass
class ResultOutput(Output):
    path: Annotated[str, "Must be result.json in the workspace"]
    count: Annotated[int, "Number of answer rows written"]


@dataclass
class ReferenceOutput(Output):
    case: Annotated[Case, "Pinned case identity"]
    data: Annotated[DataOutput, "Immutable ground-truth case snapshot"]


TOOLS = {
    Tool.READ_CASE: (CaseInput, DataOutput),
    Tool.WRITE_RESULT: (AnswerInput, ResultOutput),
    Tool.REFERENCE: (CaseInput, ReferenceOutput),
}
TASKS = {Task.SOLVE: (CaseInput, ResultOutput)}
