# GitHub Issue GraphQL API - Field Reference

> Complete list of fields available on the `Issue` type in GitHub GraphQL API v4

Generated: 2026-02-09

## Overview

The `Issue` type represents a GitHub issue. This document lists all available fields you can query via GraphQL.

## Key Fields

### Basic Information
- **id**: The Node ID of the Issue object (`NON_NULL ID`)
- **number**: Identifies the issue number (`NON_NULL Int`)
- **title**: Identifies the issue title (`NON_NULL String`)
- **titleHTML**: Identifies the issue title rendered to HTML (`NON_NULL String`)
- **body**: Identifies the body of the issue (`NON_NULL String`)
- **bodyHTML**: The body rendered to HTML (`NON_NULL HTML`)
- **bodyText**: Identifies the body of the issue rendered to text (`NON_NULL String`)

### Status & State
- **state**: Identifies the state of the issue (OPEN/CLOSED) (`NON_NULL IssueState`)
- **stateReason**: Identifies the reason for the issue state (`IssueStateReason`)
- **closed**: Indicates if the object is closed (`NON_NULL Boolean`)
- **closedAt**: Identifies the date and time when the object was closed (`DateTime`)

### Metadata
- **issueType**: The issue type for this Issue (Bug/Feature/Task) (`IssueType`)
- **labels**: A list of labels associated with the object (`LabelConnection`)
- **milestone**: Identifies the milestone associated with the issue (`Milestone`)
- **repository**: The repository associated with this node (`NON_NULL Repository`)

### Timestamps
- **createdAt**: Identifies the date and time when the object was created (`NON_NULL DateTime`)
- **updatedAt**: Identifies the date and time when the object was last updated (`NON_NULL DateTime`)
- **closedAt**: Identifies the date and time when the object was closed (`DateTime`)
- **publishedAt**: Identifies when the comment was published at (`DateTime`)
- **lastEditedAt**: The moment the editor made the last edit (`DateTime`)

### Assignments
- **assignees**: A list of Users assigned to this object (`NON_NULL UserConnection`)
- **assignedActors**: A list of actors assigned to this object (`NON_NULL AssigneeConnection`)
- **suggestedActors**: A list of suggested actors to assign to this object (`NON_NULL AssigneeConnection`)

### Relationships
- **parent**: The parent entity of the issue (`Issue`)
- **subIssues**: A list of sub-issues associated with the Issue (`NON_NULL IssueConnection`)
- **subIssuesSummary**: Summary of the state of an issue's sub-issues (`NON_NULL SubIssuesSummary`)
- **blockedBy**: A list of issues that are blocking this issue (`NON_NULL IssueConnection`)
- **blocking**: A list of issues that this issue is blocking (`NON_NULL IssueConnection`)
- **duplicateOf**: A reference to the original issue that this issue has been marked as a duplicate of (`Issue`)

### Dependencies (Beta)
- **issueDependenciesSummary**: Summary of the state of an issue's dependencies (`NON_NULL IssueDependenciesSummary`)
- **trackedIssues**: A list of issues tracked inside the current issue (`NON_NULL IssueConnection`)
- **trackedInIssues**: A list of issues that track this issue (`NON_NULL IssueConnection`)
- **trackedIssuesCount**: The number of tracked issues for this issue (`NON_NULL Int`)

### Projects v2
- **projectItems**: List of project items associated with this issue (`ProjectV2ItemConnection`)
- **projectV2**: Find a project by number (`ProjectV2`)
- **projectsV2**: A list of projects under the owner (`NON_NULL ProjectV2Connection`)

### Comments & Reactions
- **comments**: A list of comments associated with the Issue (`NON_NULL IssueCommentConnection`)
- **reactions**: A list of Reactions left on the Issue (`NON_NULL ReactionConnection`)
- **reactionGroups**: A list of reactions grouped by content left on the subject (`LIST`)
- **participants**: A list of Users that are participating in the Issue conversation (`NON_NULL UserConnection`)

