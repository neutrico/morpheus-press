# Copilot + Automation Workflow Diagrams

## Complete End-to-End Flow

```mermaid
flowchart TB
    Start([Planning System]) --> CreateIssue[Create GitHub Issue]
    
    CreateIssue --> TriggerChoice{Trigger Automation?}
    
    TriggerChoice -->|Assign to @copilot| AutoTrigger[GitHub Actions Triggered]
    TriggerChoice -->|Comment /automate| AutoTrigger
    TriggerChoice -->|Add label automation:ready| AutoTrigger
    TriggerChoice -->|Manual| Manual[Manual CLI Generation]
    
    AutoTrigger --> ExtractKey[Extract Task Key T24]
    ExtractKey --> CheckAI{Check AI Effectiveness}
    
    CheckAI -->|HIGH| RunGen[Run task-automation-agent.py]
    CheckAI -->|MEDIUM/LOW| Comment[Comment: Manual Implementation Required]
    
    RunGen --> Generate[Generate Code via Claude]
    Generate --> CreateBranch[Create Branch: automation/T24-TIMESTAMP]
    CreateBranch --> CommitFiles[Commit Generated Files]
    CommitFiles --> CreatePR[Create PR AUTO-GENERATED]
    CreatePR --> AssignCopilot[Assign PR to @copilot]
    
    AssignCopilot --> CopilotReview[Copilot Reviews PR]
    CopilotReview --> ReadSpec[Read planning/docs/ Spec]
    ReadSpec --> FindTODO[Search for TODO Comments]
    FindTODO --> Implement[Implement Business Logic]
    Implement --> RunTests[Run Tests]
    RunTests --> Push[Push Fixes to PR]
    
    Push --> HumanReview{Human Review}
    HumanReview -->|Needs Changes| FindTODO
    HumanReview -->|Approved| Merge[Merge PR]
    
    Merge --> CloseIssue[Auto-Close Issue]
    CloseIssue --> End([Complete])
    
    Manual --> LocalGen[python task-automation-agent.py T24]
    LocalGen --> ManualCommit[Manual Commit]
    ManualCommit --> ManualPR[Manual PR]
    ManualPR --> HumanReview
    
    Comment --> ManualImpl[Human Implements Manually]
    ManualImpl --> ManualCommit
    
    style Start fill:#e1f5ff
    style AutoTrigger fill:#ffeaa7
    style Generate fill:#55efc4
    style CopilotReview fill:#a29bfe
    style Merge fill:#00b894
    style End fill:#00cec9
```

## GitHub Actions Workflow Detail

```mermaid
sequenceDiagram
    actor User
    participant GitHub Issues
    participant GitHub Actions
    participant Automation Agent
    participant Anthropic Claude
    participant GitHub PRs
    actor Copilot
    
    User->>GitHub Issues: Create Issue / Assign @copilot
    GitHub Issues->>GitHub Actions: Webhook: issues.assigned
    
    GitHub Actions->>GitHub Actions: Extract Task Key (T24)
    GitHub Actions->>GitHub Actions: Check AI Effectiveness (effort-map.yaml)
    
    alt HIGH AI Effectiveness
        GitHub Actions->>Automation Agent: Run task-automation-agent.py T24
        Automation Agent->>Automation Agent: Load Specs (planning/docs/)
        Automation Agent->>Anthropic Claude: Generate Code (prompt + specs)
        Anthropic Claude-->>Automation Agent: Generated Code (JSON)
        Automation Agent->>Automation Agent: Write Files to Disk
        Automation Agent->>GitHub Actions: Exit 0 (success)
        
        GitHub Actions->>GitHub Actions: Create Branch (automation/T24-...)
        GitHub Actions->>GitHub Actions: Commit Files
        GitHub Actions->>GitHub PRs: Create PR [AUTO-GENERATED]
        GitHub PRs->>Copilot: Assign PR
        GitHub Actions->>GitHub Issues: Comment with PR Link
        
        Copilot->>GitHub PRs: Review PR
        Copilot->>Copilot: Read .github/copilot-instructions.md
        Copilot->>GitHub PRs: Fix TODOs + Refine Code
        Copilot->>GitHub PRs: Push Fixes
        
        GitHub PRs->>User: Notify: PR Ready for Review
        User->>GitHub PRs: Approve + Merge
    else MEDIUM/LOW AI
        GitHub Actions->>GitHub Issues: Comment: Manual Implementation Required
        GitHub Issues->>User: Notify
        User->>User: Manual Implementation
    end
```

## Copilot Agent Decision Flow

