# worktree-cleanup

Run the read-only scripts/worktree_audit.py <repository> to list paths, branches, and dirty state. Consider active user tasks and unpushed commits; merged status is only one signal. Report exact deletion candidates and reasons to keep others. Obtain authorization for the specific deletion set, then recheck state before acting. Inspect simulators only when the relevant platform tools exist. The audit tool never deletes a directory.
