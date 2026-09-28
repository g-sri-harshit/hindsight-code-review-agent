from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent.reviewer import CodeReviewer


app = FastAPI(
    title="Hindsight Code Reviewer",
    description="A code review agent that learns project-specific decisions.",
    version="0.1.0",
)

reviewer = CodeReviewer()


# ============================================================
# Request Models
# ============================================================

class ReviewRequest(BaseModel):
    code: str
    use_memory: bool = True


class FeedbackRequest(BaseModel):
    feedback: str


# ============================================================
# Frontend
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Hindsight Code Reviewer</title>

    <style>

        * {
            box-sizing: border-box;
        }

        :root {
            --bg: #070a12;
            --panel: #0d111c;
            --panel-2: #111827;
            --border: #20293a;
            --border-light: #2b374b;

            --text: #f8fafc;
            --muted: #94a3b8;
            --muted-2: #64748b;

            --green: #22c55e;
            --green-light: #86efac;
            --green-dark: #052e16;

            --blue: #60a5fa;
            --purple: #a78bfa;

            --danger: #f87171;
            --warning: #fbbf24;
        }


        html {
            scroll-behavior: smooth;
        }


        body {
            margin: 0;

            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 15% 0%,
                    rgba(34, 197, 94, 0.08),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(96, 165, 250, 0.08),
                    transparent 25%
                ),
                var(--bg);

            color: var(--text);

            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }


        button,
        textarea,
        input {
            font: inherit;
        }


        button {
            cursor: pointer;
        }


        /* =====================================================
           APP CONTAINER
        ===================================================== */

        .app {
            width: min(1500px, 94%);
            margin: auto;
            padding: 34px 0 70px;
        }


        /* =====================================================
           HEADER
        ===================================================== */

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;

            margin-bottom: 34px;
        }


        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }


        .brand-icon {
            width: 48px;
            height: 48px;

            display: grid;
            place-items: center;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    #12351f,
                    #0c1f16
                );

            border: 1px solid #1d5b35;

            box-shadow:
                0 0 30px rgba(34, 197, 94, 0.08);

            font-size: 24px;
        }


        .brand-name {
            font-size: 19px;
            font-weight: 800;
            letter-spacing: -0.4px;
        }


        .brand-subtitle {
            margin-top: 3px;

            color: var(--muted-2);

            font-size: 12px;
        }


        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;

            padding: 8px 12px;

            border-radius: 999px;

            border: 1px solid #174d2c;

            background: rgba(5, 46, 22, 0.55);

            color: var(--green-light);

            font-size: 12px;
            font-weight: 700;
        }


        .status-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: var(--green);

            box-shadow:
                0 0 10px rgba(34, 197, 94, 0.8);
        }


        /* =====================================================
           HERO
        ===================================================== */

        .hero {
            margin-bottom: 30px;
        }


        .hero h1 {
            margin: 0;

            max-width: 760px;

            font-size: clamp(32px, 5vw, 56px);

            line-height: 1.04;

            letter-spacing: -2.5px;
        }


        .hero h1 span {
            background:
                linear-gradient(
                    100deg,
                    #f8fafc,
                    #86efac
                );

            -webkit-background-clip: text;
            background-clip: text;

            color: transparent;
        }


        .hero p {
            max-width: 690px;

            margin: 14px 0 0;

            color: var(--muted);

            font-size: 15px;

            line-height: 1.65;
        }


        .hero-tags {
            display: flex;
            flex-wrap: wrap;

            gap: 8px;

            margin-top: 18px;
        }


        .hero-tag {
            padding: 7px 10px;

            border: 1px solid var(--border);

            border-radius: 8px;

            background: rgba(15, 23, 42, 0.55);

            color: #cbd5e1;

            font-size: 11px;
        }


        /* =====================================================
           MAIN GRID
        ===================================================== */

        .workspace {
            display: grid;

            grid-template-columns:
                minmax(0, 1fr)
                minmax(0, 1fr);

            gap: 18px;
        }


        .panel {
            background:
                linear-gradient(
                    180deg,
                    rgba(17, 24, 39, 0.9),
                    rgba(10, 15, 25, 0.94)
                );

            border: 1px solid var(--border);

            border-radius: 18px;

            overflow: hidden;

            box-shadow:
                0 18px 60px rgba(0, 0, 0, 0.22);
        }


        .panel-header {
            min-height: 62px;

            display: flex;

            justify-content: space-between;

            align-items: center;

            gap: 12px;

            padding: 0 18px;

            border-bottom: 1px solid var(--border);
        }


        .panel-title {
            display: flex;
            align-items: center;

            gap: 9px;

            font-size: 13px;
            font-weight: 800;

            letter-spacing: 0.1px;
        }


        .panel-icon {
            color: var(--green-light);
        }


        .panel-label {
            color: var(--muted-2);

            font-size: 10px;

            text-transform: uppercase;

            letter-spacing: 1px;
        }


        .panel-body {
            padding: 18px;
        }


        /* =====================================================
           CODE EDITOR
        ===================================================== */

        .editor-wrap {
            position: relative;
        }


        .editor-top {
            display: flex;

            align-items: center;

            gap: 7px;

            margin-bottom: 10px;
        }


        .editor-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;

            background: #334155;
        }


        .editor-language {
            margin-left: 5px;

            color: var(--muted-2);

            font-family: monospace;

            font-size: 11px;
        }


        textarea.code {
            width: 100%;

            min-height: 430px;

            resize: vertical;

            padding: 17px;

            border-radius: 12px;

            border: 1px solid var(--border);

            outline: none;

            background: #070b13;

            color: #dbeafe;

            font-family:
                "Cascadia Code",
                "Fira Code",
                Consolas,
                monospace;

            font-size: 13px;

            line-height: 1.65;

            tab-size: 4;

            transition:
                border-color 0.2s,
                box-shadow 0.2s;
        }


        textarea.code:focus {
            border-color: #31533e;

            box-shadow:
                0 0 0 3px rgba(34, 197, 94, 0.06);
        }


        .editor-actions {
            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 12px;

            margin-top: 14px;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .btn {
            border: 0;

            border-radius: 10px;

            padding: 10px 15px;

            font-size: 12px;

            font-weight: 800;

            transition:
                transform 0.15s,
                opacity 0.15s,
                border-color 0.15s;
        }


        .btn:hover {
            transform: translateY(-1px);
        }


        .btn:disabled {
            opacity: 0.5;

            cursor: wait;

            transform: none;
        }


        .btn-primary {
            color: #03140a;

            background:
                linear-gradient(
                    135deg,
                    #4ade80,
                    #22c55e
                );

            box-shadow:
                0 8px 25px rgba(34, 197, 94, 0.14);
        }


        .btn-secondary {
            color: #cbd5e1;

            background: #151d2b;

            border: 1px solid var(--border-light);
        }


        .btn-secondary:hover {
            border-color: #46556d;
        }


        /* =====================================================
           MEMORY TOGGLE
        ===================================================== */

        .memory-toggle {
            display: flex;

            align-items: center;

            gap: 9px;

            color: #cbd5e1;

            font-size: 12px;

            cursor: pointer;
        }


        .memory-toggle input {
            position: absolute;

            opacity: 0;
        }


        .switch {
            width: 34px;
            height: 19px;

            position: relative;

            border-radius: 999px;

            background: #273244;

            border: 1px solid #334155;

            transition: 0.2s;
        }


        .switch::after {
            content: "";

            position: absolute;

            width: 13px;
            height: 13px;

            top: 2px;
            left: 2px;

            border-radius: 50%;

            background: #64748b;

            transition: 0.2s;
        }


        .memory-toggle input:checked + .switch {
            background: #14532d;

            border-color: #166534;
        }


        .memory-toggle input:checked + .switch::after {
            transform: translateX(15px);

            background: #4ade80;
        }


        .memory-state {
            color: var(--muted);
        }


        /* =====================================================
           REVIEW OUTPUT
        ===================================================== */

        .review-scroll {
            min-height: 430px;

            max-height: 620px;

            overflow-y: auto;

            padding-right: 3px;
        }


        .empty-state {
            min-height: 430px;

            display: grid;

            place-items: center;

            text-align: center;

            padding: 40px;
        }


        .empty-icon {
            width: 64px;
            height: 64px;

            margin: auto;

            display: grid;
            place-items: center;

            border-radius: 18px;

            background: #111827;

            border: 1px solid var(--border);

            font-size: 28px;
        }


        .empty-title {
            margin-top: 15px;

            font-weight: 800;
        }


        .empty-text {
            max-width: 330px;

            margin-top: 7px;

            color: var(--muted-2);

            font-size: 12px;

            line-height: 1.6;
        }


        /* =====================================================
           MEMORY CARD
        ===================================================== */

        .memory-card {
            margin-bottom: 15px;

            padding: 15px;

            border-radius: 13px;

            border: 1px solid #174d2c;

            background:
                linear-gradient(
                    145deg,
                    rgba(20, 83, 45, 0.18),
                    rgba(6, 32, 19, 0.12)
                );
        }


        .memory-card.off {
            border-color: #3f3a20;

            background:
                linear-gradient(
                    145deg,
                    rgba(120, 90, 10, 0.08),
                    rgba(30, 25, 10, 0.12)
                );
        }


        .memory-heading {
            display: flex;

            justify-content: space-between;

            align-items: center;

            gap: 10px;

            margin-bottom: 10px;
        }


        .memory-title {
            color: var(--green-light);

            font-size: 12px;

            font-weight: 900;
        }


        .memory-card.off .memory-title {
            color: var(--warning);
        }


        .memory-badge {
            padding: 4px 7px;

            border-radius: 6px;

            background: rgba(34, 197, 94, 0.1);

            color: #86efac;

            font-size: 9px;

            font-weight: 800;

            text-transform: uppercase;

            letter-spacing: 0.8px;
        }


        .memory-card.off .memory-badge {
            background: rgba(251, 191, 36, 0.08);

            color: #fde68a;
        }


        .memory-list {
            display: flex;

            flex-direction: column;

            gap: 7px;
        }


        .memory-item {
            padding: 8px 10px;

            border-radius: 8px;

            background: rgba(2, 6, 23, 0.35);

            color: #bbf7d0;

            font-size: 11px;

            line-height: 1.5;
        }


        .memory-card.off .memory-item {
            color: #cbd5e1;
        }


        /* =====================================================
           SUMMARY
        ===================================================== */

        .summary {
            padding: 14px;

            border-radius: 12px;

            border: 1px solid var(--border);

            background: #0a101b;

            margin-bottom: 14px;
        }


        .summary-label {
            color: var(--muted-2);

            font-size: 9px;

            font-weight: 900;

            text-transform: uppercase;

            letter-spacing: 1px;
        }


        .summary-text {
            margin-top: 7px;

            color: #cbd5e1;

            font-size: 12px;

            line-height: 1.6;
        }


        /* =====================================================
           ISSUE CARDS
        ===================================================== */

        .issues {
            display: flex;

            flex-direction: column;

            gap: 9px;
        }


        .issue {
            padding: 13px;

            border-radius: 11px;

            border: 1px solid var(--border);

            background: rgba(8, 13, 23, 0.8);
        }


        .issue-header {
            display: flex;

            align-items: center;

            flex-wrap: wrap;

            gap: 7px;

            margin-bottom: 7px;
        }


        .severity {
            padding: 4px 7px;

            border-radius: 5px;

            font-size: 9px;

            font-weight: 900;

            text-transform: uppercase;

            letter-spacing: 0.6px;
        }


        .severity-critical {
            background: #450a0a;
            color: #fca5a5;
        }


        .severity-high {
            background: #451a03;
            color: #fdba74;
        }


        .severity-medium {
            background: #422006;
            color: #fde68a;
        }


        .severity-low {
            background: #172554;
            color: #bfdbfe;
        }


        .category {
            color: var(--muted-2);

            font-size: 10px;
        }


        .issue-title {
            color: #f1f5f9;

            font-size: 12px;

            font-weight: 800;
        }


        .issue-explanation {
            margin-top: 6px;

            color: #94a3b8;

            font-size: 11px;

            line-height: 1.55;
        }


        .suggestion {
            margin-top: 9px;

            padding: 9px 10px;

            border-left: 2px solid #31533e;

            background: #0c1512;

            color: #cbd5e1;

            font-size: 11px;

            line-height: 1.55;
        }


        .suggestion-label {
            color: var(--green-light);

            font-weight: 800;
        }


        /* =====================================================
           TEACH SECTION
        ===================================================== */

        .teach {
            margin-top: 18px;
        }


        .teach-header {
            display: flex;

            align-items: center;

            gap: 10px;
        }


        .teach-icon {
            width: 32px;
            height: 32px;

            display: grid;
            place-items: center;

            border-radius: 9px;

            background: #10261a;

            border: 1px solid #1b5230;
        }


        .teach-title {
            font-size: 13px;

            font-weight: 800;
        }


        .teach-description {
            margin-top: 2px;

            color: var(--muted-2);

            font-size: 10px;
        }


        textarea.feedback {
            width: 100%;

            min-height: 100px;

            margin-top: 14px;

            padding: 13px;

            resize: vertical;

            outline: none;

            border-radius: 11px;

            border: 1px solid var(--border);

            background: #080d16;

            color: #dbeafe;

            font-size: 12px;

            line-height: 1.55;
        }


        textarea.feedback:focus {
            border-color: #31533e;
        }


        .teach-actions {
            display: flex;

            gap: 8px;

            margin-top: 9px;
        }


        .status {
            min-height: 20px;

            margin-top: 9px;

            color: var(--muted);

            font-size: 11px;
        }


        .status.success {
            color: var(--green-light);
        }


        .status.error {
            color: var(--danger);
        }


        /* =====================================================
           LEARNING FLOW
        ===================================================== */

        .learning {
            margin-top: 18px;
        }


        .learning-grid {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 10px;
        }


        .learning-card {
            padding: 15px;

            border-radius: 12px;

            border: 1px solid var(--border);

            background: rgba(13, 17, 28, 0.85);
        }


        .learning-number {
            color: var(--green-light);

            font-size: 9px;

            font-weight: 900;

            letter-spacing: 1px;
        }


        .learning-title {
            margin-top: 6px;

            font-size: 12px;

            font-weight: 800;
        }


        .learning-text {
            margin-top: 5px;

            color: var(--muted-2);

            font-size: 10px;

            line-height: 1.55;
        }


        /* =====================================================
           LOADING
        ===================================================== */

        .loading {
            display: inline-flex;

            align-items: center;

            gap: 7px;
        }


        .spinner {
            width: 12px;
            height: 12px;

            border-radius: 50%;

            border: 2px solid #334155;

            border-top-color: var(--green);

            animation:
                spin 0.8s linear infinite;
        }


        @keyframes spin {

            to {
                transform: rotate(360deg);
            }

        }


        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 980px) {

            .workspace {
                grid-template-columns: 1fr;
            }

            .review-scroll {
                max-height: none;
            }

        }


        @media (max-width: 650px) {

            .app {
                width: 92%;
                padding-top: 22px;
            }

            .topbar {
                align-items: flex-start;
            }

            .status-pill {
                display: none;
            }

            .hero h1 {
                letter-spacing: -1.5px;
            }

            .learning-grid {
                grid-template-columns: 1fr;
            }

            .editor-actions {
                flex-direction: column;
                align-items: stretch;
            }

            .editor-actions .btn-primary {
                width: 100%;
            }

        }

    </style>