```mermaid
flowchart TD
    Start([Copilot Receives Task]) --> ReadInstructions[Read .github/copilot-instructions.md]
    
    ReadInstructions --> CheckPR{Check for Auto-Generated PR?}
    
    CheckPR -->|Found| ReviewPR[Review PR Code]
    CheckPR -->|Not Found| CheckTrigger{Can Trigger Automation?}
    
    CheckTrigger -->|YES HIGH AI| Comment[Comment /automate]
    Comment --> Wait[Wait for PR]
    Wait --> ReviewPR
    
    CheckTrigger -->|NO| Manual[Manual Implementation]
    
    ReviewPR --> ReadSpec[Read planning/docs/ + issues/*.yaml]
    ReadSpec --> SearchTODO[Search for TODO Comments]
    
    SearchTODO --> ImplementLogic[Implement Business Logic]
    ImplementLogic --> VerifySchema[Verify Zod Schemas]
    VerifySchema --> AddTests[Add/Fix Tests]
    AddTests --> RunTests[Run Tests: pnpm test]
    
    RunTests --> TestPass{Tests Pass?}
    TestPass -->|NO| Debug[Debug Failures]
    Debug --> ImplementLogic
    TestPass -->|YES| CheckError[Check Error Handling]
    
    CheckError --> AddLogging[Add Logging]
    AddLogging --> TypeCheck[Type Check: pnpm type-check]
    
    TypeCheck --> TypePass{Types Valid?}
    TypePass -->|NO| FixTypes[Fix Type Errors]
    FixTypes --> TypeCheck
    TypePass -->|YES| Push[Push to PR Branch]
    
    Push --> Notify[Notify: Ready for Human Review]
    Notify --> End([Wait for Approval])
    
    Manual --> ReadSpec
    
    style Start fill:#e1f5ff
    style CheckPR fill:#ffeaa7
    style ReviewPR fill:#55efc4
    style RunTests fill:#a29bfe
    style Push fill:#00b894
    style End fill:#00cec9
```

## Task Pattern Recognition

```mermaid
flowchart LR
    Task[Task Specification] --> Analyze{Analyze Pattern}
    
    Analyze -->|Database Keywords| DB[Database Setup]
    Analyze -->|Testing Keywords| Test[Testing]
    Analyze -->|API Keywords| API[API Routes]
    Analyze -->|Docs Keywords| Docs[Documentation]
    Analyze -->|UI Keywords| UI[Component]
    Analyze -->|Unknown| Generic[Generic Code]
    
    DB --> DBGen[setup-supabase.sh]
    Test --> TestGen[setup-tests.sh]
    API --> APIGen[api-generator.py]
    Docs --> DocsGen[docs-generator.py]
    UI --> UIGen[component-generator.py]
    Generic --> LLMGen[task-automation-agent.py LLM]
    
    DBGen --> Output[Generated Files]
    TestGen --> Output
    APIGen --> Output
    DocsGen --> Output
    UIGen --> Output
    LLMGen --> Output
    
    Output --> Review[Human/Copilot Review]
    
    style Task fill:#e1f5ff
    style Analyze fill:#ffeaa7
    style Output fill:#55efc4
    style Review fill:#a29bfe
```

## Data Flow

```mermaid
flowchart TB
    subgraph Planning Layer
        PlanDocs[planning/docs/\n*.md]
        PlanIssues[planning/issues/\n*.yaml]
        EffortMap[planning/estimates/\neffort-map.yaml]
    end
    
    subgraph Automation Layer
        IssueCreator[create-github-issues.py]
        TaskAgent[task-automation-agent.py]
        CLIGen[CLI Generators]
    end
    
    subgraph GitHub Layer
        Issues[GitHub Issues]
        Actions[GitHub Actions]
        PRs[GitHub PRs]
    end
    
    subgraph Agent Layer
        Copilot[Copilot Agent]
        Instructions[.github/copilot-instructions.md]
    end
    
    subgraph Output Layer
        Code[Generated Code]
        Tests[Test Suites]
        Migrations[DB Migrations]
    end
    
    PlanDocs --> IssueCreator
    PlanIssues --> IssueCreator
    EffortMap --> IssueCreator
    
    IssueCreator --> Issues
    
    Issues --> Actions
    Actions --> TaskAgent
    
    PlanDocs --> TaskAgent
    PlanIssues --> TaskAgent
    EffortMap --> TaskAgent
    
    TaskAgent --> Code
    TaskAgent --> Tests
    TaskAgent --> Migrations
    
    CLIGen --> Code
    CLIGen --> Tests
    CLIGen --> Migrations
    
    Code --> PRs
    Tests --> PRs
    Migrations --> PRs
    
    PRs --> Copilot
    Instructions --> Copilot
    
    Copilot --> Code
    Copilot --> Tests
    
    style PlanDocs fill:#e1f5ff
    style TaskAgent fill:#ffeaa7
    style Actions fill:#55efc4
    style Copilot fill:#a29bfe
    style Code fill:#00b894
```

