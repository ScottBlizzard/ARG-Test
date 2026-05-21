# Assignment 2: Final Project

**截止时间：** 5月29日 17:00  
**得分：** 60  
**开放时间：** 5月7日 0:00 至 5月29日 23:59

---

## 1. Assignment 2: Final Project

## Requirements

The assignment requires the development of an **AI-driven AutoTestDesign tool** capable of performing requirements analysis, risk assessment, and systematic test case generation, among other functions, aligning with industry standards like **ISTQB Foundation Level principles** and the detailed test techniques defined in **ISO/IEC/IEEE standards**.

---

## 1.1 AutoTestDesign Requirements

The AutoTestDesign app comprises functional requirements (**1.1.1**) and non-functional requirements (**1.1.2**).

---

## 1.1.1 Functional Requirements (FR)

The system may include the following core features:

| ID | Feature Category | Description |
|---|---|---|
| FR 1.0 | Input/Parsing | The system can ingest software requirements from various sources, such as CSV, plain text, or direct user input. |
| FR 1.1 | Requirement Structuring | The system can parse and tokenize raw text, identifying key components like Input Fields, Data Ranges, Conditions, and Expected Actions. |
| FR 2.0 | Risk Analysis & Prioritization | The system can assign a Risk Score and Test Priority, such as High, Medium, or Low, to each imported requirement. |
| FR 3.0 | Black-Box Test Design | The system can automatically apply and generate test cases for at least three core Black-Box techniques from ISO 29119-4, such as Equivalence Partitioning, Boundary Value Analysis, and Decision Tables. |
| FR 4.0 | White-Box Test Modeling | The system can model system behavior, such as a State Transition Diagram, and generate optimal test sequences for a chosen coverage criterion, such as All States. |
| FR 5.0 | Test Oracle Generation | The system can help synthesize the Expected Result for a given requirement and specific test data. |
| FR 6.0 | Output & Export | The system can generate test artifacts, such as Test Cases, Test Suites, and Risk Scores, in a structured, standard format, such as JSON or Excel/CSV, suitable for import into Test Management Tools. |
| FR 7.0 | Test Suite Optimization | The system includes an optimization to prioritize or minimize the generated Test Suite based on risk or coverage efficiency. |

---

## 1.1.2 Non-Functional Requirements (NFR)

The non-functional requirements include, but are not limited to:

- Performance
- Usability (UX/UI)
- Security
- Maintainability and Technology

---

## 1.2 Project Artifact

The project should include the following artifacts:

### 1. AI-driven AutoTestDesign Tool — 20%

Including:

- Source code
- Prompts
- Setup instructions / README
- Video demonstration

### 2. Risk Analysis Report — 10%

A risk analysis report for the application under test.

### 3. Test Plan — 40%

The test plan must cover at least the following aspects:

#### Project Scope

- Background of the software project
- Overall objectives of the software project

#### Test Items

- Major functional features
- Major non-functional features
- Description of the system architecture
- Main components of the system

#### High-level Test Suite Design

Based on the market requirements document or prototype and the risk analysis, select testing techniques for each test suite.

#### Schedule or Checklist

Show test levels and objectives.

#### Organization Chart

Explain team members’ responsibilities.

#### Chosen Testing Framework and Rationale

Describe the selected testing framework and explain the rationale for choosing it.

#### Cost Estimation

Provide a cost estimation for the project.

### 4. Detailed Test Design and Execution Document — 30%

This document should focus on one major feature or module.

#### Test Case Design

- Design test cases for one selected major feature/module.
- Explain test coverage.
- Use multiple black-box testing techniques.
- Use white-box testing techniques as well.

#### Test Tool Implementation

- Choose a testing framework for executing the tests.
- Ideally, develop test scripts based on the detailed test cases above.

#### Test Result Analysis

Provide a summary based on the test results.

---

## Assessment Criteria

| Criterion | Weight |
|---|---:|
| Understanding of concepts | 10% |
| Coherence of design and implementation | 20% |
| Coverage and effectiveness/usefulness | 40% |
| In-depth analysis, such as generalizability demonstration and reasoning | 20% |
| Presentation | 10% |

---

## 2. Presentation

Each group has **15 minutes** to complete the project presentation, covering all aspects listed above.

A **Q&A session** follows. Reviewers will ask questions based on:

- Submitted documents
- Presentation content
- Software testing fundamentals that students are expected to have learned

---

## Submission

Each group must submit the following materials by email to the TA:

### a) Project Artifact

The project artifact must contain all required content described above.

The cover page must include:

- Team ID
- Full names of all members
- Student IDs of all members

### b) Final Presentation PPT

The first slide must include:

- Team ID
- Full names of all members
- Student IDs of all members

The report and PPT must be submitted in **PDF format**.

The test scripts must be submitted as a **compressed file**.

---

## Submission and Presentation Schedule

| Item | Schedule |
|---|---|
| Submission Deadline | Week 13, Friday, before 17:00 pm |
| Presentation Dates | Week 14–16, Tuesday/Thursday, 10:00–11:35 |
