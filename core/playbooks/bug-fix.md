# bug-fix

Reproduce the defect on the same UI or CLI path reported by the user and preserve failing evidence. Trace the smallest call chain to the root cause. If an inexpensive regression check exists, follow workflows/tdd.md. After the fix, rerun the original scenario and related regressions. A passing unit test alone does not prove a UI defect is gone. Mark the original scenario unverified when it cannot be accessed.
