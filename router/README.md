# OmniDesk-AI Router

The router is a provider-agnostic multi-intent classification and routing layer for OmniDesk-AI. It serves as the conversational front door for organizational knowledge.

It does **NOT** currently require an external LLM or API.

The current baseline classifier runs locally using:
- **TF-IDF** vectorization
- **Logistic Regression** (calibrated classification)
- **scikit-learn**

---

## 1. System Responsibility & Architecture

The router acts purely as a decision and routing engine. It **never** calls RAG retrieval directly and does **not** generate final employee responses.

```
User Query
    ↓
AI Router (router.route_query)
    ↓
Structured RoutingResult
    ↓
Orchestrator
    ↓
for each RouteIntent:
    retrieve(domain=route.domain, query=route.query, top_k=5)
    ↓
Retrieved Context
    ↓
LLM / Gemini Synthesis
    ↓
Final Answer
```

### Capabilities:
1. **Detect single-intent queries.**
2. **Detect and decompose multi-intent queries** into isolated, self-contained sub-queries.
3. **Classify each sub-query** into one of the canonical enterprise domains.
4. **Assign a canonical intent identifier.**
5. **Produce a calibrated confidence score** (0.0 to 1.0).
6. **Detect ambiguity and low confidence.**
7. **Request targeted clarification** when queries are vague, collision-prone, or low confidence.
8. **Return a structured Pydantic `RoutingResult`.**

---

## 2. Supported Domains & Canonical Intents

The router operates across the four official enterprise domains defined in the knowledge base:

| Domain | Scope | Example Canonical Intents |
| :--- | :--- | :--- |
| **IT** | Hardware, remote access, credentials, networks | `vpn`, `password_reset`, `account_unlock`, `mfa_access`, `device_hardware`, `network_wifi`, `lost_stolen_device` |
| **HR** | Leave, benefits, payroll, onboarding, policies | `annual_leave`, `sick_leave`, `parental_family_leave`, `work_from_home`, `benefits_insurance`, `payroll_profile`, `onboarding_offboarding` |
| **Finance** | Expenses, travel booking, reimbursement, corporate cards | `expense_claims`, `hotel_lodging`, `travel_booking_limits`, `receipt_policy`, `corporate_card`, `approval_workflow`, `stipend_reimbursement` |
| **Facilities** | Building badges, office access, room booking, HVAC | `badge_access`, `visitor_access`, `room_desk_booking`, `office_maintenance`, `safety_emergency`, `lost_and_found` |

*All intent identifiers match the canonical taxonomy defined in `router/intent.py`.*

---

## 3. Public Data Contract (Pydantic Schemas)

The routing engine emits strongly-typed Pydantic models defined in `router/schemas.py`.

### `RouteIntent`
Represents an individual routed sub-query:
```python
class RouteIntent(BaseModel):
    domain: str        # "IT" | "HR" | "Finance" | "Facilities"
    intent: str        # e.g. "vpn", "expense_claims"
    query: str         # Decomposed sub-query string
    confidence: float  # Calibrated score between 0.0 and 1.0
```

### `RoutingResult`
The complete payload returned by the router:
```python
class RoutingResult(BaseModel):
    original_query: str
    intents: List[RouteIntent] = []
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    is_out_of_domain: bool = False
    explanation: Optional[str] = None
```

---

## 4. Multi-Intent Routing Example

### Input:
```
"my vpn isnt working and i want my travel reimbursement"
```

### Decomposed Conceptual Routing:
1. **Domain**: `IT`  
   **Intent**: `vpn`  
   **Subquery**: `"my vpn isnt working"`
2. **Domain**: `Finance`  
   **Intent**: `expense_claims`  
   **Subquery**: `"i want my travel reimbursement"`

### Structured JSON Output:
```json
{
  "original_query": "my vpn isnt working and i want my travel reimbursement",
  "intents": [
    {
      "domain": "IT",
      "intent": "vpn",
      "query": "my vpn isnt working",
      "confidence": 0.62
    },
    {
      "domain": "Finance",
      "intent": "expense_claims",
      "query": "i want my travel reimbursement",
      "confidence": 0.66
    }
  ],
  "needs_clarification": false,
  "clarification_question": null,
  "is_out_of_domain": false,
  "explanation": null
}
```
*(Confidence scores reflect model-calibrated outputs from the local baseline classifier).*

---

## 5. Confidence Thresholds & Clarification Policy

Configured in `router/config.py` and evaluated in `router/confidence.py`:

