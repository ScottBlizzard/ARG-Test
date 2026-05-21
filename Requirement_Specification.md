# 📄 Requirement Specification: AutoTestDesign AI App

**作者：** 刘琴  
**适用范围：** 所有班级  
**状态：** 无未读答复。无答复。

---

## 1. Introduction

The **AutoTestDesign AI Application** is a proposed system designed to automate and enhance software test design activities, aligning with industry standards like **ISTQB Foundation Level principles** and the detailed test techniques defined in **ISO/IEC/IEEE 29119-4**.

The primary goal is to leverage **Artificial Intelligence (AI)** and **Machine Learning (ML)** to perform requirements analysis, risk assessment, and systematic test case generation, thereby improving test efficiency and coverage.

---

## 2. Goals and Objectives

| ID | Goal | Description |
|---|---|---|
| G1 | Standard Alignment | Ensure generated test artifacts, such as test cases and priority scores, comply with established testing standards, including ISTQB terminology and ISO 29119 structure. |
| G2 | Automation | Automate complex, rule-based test design techniques, such as EP, BVA, and Decision Tables. |
| G3 | Risk-Based Testing | Integrate risk analysis early in the process to prioritize testing effort. |
| G4 | Modularity | Design a platform that allows easy integration of new test design algorithms and AI models as distinct modules. |

---

## 3. Functional Requirements (FR)

The system must support the following core features:

| ID | Feature Category | Description |
|---|---|---|
| FR 1.0 | Input / Parsing | The system must be able to ingest software requirements from various sources, such as CSV, plain text, or direct user input. |
| FR 1.1 | Requirement Structuring | The system must use Natural Language Processing (NLP) to parse and tokenize raw text, identifying key components like Input Fields, Data Ranges, Conditions, and Expected Actions. |
| FR 2.0 | Risk Analysis & Prioritization | The system must employ an AI/ML model, Project 1, to assign a Risk Score and Test Priority, including High, Medium, or Low, to each imported requirement. |
| FR 3.0 | Black-Box Test Design | The system must include modules to automatically apply and generate test cases for at least three core Black-Box techniques from ISO 29119-4, such as Equivalence Partitioning, Boundary Value Analysis, and Decision Tables. |
| FR 4.0 | White-Box Test Modeling | The system must include a module to model system behavior, such as State Transition Diagram, and generate optimal test sequences for a chosen coverage criterion, such as All States. |
| FR 5.0 | Test Oracle Generation | The system must include a component, Project 10, to help synthesize the Expected Result for a given requirement and specific test data. |
| FR 6.0 | Output & Export | The system must generate test artifacts, including Test Cases, Test Suites, and Risk Scores, in a structured, standard format, such as JSON or Excel/CSV, suitable for import into Test Management Tools. |
| FR 7.0 | Test Suite Optimization | The system must include an optimization module, Project 4 or 9, to prioritize or minimize the generated Test Suite based on risk or coverage efficiency. |

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance

| ID | Requirement | Description |
|---|---|---|
| NFR 4.1.1 | Analysis Time | Requirements processing and risk analysis for a batch of 100 requirements must complete within 5 seconds. |
| NFR 4.1.2 | Test Case Generation | Generation of a full set of test cases for a single requirement, such as Decision Table, must not exceed 2 seconds. |

---

### 4.2 Usability (UX/UI)

| ID | Requirement | Description |
|---|---|---|
| NFR 4.2.1 | Interface | The application must provide a clean, intuitive User Interface (UI) to input requirements and view generated test artifacts. |
| NFR 4.2.2 | Traceability | All generated test cases must clearly link back to the original requirement ID and the design technique used. |

---

### 4.3 Security

| ID | Requirement | Description |
|---|---|---|
| NFR 4.3.1 | Data Handling | If requirement data contains sensitive information, the system must implement basic access control. For a student project, this may be simplified. |

---

### 4.4 Maintainability and Technology

| ID | Requirement | Description |
|---|---|---|
| NFR 4.4.1 | Technology Stack | The application should be developed using a modern, open-source technology stack suitable for AI/ML integration, such as Python/Flask/Django for backend logic and ML, and HTML/CSS/JavaScript or a frontend framework for the UI. |
| NFR 4.4.2 | Modularity | The architecture must enforce loose coupling between the core framework and the individual test design modules, Projects 1-10, to allow for independent development and swapping of algorithms. |
| NFR 4.4.3 | Documentation | All code must be well-documented, and the project must include a System Architecture Diagram and a User Manual. |

---

## 5. Technical Constraints

| ID | Constraint | Description |
|---|---|---|
| C 5.1 | AI Framework | Students must use common AI/ML libraries, such as Scikit-learn, TensorFlow, PyTorch, or spaCy for NLP, for their respective modules. |
| C 5.2 | Data | The system must include a sample mock dataset of requirements and historical execution results for training and demonstration purposes. |
| C 5.3 | Language | All core logic and UI must be developed in the chosen primary development language, such as Python. |