</head>


<body>

<div class="app">


    <!-- ======================================================
         HEADER
    ======================================================= -->

    <header class="topbar">

        <div class="brand">

            <div class="brand-icon">
                🧠
            </div>

            <div>

                <div class="brand-name">
                    Hindsight Code Reviewer
                </div>

                <div class="brand-subtitle">
                    Project-aware AI code review
                </div>

            </div>

        </div>


        <div class="status-pill">

            <span class="status-dot"></span>

            Hindsight connected

        </div>

    </header>


    <!-- ======================================================
         HERO
    ======================================================= -->

    <section class="hero">

        <h1>
            Code review that
            <span>remembers.</span>
        </h1>

        <p>
            Review code with an AI agent that learns your team's
            conventions, architectural decisions, and preferences
            instead of starting from zero every time.
        </p>


        <div class="hero-tags">

            <span class="hero-tag">
                Persistent memory
            </span>

            <span class="hero-tag">
                Project-aware reviews
            </span>

            <span class="hero-tag">
                Developer feedback
            </span>

            <span class="hero-tag">
                Hindsight
            </span>

        </div>

    </section>


    <!-- ======================================================
         WORKSPACE
    ======================================================= -->

    <main class="workspace">


        <!-- ==================================================
             CODE PANEL
        =================================================== -->

        <section class="panel">

            <div class="panel-header">

                <div class="panel-title">

                    <span class="panel-icon">
                        ◈
                    </span>

                    Code

                </div>


                <button
                    class="btn btn-secondary"
                    onclick="loadDemo()"
                >
                    Load demo
                </button>

            </div>


            <div class="panel-body">

                <div class="editor-top">

                    <span class="editor-dot"></span>
                    <span class="editor-dot"></span>
                    <span class="editor-dot"></span>

                    <span class="editor-language">
                        Python
                    </span>

                </div>


                <div class="editor-wrap">

                    <textarea
                        id="codeInput"
                        class="code"
                        spellcheck="false"
                        placeholder="Paste Python code here..."
                    ></textarea>

                </div>


                <div class="editor-actions">


                    <label class="memory-toggle">

                        <input
                            id="memoryToggle"
                            type="checkbox"
                            checked
                            onchange="updateMemoryLabel()"
                        >

                        <span class="switch"></span>

                        <span
                            id="memoryLabel"
                            class="memory-state"
                        >
                            Hindsight memory ON
                        </span>

                    </label>


                    <button
                        id="reviewButton"
                        class="btn btn-primary"
                        onclick="reviewCode()"
                    >
                        Review code →
                    </button>

                </div>

            </div>

        </section>


        <!-- ==================================================
             REVIEW PANEL
        =================================================== -->

        <section class="panel">

            <div class="panel-header">

                <div class="panel-title">

                    <span class="panel-icon">
                        ✦
                    </span>

                    Review

                </div>


                <span
                    id="reviewStatus"
                    class="panel-label"
                >
                    Ready
                </span>

            </div>


            <div
                id="reviewOutput"
                class="panel-body"
            >

                <div class="empty-state">

                    <div>

                        <div class="empty-icon">
                            ✦
                        </div>

                        <div class="empty-title">
                            Ready to review
                        </div>

                        <div class="empty-text">
                            Paste your code and run a review.
                            Enable Hindsight memory to let the
                            agent use learned project context.
                        </div>

                    </div>

                </div>

            </div>

        </section>

    </main>


    <!-- ======================================================
         TEACH AGENT
    ======================================================= -->

    <section class="panel teach">

        <div class="panel-body">

            <div class="teach-header">

                <div class="teach-icon">
                    🧠
                </div>

                <div>

                    <div class="teach-title">
                        Teach the agent
                    </div>

                    <div class="teach-description">
                        Store a project decision or developer preference
                        in persistent Hindsight memory.
                    </div>

                </div>

            </div>


            <textarea
                id="feedbackInput"
                class="feedback"
                placeholder="Example: Keep requests for synchronous HTTP. Do not recommend httpx unless async HTTP is actually required."
            ></textarea>


            <div class="teach-actions">

                <button
                    id="teachButton"
                    class="btn btn-primary"
                    onclick="teachAgent()"
                >
                    Teach agent
                </button>


                <button
                    class="btn btn-secondary"
                    onclick="loadFeedback()"
                >
                    Load example
                </button>

            </div>


            <div
                id="feedbackStatus"
                class="status"
            ></div>

        </div>

    </section>


    <!-- ======================================================
         LEARNING FLOW
    ======================================================= -->

    <section class="learning">

        <div class="learning-grid">


            <div class="learning-card">

                <div class="learning-number">
                    STEP 01
                </div>

                <div class="learning-title">
                    Review
                </div>

                <div class="learning-text">
                    The agent analyzes code using general
                    engineering knowledge.
                </div>

            </div>


            <div class="learning-card">

                <div class="learning-number">
                    STEP 02
                </div>

                <div class="learning-title">
                    Learn
                </div>

                <div class="learning-text">
                    Developer feedback becomes persistent
                    project memory through Hindsight.
                </div>

            </div>


            <div class="learning-card">

                <div class="learning-number">
                    STEP 03
                </div>

                <div class="learning-title">
                    Improve
                </div>

                <div class="learning-text">
                    Future reviews recall that knowledge and
                    adapt recommendations to the project.
                </div>

            </div>


        </div>

    </section>


