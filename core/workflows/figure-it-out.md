# figure-it-out

1. Define falsifiable completion criteria, scope, baseline, size, and major unknowns. Find existing checks before choosing the smallest additional verification tool.
2. Split work into deliverable units that each end in an observation. State dependencies and rollback points. Read the architect workflow only for structural decisions.
3. For every iteration, record the hypothesis, change, observed result, and reason to keep or revert it. Repeated failure calls for revisiting the shared premise, not accumulating patches.
4. For multi-round work, save a checkpoint and decision log with the current revision, evidence paths, unfinished work, and next action. This workflow does not provide durable wake-up.
5. Recheck each unit and then verify the whole outcome against the real target. Report VERIFIED, NOT_VERIFIED, INCONCLUSIVE, or BLOCKED with evidence. Completing the plan is not itself proof of the goal.
