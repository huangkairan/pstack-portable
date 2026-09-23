# Benny external integration boundary

The upstream `setup-benny`, `triage-issue-reports`, and `reproduce-and-fix-issues` skills remain in `vendor`; they are not registered as everyday commands. A host skill adapter alone cannot run them as a service.

A real integration needs an event source, trusted user identity, thread routing, a deduplication key, an issue tracker, test-environment credentials, and a UI control interface. The control interface must support launch, environment checks, navigation, interaction, state observation, evidence capture, and cleanup. It must support repeated verification of the same issue. Enforce permissions with actual tool configuration.

One processing attempt receives an event and a fixed thread coordinate, validates identity and authorization, looks up a deduplication record, triages, reproduces, makes the smallest fix, verifies the real behavior, and records artifacts. Reply in the original thread or open a draft PR only when authorized. A repeated event returns the existing record without repeating external writes. Do not merge or deploy.

This package connects to no Slack, tracker, or control environment. Its status is `BLOCKED_EXTERNAL_INTEGRATION`; no interface or production service is simulated.
