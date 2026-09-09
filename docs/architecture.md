AI Receptionist — V1 System Architecture

1. Architecture Overview

The AI Receptionist will use a modular architecture that separates conversation intelligence from business logic and external integrations.

The language model will interpret customer requests and determine which approved application tools should be used.

The language model will not directly access Google Calendar, customer databases, phone systems, or other external services.

Application code will validate and execute all external actions.

2. High-Level System

The complete production system is expected to eventually follow this flow:

Customer Phone Call
        |
        v
Telephony Provider
        |
        v
Voice Layer
Speech-to-Text / Text-to-Speech
        |
        v
Conversation Agent
        |
        v
Tool Layer
        |
        +--------------------+
        |                    |
        v                    v
Scheduling Service      Business Knowledge
        |                    |
        v                    v
Google Calendar        Approved Business Data

Version 1 development will initially replace the telephone and voice portions with a local text interface.

Initial development flow:

Terminal User
     |
     v
Conversation Agent
     |
     v
Tool Layer
     |
     +--------------------+
     |                    |
     v                    v
Local/Test Scheduler   Business Knowledge

After the agent and scheduling behavior are reliable, the local scheduler will be replaced with Google Calendar.

3. Major Components

3.1 Conversation Interface

The first interface will be a terminal-based text application.

Responsibilities:

* Receive customer messages.
* Display agent responses.
* Maintain the active conversation.
* Pass user input to the agent.

This interface will later be replaced or supplemented by the voice and telephony layers.

3.2 Conversation Agent

The conversation agent is responsible for understanding customer requests and managing the interaction.

Responsibilities include:

* Identify customer intent.
* Determine what information is missing.
* Ask appropriate follow-up questions.
* Maintain conversational context.
* Decide when an approved tool should be called.
* Interpret tool results.
* Explain results to the customer.
* Determine when human escalation is required.

The agent must not directly modify external systems.

3.3 Conversation State

The application should maintain structured state separately from conversational text.

Example state:

customer_name
phone_number
property_address
project_type
project_scope
preferred_date
preferred_time
appointment_id
additional_notes
current_intent

Structured state will make tool execution more predictable and reduce reliance on the model remembering every important detail from raw conversation history.

3.4 Tool Layer

The tool layer exposes narrowly defined capabilities to the agent.

Initial planned tools include:

check_availability()
book_estimate()
find_appointment()
reschedule_estimate()
cancel_estimate()
get_business_information()
request_human_handoff()

Each tool will:

1. Accept structured input.
2. Validate that input.
3. Execute application logic.
4. Return a structured result.
5. Report errors without pretending the operation succeeded.

The agent will only have access to explicitly approved tools.

4. Scheduling Service

Scheduling logic will be separated from the agent.

Responsibilities:

* Enforce business hours.
* Enforce appointment duration.
* Enforce travel buffer time.
* Prevent same-day appointments.
* Enforce the 30-day booking window.
* Detect scheduling conflicts.
* Return available appointment times.
* Create appointments.
* Reschedule appointments.
* Cancel appointments.

The scheduling service will define a stable interface so the scheduling backend can change without rewriting the conversation agent.

Example:

Agent
  |
  v
Scheduling Service
  |
  +---- Test Scheduler
  |
  +---- Google Calendar Adapter

During early development, a local test scheduler can be used.

Google Calendar will later become the production scheduling backend.

5. Google Calendar Adapter

The Google Calendar integration will be isolated in its own module.

Responsibilities:

* Authenticate with Google Calendar.
* Read calendar availability.
* Create estimate events.
* Find existing appointment events.
* Modify appointment events.
* Delete or cancel appointment events.
* Translate Google API errors into application-level errors.

The agent will never receive Google credentials.

Credentials will remain inside the application environment.

6. Business Knowledge Service

Business information should come from an approved source rather than the model’s general knowledge.

Initial information may include:

* Business name
* Business hours
* Service area
* Interior painting services
* Exterior painting services
* Estimate process
* Scheduling policies
* Cancellation policies
* Contact information

For the first implementation, this information may be stored in a structured configuration file.

Example:

config/business.json

If business information becomes significantly larger, the project may later use retrieval-augmented generation.

RAG is not required for the initial version.

7. Validation Layer

Important actions must be validated by application code.

Examples:

* Required customer information is present.
* Phone number has a valid format.
* Appointment date is not in the past.
* Appointment is not same-day.
* Appointment is within the 30-day window.
* Appointment occurs during business hours.
* The requested time is actually available.
* Required confirmation has been obtained before booking.