### Author Information
- **author**: The actor who authored the comment (`Actor`)
- **authorAssociation**: Author's association with the subject of the comment (`NON_NULL CommentAuthorAssociation`)
- **editor**: The actor who edited the comment (`Actor`)

### Links & URLs
- **url**: The HTTP URL for this issue (`NON_NULL URI`)
- **resourcePath**: The HTTP path for this issue (`NON_NULL URI`)
- **bodyUrl**: The http URL for this issue body (`NON_NULL URI`)
- **bodyResourcePath**: The http path for this issue body (`NON_NULL URI`)

### Timeline & History
- **timelineItems**: A list of events, comments, commits, etc. associated with the issue (`NON_NULL IssueTimelineItemsConnection`)
- **userContentEdits**: A list of edits to this content (`UserContentEditConnection`)
- **includesCreatedEdit**: Check if this comment was edited and includes an edit with the creation data (`NON_NULL Boolean`)

### Pull Requests
- **closedByPullRequestsReferences**: List of open pull requests referenced from this issue (`PullRequestConnection`)
- **linkedBranches**: Branches linked to this issue (`NON_NULL LinkedBranchConnection`)

### Locking & Pinning
- **locked**: `true` if the object is locked (`NON_NULL Boolean`)
- **activeLockReason**: Reason that the conversation was locked (`LockReason`)
- **isPinned**: Indicates whether or not this issue is currently pinned to the repository issues list (`Boolean`)

### Viewer Permissions
- **viewerCanClose**: Indicates if the object can be closed by the viewer (`NON_NULL Boolean`)
- **viewerCanReopen**: Indicates if the object can be reopened by the viewer (`NON_NULL Boolean`)
- **viewerCanUpdate**: Check if the current viewer can update this object (`NON_NULL Boolean`)
- **viewerCanDelete**: Check if the current viewer can delete this object (`NON_NULL Boolean`)
- **viewerCanLabel**: Indicates if the viewer can edit labels for this object (`NON_NULL Boolean`)
- **viewerCanReact**: Can user react to this subject (`NON_NULL Boolean`)
- **viewerCanSetFields**: Check if the current viewer can set fields on the issue (`Boolean`)
- **viewerCanSubscribe**: Check if the viewer is able to change their subscription status for the repository (`NON_NULL Boolean`)
- **viewerCannotUpdateReasons**: Reasons why the current viewer can not update this comment (`NON_NULL`)
- **viewerDidAuthor**: Did the viewer author this comment (`NON_NULL Boolean`)

### Subscription Status
- **viewerSubscription**: Identifies if the viewer is watching, not watching, or ignoring the subscribable entity (`SubscriptionState`)
- **viewerThreadSubscriptionFormAction**: Identifies the viewer's thread subscription form action (`ThreadSubscriptionFormAction`)
- **viewerThreadSubscriptionStatus**: Identifies the viewer's thread subscription status (`ThreadSubscriptionState`)
- **isReadByViewer**: Is this issue read by the viewer (`Boolean`)

### Miscellaneous
- **databaseId**: Identifies the primary key from the database (`Int`)
- **fullDatabaseId**: Identifies the primary key from the database as a BigInt (`BigInt`)
- **hovercard**: The hovercard information for this issue (`NON_NULL Hovercard`)
- **createdViaEmail**: Check if this comment was created via an email reply (`NON_NULL Boolean`)

---

## Complete Field List (Alphabetical)

