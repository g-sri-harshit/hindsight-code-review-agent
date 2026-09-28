from app.models.review import (
    CodeReview,
    IssueCategory,
    ReviewIssue,
    Severity,
)


def test_review_schema():
    issue = ReviewIssue(
        suggestion_id="SEC-001",
        severity=Severity.HIGH,
        category=IssueCategory.SECURITY,
        title="Missing input validation",
        line=12,
        explanation="User input is used without validation.",
        suggestion="Validate the input before processing it.",
    )

    review = CodeReview(
        summary="The code contains a security issue.",
        issues=[issue],
    )

    assert review.summary == "The code contains a security issue."
    assert len(review.issues) == 1
    assert review.issues[0].severity == Severity.HIGH