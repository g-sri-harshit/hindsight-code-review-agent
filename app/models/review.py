from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueCategory(str, Enum):
    BUG = "bug"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    STYLE = "style"
    TESTING = "testing"


class ReviewIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestion_id: str = Field(
        description="Unique identifier for this review finding."
    )

    severity: Severity

    category: IssueCategory

    title: str

    line: int | None

    explanation: str

    suggestion: str


class CodeReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str

    issues: list[ReviewIssue]