```python
DEFAULT_HIGH_CONFIDENCE_THRESHOLD = 0.65
DEFAULT_CLARIFICATION_THRESHOLD = 0.35
DEFAULT_AMBIGUITY_MARGIN_THRESHOLD = 0.15
DEFAULT_OOD_THRESHOLD = 0.30
```

### Policy Execution Rules:
- **Automatic Routing**: If `confidence >= 0.35` and no ambiguity collisions exist, the query routes automatically to the highest-scoring domain.
- **Low Confidence**: If `top_probability < 0.35`, the engine requests clarification:
  `"Could you please provide more details or specify the relevant department (IT, HR, Finance, Facilities)?"`
- **Ambiguity Detection**:
  - *Pattern-based*: Well-known cross-domain ambiguous queries (e.g., `"Tell me about the policy."` or `"My access isn't working"`) immediately trigger a targeted clarifying question without false routing.
  - *Margin-based*: If the margin between competing top domains is `< 0.08` and `confidence < 0.38`, clarification is triggered.
- **Out-of-Domain (OOD) Protection**: General-knowledge queries (e.g. `"What is the weather in Delhi today?"`) or queries with 0 domain vocabulary overlap return `is_out_of_domain = True`, `intents = []`, preventing false enterprise routing.

---

## 6. Handoff to RAG Orchestration Layer

The router provides clean separation of concerns. The orchestrator consumes `RoutingResult` and dispatches each sub-query to the RAG retrieval function.

The existing RAG module exposes:
```python
from rag import retrieve  # or from rag_mvp.rag import retrieve
# Signature: retrieve(domain: str, query: str, top_k: int = 5) -> list[RetrievedChunk]
```

### Orchestrator Integration Pattern:
```python
from router import route_query
from rag import retrieve  # Existing RAG retrieval interface

def handle_employee_query(user_query: str) -> str:
    # 1. AI Router determines domain(s), intent(s), and sub-queries
    routing_result = route_query(user_query)

    # 2. Check for clarification or out-of-domain
    if routing_result.needs_clarification:
        return routing_result.clarification_question

    if routing_result.is_out_of_domain:
        return "I can only assist with internal IT, HR, Finance, and Facilities questions."

    # 3. Retrieve relevant domain contexts
    contexts = []
    for route in routing_result.intents:
        chunks = retrieve(domain=route.domain, query=route.query, top_k=5)
        contexts.append({
            "domain": route.domain,
            "intent": route.intent,
            "subquery": route.query,
            "chunks": chunks,
        })

    # 4. Pass structured contexts to LLM (e.g., Gemini) for multi-part synthesis
    # return synthesize_response(user_query, contexts)
```

---

## 7. Provider-Agnostic Design & Future Gemini Integration

The router is designed around the `BaseClassifier` abstract base class (`router/classifier.py`):

```
BaseClassifier
      ↑
      |
      +---- BaselineClassifier (Current local scikit-learn model)
      |
      +---- GeminiClassifier   (Future cloud LLM implementation)
```

### How to Integrate Gemini:
To integrate Google Gemini in the future, simply subclass `BaseClassifier`:
1. Implement `classify(query: str) -> ClassificationResult`.
2. Map model predictions to the canonical domains (`IT`, `HR`, `Finance`, `Facilities`).
3. Pass the instance to `Router(classifier=GeminiClassifier())`.

**No changes** will be needed to:
- Multi-intent decomposition logic (`intent.py`)
- Confidence & ambiguity policy (`confidence.py`)
- Pydantic schemas (`schemas.py`)
- FastAPI endpoints (`main.py`)
- Downstream orchestration contract (`RoutingResult`)

---

## 8. Usage & CLI

### CLI Usage:
```bash
# Single query testing
python -m router.cli "my vpn isnt working and i want my travel reimbursement"

# Interactive terminal mode
python -m router.cli
```

### Running the API:
```bash
uvicorn router.main:app --host 0.0.0.0 --port 8000
```
- `POST /route`: Body `{"query": "my vpn isnt working"}` -> returns `RoutingResult`
- `GET /health`: Returns service health and active classifier name.

---

## 9. Evaluation & Testing

### Running Tests:
```bash
# Run full suite (both router and RAG)
python -m pytest

# Run router tests only
python -m pytest router/tests
```

### Running Evaluation Harness:
```bash
python -m router.evaluate
```

> **Evaluation Independence Notice:**  
> The current benchmark is a development sanity check and should not be interpreted as an independent generalization benchmark if training/bootstrap examples overlap with evaluation prompts in `knowledgebase/06_evaluation_dataset_and_rag_notes.md`.
