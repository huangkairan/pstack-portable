# typescript-best-practices

1. Read the project's tsconfig, conventions, and target code. Reuse existing types and libraries.
2. Validate and narrow external input, then rely on trusted internal types. Use discriminated unions for mutually exclusive states; avoid unconstrained any, assertions that hide errors, and unnecessary optional fields.
3. Make public signatures express their real contracts while leaving module internals replaceable. Do not add complex generics for a few similar statements.
4. Run existing type checks and relevant behavioral checks. Compilation and runtime correctness are different claims. Update callers with type changes.