- **activeLockReason**: Reason that the conversation was locked (`LockReason`)
- **assignedActors**: A list of actors assigned to this object (`NON_NULL AssigneeConnection`)
- **assignees**: A list of Users assigned to this object (`NON_NULL UserConnection`)
- **author**: The actor who authored the comment (`Actor`)
- **authorAssociation**: Author's association with the subject of the comment (`NON_NULL CommentAuthorAssociation`)
- **blockedBy**: A list of issues that are blocking this issue (`NON_NULL IssueConnection`)
- **blocking**: A list of issues that this issue is blocking (`NON_NULL IssueConnection`)
- **body**: Identifies the body of the issue (`NON_NULL String`)
- **bodyHTML**: The body rendered to HTML (`NON_NULL HTML`)
- **bodyResourcePath**: The http path for this issue body (`NON_NULL URI`)
- **bodyText**: Identifies the body of the issue rendered to text (`NON_NULL String`)
- **bodyUrl**: The http URL for this issue body (`NON_NULL URI`)
- **closed**: Indicates if the object is closed (definition of closed may depend on type) (`NON_NULL Boolean`)
- **closedAt**: Identifies the date and time when the object was closed (`DateTime`)
- **closedByPullRequestsReferences**: List of open pull requests referenced from this issue (`PullRequestConnection`)
- **comments**: A list of comments associated with the Issue (`NON_NULL IssueCommentConnection`)
- **createdAt**: Identifies the date and time when the object was created (`NON_NULL DateTime`)
- **createdViaEmail**: Check if this comment was created via an email reply (`NON_NULL Boolean`)
- **databaseId**: Identifies the primary key from the database (`Int`)
- **duplicateOf**: A reference to the original issue that this issue has been marked as a duplicate of (`Issue`)
- **editor**: The actor who edited the comment (`Actor`)
- **fullDatabaseId**: Identifies the primary key from the database as a BigInt (`BigInt`)
- **hovercard**: The hovercard information for this issue (`NON_NULL Hovercard`)
- **id**: The Node ID of the Issue object (`NON_NULL ID`)
- **includesCreatedEdit**: Check if this comment was edited and includes an edit with the creation data (`NON_NULL Boolean`)
- **isPinned**: Indicates whether or not this issue is currently pinned to the repository issues list (`Boolean`)
- **isReadByViewer**: Is this issue read by the viewer (`Boolean`)
- **issueDependenciesSummary**: Summary of the state of an issue's dependencies (`NON_NULL IssueDependenciesSummary`)
- **issueType**: The issue type for this Issue (`IssueType`)
- **labels**: A list of labels associated with the object (`LabelConnection`)
- **lastEditedAt**: The moment the editor made the last edit (`DateTime`)
- **linkedBranches**: Branches linked to this issue (`NON_NULL LinkedBranchConnection`)
- **locked**: `true` if the object is locked (`NON_NULL Boolean`)
- **milestone**: Identifies the milestone associated with the issue (`Milestone`)
- **number**: Identifies the issue number (`NON_NULL Int`)
- **parent**: The parent entity of the issue (`Issue`)
- **participants**: A list of Users that are participating in the Issue conversation (`NON_NULL UserConnection`)
- **projectItems**: List of project items associated with this issue (`ProjectV2ItemConnection`)
- **projectV2**: Find a project by number (`ProjectV2`)
- **projectsV2**: A list of projects under the owner (`NON_NULL ProjectV2Connection`)
- **publishedAt**: Identifies when the comment was published at (`DateTime`)
- **reactionGroups**: A list of reactions grouped by content left on the subject (`LIST`)
- **reactions**: A list of Reactions left on the Issue (`NON_NULL ReactionConnection`)
- **repository**: The repository associated with this node (`NON_NULL Repository`)
- **resourcePath**: The HTTP path for this issue (`NON_NULL URI`)
- **state**: Identifies the state of the issue (`NON_NULL IssueState`)
- **stateReason**: Identifies the reason for the issue state (`IssueStateReason`)
- **subIssues**: A list of sub-issues associated with the Issue (`NON_NULL IssueConnection`)
- **subIssuesSummary**: Summary of the state of an issue's sub-issues (`NON_NULL SubIssuesSummary`)
- **suggestedActors**: A list of suggested actors to assign to this object (`NON_NULL AssigneeConnection`)
- **timelineItems**: A list of events, comments, commits, etc. associated with the issue (`NON_NULL IssueTimelineItemsConnection`)
- **title**: Identifies the issue title (`NON_NULL String`)
- **titleHTML**: Identifies the issue title rendered to HTML (`NON_NULL String`)
- **trackedInIssues**: A list of issues that track this issue (`NON_NULL IssueConnection`)
- **trackedIssues**: A list of issues tracked inside the current issue (`NON_NULL IssueConnection`)
- **trackedIssuesCount**: The number of tracked issues for this issue (`NON_NULL Int`)
- **updatedAt**: Identifies the date and time when the object was last updated (`NON_NULL DateTime`)
- **url**: The HTTP URL for this issue (`NON_NULL URI`)
- **userContentEdits**: A list of edits to this content (`UserContentEditConnection`)
- **viewerCanClose**: Indicates if the object can be closed by the viewer (`NON_NULL Boolean`)
- **viewerCanDelete**: Check if the current viewer can delete this object (`NON_NULL Boolean`)
- **viewerCanLabel**: Indicates if the viewer can edit labels for this object (`NON_NULL Boolean`)
- **viewerCanReact**: Can user react to this subject (`NON_NULL Boolean`)
- **viewerCanReopen**: Indicates if the object can be reopened by the viewer (`NON_NULL Boolean`)
- **viewerCanSetFields**: Check if the current viewer can set fields on the issue (`Boolean`)
- **viewerCanSubscribe**: Check if the viewer is able to change their subscription status for the repository (`NON_NULL Boolean`)
- **viewerCanUpdate**: Check if the current viewer can update this object (`NON_NULL Boolean`)
- **viewerCannotUpdateReasons**: Reasons why the current viewer can not update this comment (`NON_NULL`)
- **viewerDidAuthor**: Did the viewer author this comment (`NON_NULL Boolean`)
- **viewerSubscription**: Identifies if the viewer is watching, not watching, or ignoring the subscribable entity (`SubscriptionState`)
- **viewerThreadSubscriptionFormAction**: Identifies the viewer's thread subscription form action (`ThreadSubscriptionFormAction`)
- **viewerThreadSubscriptionStatus**: Identifies the viewer's thread subscription status (`ThreadSubscriptionState`)