</div>


<script>


// ============================================================
// Demo Data
// ============================================================

const demoCode = `
import requests


def fetch_users(user_ids):
    results = []

    for user_id in user_ids:
        response = requests.get(
            f"https://api.example.com/users/{user_id}"
        )
        response.raise_for_status()
        results.append(response.json())

    return results
`.trim();


const demoFeedback = `
Architectural decision: This project uses requests for
synchronous HTTP calls. Do not recommend replacing requests
with httpx or another async HTTP library unless there is a
concrete requirement for asynchronous execution.
`.trim();


// ============================================================
// Helpers
// ============================================================

function loadDemo() {

    document.getElementById("codeInput").value = demoCode;

}


function loadFeedback() {

    document.getElementById("feedbackInput").value = demoFeedback;

}


function updateMemoryLabel() {

    const enabled =
        document.getElementById("memoryToggle").checked;

    const label =
        document.getElementById("memoryLabel");

    label.textContent =
        enabled
            ? "Hindsight memory ON"
            : "Hindsight memory OFF";
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


// ============================================================
// Render Review
// ============================================================

function renderReview(data) {

    const output =
        document.getElementById("reviewOutput");

    const memoryEnabled =
        data.memory_enabled;

    const memories =
        data.memory_used || [];

    const issues =
        data.issues || [];


    let html = `<div class="review-scroll">`;


    // --------------------------------------------------------
    // Memory
    // --------------------------------------------------------

    if (memoryEnabled) {

        html += `
            <div class="memory-card">

                <div class="memory-heading">

                    <div class="memory-title">
                        🧠 Hindsight memory
                    </div>

                    <div class="memory-badge">
                        recalled
                    </div>

                </div>

                <div class="memory-list">
        `;


        if (memories.length === 0) {

            html += `
                <div class="memory-item">
                    No relevant project memory found.
                </div>
            `;

        } else {

            memories.forEach(memory => {

                html += `
                    <div class="memory-item">
                        ${escapeHtml(memory)}
                    </div>
                `;

            });

        }


        html += `
                </div>

            </div>
        `;

    } else {

        html += `
            <div class="memory-card off">

                <div class="memory-heading">

                    <div class="memory-title">
                        🧠 Hindsight memory
                    </div>

                    <div class="memory-badge">
                        disabled
                    </div>

                </div>

                <div class="memory-list">

                    <div class="memory-item">
                        This review uses only general
                        code-review knowledge.
                    </div>

                </div>

            </div>
        `;

    }


    // --------------------------------------------------------
    // Summary
    // --------------------------------------------------------

    html += `
        <div class="summary">

            <div class="summary-label">
                Review summary
            </div>

            <div class="summary-text">
                ${escapeHtml(data.summary)}
            </div>

        </div>
    `;


    // --------------------------------------------------------
    // Issues
    // --------------------------------------------------------

    html += `
        <div class="issues">
    `;


    if (issues.length === 0) {

        html += `
            <div class="issue">
                No meaningful issues found.
            </div>
        `;

    } else {

        issues.forEach(issue => {

            const severity =
                escapeHtml(issue.severity);

            const severityClass =
                `severity-${severity}`;

            html += `
                <div class="issue">

                    <div class="issue-header">

                        <span
                            class="severity ${severityClass}"
                        >
                            ${severity}
                        </span>

                        <span class="category">
                            ${escapeHtml(issue.category)}
                        </span>

                    </div>


                    <div class="issue-title">
                        ${escapeHtml(issue.title)}
                    </div>


                    <div class="issue-explanation">
                        ${escapeHtml(issue.explanation)}
                    </div>


                    <div class="suggestion">

                        <span class="suggestion-label">
                            💡 Suggestion
                        </span>

                        <br>

                        ${escapeHtml(issue.suggestion)}

                    </div>

                </div>
            `;

        });

    }


    html += `
        </div>
    `;


    html += `</div>`;


    output.innerHTML = html;

}


// ============================================================
// Review
// ============================================================

async function reviewCode() {

    const code =
        document.getElementById("codeInput")
            .value
            .trim();


    const useMemory =
        document.getElementById("memoryToggle")
            .checked;


    const button =
        document.getElementById("reviewButton");


    const status =
        document.getElementById("reviewStatus");


    if (!code) {

        alert("Paste some code first.");

        return;
    }


    button.disabled = true;

    status.innerHTML = `
        <span class="loading">
            <span class="spinner"></span>
            Reviewing
        </span>
    `;


    try {

        const response =
            await fetch(
                "/api/review",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        code: code,
                        use_memory: useMemory
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.error ||
                "Review failed."
            );

        }


        renderReview(data);

        status.textContent =
            "Review complete";


    } catch (error) {

        document.getElementById(
            "reviewOutput"
        ).innerHTML = `

            <div class="empty-state">

                <div>

                    <div class="empty-icon">
                        !
                    </div>

                    <div class="empty-title">
                        Review failed
                    </div>

                    <div class="empty-text">
                        ${escapeHtml(error.message)}
                    </div>

                </div>

            </div>
        `;

        status.textContent = "Error";


    } finally {

        button.disabled = false;

    }

}