## Cost-Benefit Analysis Flow

```mermaid
flowchart LR
    subgraph Input
        Task[Task: T24\n2 days estimated]
    end
    
    subgraph Without Automation
        ManualTime[Manual Work:\n16 hours]
        ManualCost[Cost: 16h × $75/h\n= $1,200]
    end
    
    subgraph With Automation
        GenTime[Generation:\n30 min]
        CopilotTime[Copilot Review:\n2 hours]
        HumanTime[Human Review:\n1.5 hours]
        
        TotalTime[Total: 4 hours]
        
        LLMCost[LLM Cost:\n$0.15]
        DevCost[Dev Cost: 4h × $75/h\n= $300]
        
        TotalCost[Total: $300.15]
    end
    
    subgraph Savings
        TimeSaved[Time Saved:\n12 hours 75%]
        CostSaved[Cost Saved:\n$899.85 75%]
        ROI[ROI:\n599,900%]
    end
    
    Task --> ManualTime
    Task --> GenTime
    
    ManualTime --> ManualCost
    
    GenTime --> TotalTime
    CopilotTime --> TotalTime
    HumanTime --> TotalTime
    
    TotalTime --> DevCost
    LLMCost --> TotalCost
    DevCost --> TotalCost
    
    ManualCost --> CostSaved
    TotalCost --> CostSaved
    
    ManualTime --> TimeSaved
    TotalTime --> TimeSaved
    
    CostSaved --> ROI
    
    style Task fill:#e1f5ff
    style ManualCost fill:#ff7675
    style TotalCost fill:#00b894
    style ROI fill:#00cec9
```

## State Machine: PR Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft: Auto-Generated
    
    Draft --> InReview: Copilot Assigned
    InReview --> FixingTODOs: Found TODOs
    FixingTODOs --> Testing: TODO Fixed
    Testing --> Failed: Tests Fail
    Failed --> FixingTODOs: Debug
    Testing --> TypeChecking: Tests Pass
    TypeChecking --> TypeErrors: Errors Found
    TypeErrors --> FixingTODOs: Fix Types
    TypeChecking --> ReadyForReview: All Checks Pass
    
    ReadyForReview --> HumanReview: Notify Human
    HumanReview --> ChangesRequested: Issues Found
    ChangesRequested --> FixingTODOs: Copilot Fixes
    HumanReview --> Approved: LGTM
    
    Approved --> Merged: Merge PR
    Merged --> [*]: Issue Closed
    
    note right of Draft
        Files created by
        task-automation-agent.py
    end note
    
    note right of FixingTODOs
        Copilot implements
        business logic based
        on planning/docs/ specs
    end note
    
    note right of Testing
        pnpm test
        Check coverage
        Verify mocks
    end note
    
    note right of Approved
        Human verifies:
        - Tests pass
        - Types valid
        - Logic correct
        - Docs updated
    end note
```

## Architecture Layers

```mermaid
graph TB
    subgraph Layer 1: Planning
        A1[YAML Specs]
        A2[Markdown Docs]
        A3[AI Effectiveness]
    end
    
    subgraph Layer 2: Automation
        B1[GitHub Actions]
        B2[Task Automation Agent]
        B3[CLI Generators]
    end
    
    subgraph Layer 3: Code Generation
        C1[Anthropic Claude API]
        C2[Template Engine]
        C3[File Writer]
    end
    
    subgraph Layer 4: Quality Assurance
        D1[Copilot Agent]
        D2[Unit Tests]
        D3[Type Checking]
    end
    
    subgraph Layer 5: Review & Deploy
        E1[Human Review]
        E2[CI/CD]
        E3[Production]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B2
    
    B1 --> C1
    B2 --> C1
    B3 --> C2
    
    C1 --> C3
    C2 --> C3
    
    C3 --> D1
    C3 --> D2
    
    D1 --> E1
    D2 --> E2
    D3 --> E2
    
    E1 --> E3
    E2 --> E3
    
    style A1 fill:#e1f5ff
    style B1 fill:#ffeaa7
    style C1 fill:#55efc4
    style D1 fill:#a29bfe
    style E1 fill:#00b894
```

---

**Visual Reference**: Use these diagrams to understand the complete automation workflow.

**Tools**: Render these with any Mermaid-compatible tool (GitHub, VS Code, online viewers).

**Version**: 1.0.0

**Last Updated**: 2026-02-08
