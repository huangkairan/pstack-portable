# make-bot-ui

1. Check whether the target platform actually provides state updates, messaging, an accessible UI, and user/thread identity. The original GrokBot and Tailscale interfaces are not portable capabilities.
2. When interfaces exist, separate UI state from external effects. Define inputs, state, actions, errors, and retries. Use only interfaces that exist and are authorized for the task.
3. Verify initial load, state transitions, failures, and recovery through user scenarios. Check isolation between users and threads.
4. If interfaces are missing, provide an explicit adapter contract and BLOCKED status. Build a local prototype when requested, but do not claim that the bot integration works.
