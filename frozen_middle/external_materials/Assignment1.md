# Assignment 1: AI-Enhanced Software Testing

## 1. Requirements
The assignment requires students to design and implement (or enhance) a testing technique using **AI methods** (e.g., LLMs). Students can choose one of the following categories:

* **Static Testing:** Static code analysis.
* **Black-box Dynamic Testing:** Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Testing Combinations of Inputs, State Transition Testing Model Generator, or Decision Table Testing.
* **White-box Dynamic Testing:** Measuring statement coverage, branch coverage, condition coverage, path coverage, d-u coverage, etc.

### Tool Functionality
The tool must be implemented to take one of two forms of input:
1.  **System Requirements:** Analyzing requirements to create test cases.
2.  **Testing Codebase:** Analyzing existing code (or a partial module) to create test cases or identify issues.

---

## 2. Submission Artifacts
Each group must submit the following:

### A. Core Artifact Content
* **Input:** Requirement document or project codebase.
* **Tool Artifact:** Specific prompts used, the model used (e.g., GPT-4o), and any model-generated code.
* **Generated Output:** * Reported alarms (for static analysis).
    * Test cases (for black-box and white-box analysis).
* **Experimental Analysis:** Evaluation of Accuracy, Coverage, Generalizability, etc.
* **Project Report:** * Comparison to traditional non-AI-based techniques (pros and cons).
    * **Analytical Report:** Documentation of AI limitations encountered and how the tool was improved during practice.
    * Summary.

### B. Assessment Criteria
| Criteria | Weight |
| :--- | :--- |
| Understanding of concepts | 10% |
| Coherence of design and implementation | 20% |
| Coverage and effectiveness/usefulness | 40% |
| In-depth analysis (generalizability, reasoning) | 20% |
| Presentation | 10% |

---

## 3. Presentation & Submission Process

### Presentation
* **Duration:** 15 minutes per group (in English).
* **Format:** Presentation followed by a Q&A session.
* **Scope:** Must cover all aspects listed in the requirements.
* **Peer Contribution:** Default is equal allocation unless a deviation is signed by all members.

### Submission Instructions
Submit the following via email to the TA **one day before** the presentation date:
1.  **Submission Artifact (PDF):** Must include a cover page with Team ID, full names, and student IDs.
2.  **Final Presentation (PDF):** PPT converted to PDF; first slide must include Team ID and member details.
3.  **Test Scripts:** Submitted as a **compressed file (.zip/ .rar)**.

**Deadlines:**
* **Submission:** Week 8, Monday, before 17:00 pm.
* **Presentation:** Week 8–9, Tuesday/Thursday, 10:00–11:35.

---

## 4. Examples of Submission Structures

### Example 1: LLM-based Dynamic Black-box Testing
* **Title:** LLM-based Dynamic Black-box Testing for Multi-Item Smart Vending Machine.
* **Input:** Functional requirements (Item selection, Payment methods, Constraints, Inventory).
* **Prompt Example:** *"You are a software testing assistant. Given the following requirement, identify: 1) Input variables 2) Equivalence partitions... {requirement_text}"*
* **Analysis Focus:** Coverage of EP/BVA and refining prompts for accuracy.

### Example 2: LLM-based Static Analysis
* **Title:** LLM-based Static Analysis for OpenHarmony Axios.
* **Input:** Source code of the library.
* **Prompt Example:** *"You are a static code analyzer. Detect potential issues (syntax, security, quality) and return structured JSON..."*
* **Analysis Focus:** False alarm analysis and bug validation.

### Example 3: LLM-based White-box Testing
* **Title:** LLM-based White-box Testing for Statement Coverage.
* **Input:** Code snippets/functions.
* **Prompt Example:** *"Analyze the following function and generate test cases that achieve full statement coverage. Output in JSON format..."*
* **Analysis Focus:** Identifying unreachable code and improving generalizability.