The language model should not be treated as the authority for validation.

8. Model Provider Abstraction

The application should avoid tightly coupling all business logic to one language model provider.

The agent layer should eventually expose a simple interface such as:

generate_response()

This makes it easier to test different model providers or local models later without rewriting the scheduling and business logic.

Initial development may use one provider while preserving this separation.

9. Configuration

Application configuration should be kept separate from source code.

Potential configuration includes:

Business hours
Appointment duration
Travel buffer
Maximum booking window
Business information
Model settings
Calendar ID
Environment settings

Non-sensitive configuration may be stored in the config/ directory.

Secrets must not be committed to GitHub.

Secrets may include:

* API keys
* Google credentials
* Telephony credentials
* Database passwords

Secrets should eventually be loaded through environment variables or an approved secrets-management system.

10. Logging

The application should log important system events.

Examples:

Agent started
Tool requested
Tool validation failed
Calendar availability checked
Appointment created
Appointment rescheduled
Appointment cancelled
External API error
Human escalation requested

Logs should avoid unnecessarily storing sensitive customer information.

Logging will be important for debugging conversations where the agent behaves incorrectly.

11. Error Handling

External operations may fail.

Examples include:

* Google Calendar unavailable
* Authentication failure
* Network error
* Appointment becomes unavailable before booking
* Invalid tool arguments
* Model provider error

The application should detect these failures and return controlled errors.

The agent should never represent a failed operation as successful.

Example:

Calendar API failure
        |
        v
Scheduling Service reports failure
        |
        v
Agent tells customer the appointment could not be completed
        |
        v
Human follow-up may be offered

12. Human Handoff

Human escalation will initially be represented as an application state or tool result.

Example:

request_human_handoff(reason)

Later, when telephony is implemented, this may:

* Transfer the active call.
* Route the caller to voicemail.
* Create a callback request.
* Notify a staff member.

The conversation agent should not attempt to solve problems outside its approved scope when escalation is more appropriate.

13. Voice Layer

Voice support will be added after the text agent is reliable.

The voice layer will handle:

* Speech-to-text.
* Text-to-speech.
* Caller interruptions.
* Silence detection.
* Audio streaming.
* Conversation latency.

The voice layer should communicate with the same conversation agent used by the text prototype.

This prevents the business logic from depending on whether the customer is typing or speaking.

14. Telephony Layer

The telephony layer will eventually connect the application to a real telephone number.

Responsibilities may include:

* Receive inbound calls.
* Stream call audio.
* Send synthesized speech.
* Transfer calls.
* Detect call termination.
* Provide caller metadata when permitted.

A telephony provider will be selected later.

15. Proposed Source Structure

The project may evolve toward a structure similar to:

ai-receptionist/
|
├── README.md
├── config/
│   └── business.json
|
├── docs/
│   ├── requirements.md
│   ├── architecture.md
│   ├── development-log.md
│   ├── integrations.md
│   └── testing.md
|
├── src/
│   ├── __init__.py
│   ├── main.py
│   |
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── receptionist.py
│   │   ├── state.py
│   │   └── prompts.py
│   |
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── scheduling.py
│   │   ├── business_info.py
│   │   └── handoff.py
│   |
│   ├── scheduling/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   ├── test_scheduler.py
│   │   └── google_calendar.py
│   |
│   ├── knowledge/
│   │   ├── __init__.py
│   │   └── service.py
│   |
│   └── utils/
│       ├── __init__.py
│       ├── validation.py
│       └── logging.py
|
└── tests/
    ├── test_scheduling.py
    ├── test_validation.py
    └── test_agent_tools.py

This structure may change as development progresses.

Architectural changes should be documented rather than treated as fixed assumptions.

16. Key Architectural Principles

The project will follow these principles:

1. The AI interprets requests but does not directly control external systems.
2. Important actions are executed through narrowly scoped tools.
3. Application code validates tool requests.
4. Conversation state should be represented structurally where possible.
5. Scheduling logic should remain separate from Google Calendar-specific code.
6. Business knowledge should come from approved sources.
7. Secrets must never be committed to GitHub.
8. Failed operations must never be reported as successful.
9. Human escalation should always remain available.
10. Voice and telephony should be interfaces around the same core agent rather than separate implementations.
11. Components should remain modular enough to support different businesses and providers later.
12. Architecture documentation should evolve with the implementation.