// ============================================================
// Teach Agent
// ============================================================

async function teachAgent() {

    const feedback =
        document.getElementById("feedbackInput")
            .value
            .trim();


    const button =
        document.getElementById("teachButton");


    const status =
        document.getElementById("feedbackStatus");


    if (!feedback) {

        alert(
            "Enter a project decision or preference first."
        );

        return;
    }


    button.disabled = true;

    status.className = "status";

    status.textContent =
        "Storing decision in Hindsight...";


    try {

        const response =
            await fetch(
                "/api/feedback",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        feedback: feedback
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.error ||
                "Could not store feedback."
            );

        }


        status.className =
            "status success";

        status.textContent =
            "✓ Learned and stored in Hindsight.";


    } catch (error) {

        status.className =
            "status error";

        status.textContent =
            "✕ " + error.message;


    } finally {

        button.disabled = false;

    }

}


// ============================================================
// Keyboard shortcut
// ============================================================

document
    .getElementById("codeInput")
    .addEventListener(
        "keydown",
        function(event) {

            if (
                event.ctrlKey &&
                event.key === "Enter"
            ) {

                reviewCode();

            }

        }
    );


</script>

</body>

</html>
"""


# ============================================================
# Routes
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "hindsight-code-review-agent",
    }


@app.post("/api/review")
def review_code(request: ReviewRequest):

    if not request.code.strip():

        return {
            "error": "Code cannot be empty."
        }


    review = reviewer.review(
        code=request.code,
        use_memory=request.use_memory,
    )


    return {
        "summary": review.summary,

        "memory_enabled": getattr(
            review,
            "_memory_enabled",
            False,
        ),

        "memory_used": getattr(
            review,
            "_memory_used",
            [],
        ),

        "issues": [

            {
                "suggestion_id":
                    issue.suggestion_id,

                "severity":
                    issue.severity.value,

                "category":
                    issue.category.value,

                "title":
                    issue.title,

                "line":
                    issue.line,

                "explanation":
                    issue.explanation,

                "suggestion":
                    issue.suggestion,
            }

            for issue in review.issues
        ],
    }


@app.post("/api/feedback")
def teach_agent(request: FeedbackRequest):

    if not request.feedback.strip():

        return {
            "error": "Feedback cannot be empty."
        }


    result = reviewer.retain_feedback(
        feedback=request.feedback,
        context="Explicit developer project decision",
    )


    return {
        "success": result.success,
        "message":
            "Developer feedback stored in Hindsight.",
    }
"""


# ============================================================
# END
# ============================================================
"""