---

## Example Query

```graphql
query GetIssue {
  repository(owner: "neutrico", name: "morpheus-press") {
    issue(number: 51) {
      id
      number
      title
      body
      state
      createdAt
      updatedAt
      
      # Native Type
      issueType {
        id
        name
      }
      
      # Milestone
      milestone {
        title
        dueOn
      }
      
      # Labels
      labels(first: 10) {
        nodes {
          name
          color
        }
      }
      
      # Projects v2
      projectItems(first: 5) {
        nodes {
          id
          project {
            title
          }
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
              ... on ProjectV2ItemFieldIterationValue {
                title
                startDate
                duration
              }
            }
          }
        }
      }
      
      # Relationships
      parent {
        number
        title
      }
      
      subIssues(first: 10) {
        nodes {
          number
          title
        }
      }
      
      blockedBy(first: 10) {
        nodes {
          number
          title
        }
      }
    }
  }
}
```

---

## Related Types

- **IssueType**: Bug, Feature, Task (native GitHub feature)
- **IssueState**: OPEN, CLOSED
- **IssueStateReason**: COMPLETED, NOT_PLANNED, REOPENED
- **Milestone**: Sprint/release milestone
- **Label**: Categorization tags
- **ProjectV2**: GitHub Projects (new version)
- **ProjectV2Item**: Issue/PR in a project
- **Actor**: User, Bot, or Organization

---

## Resources

- [GitHub GraphQL API Docs](https://docs.github.com/en/graphql)
- [GraphQL Explorer](https://docs.github.com/en/graphql/overview/explorer) (deprecated Nov 2025)
- [Insomnia GraphQL Client](https://insomnia.rest)
- [GitHub CLI GraphQL](https://cli.github.com/manual/gh_api)

---

**Generated with**: `gh api graphql` + introspection query on `__type(name: "Issue")`
