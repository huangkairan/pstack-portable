# poteto-mode

1. Read references/playbooks/index.md and select one playbook that matches the current task. Complete small tasks directly; a function change alone does not trigger a design competition.
2. Read the selected playbook and state task-specific completion criteria. Read only the relevant principles from references/principles.md when a design or verification question calls for them.
3. Workflows are in references/workflows/ and may be read directly. They do not require another installed skill. A leaf workflow must not call this router again.
4. Choose local execution or native delegation by task complexity. Inherit the host model and start with at most two parallel workers. Increase this only when current authorization and budget warrant it.
5. Report artifacts, actual verification, and unfinished work. This entry applies only to the current task. It does not change global instructions or automatically send messages, open PRs, merge, or deploy.

Common routes: understanding a system -> how; fixing a bug -> bug-fix playbook; new behavior -> feature; structural design -> architect; change impact -> blast-radius; project verification -> create-verification-skill.
