# TypeScript rules

- Use discriminated unions for variants. Brand primitives when mixing them would be dangerous, and construct branded values only after boundary validation.
- Express non-empty, paired, and range invariants structurally when needed. Keep ordinary arrays when all operations on them remain total.
- Treat external input as unknown. Reuse the project's schema library and derive types from its schemas.
- Narrow with discriminants first, then `in`, `typeof` or `instanceof`, and truthful type guards. An assertion cannot replace validation.
- Check exhaustive branches with `never`. Prefer `satisfies` when literal types must remain narrow. Derive existing contracts with `Pick`, `Omit`, `ReturnType`, and similar utilities.
- Parse inputs into domain types at boundaries and trust those types internally. Do not pass unbounded dictionaries through every layer.
- Object parameters can clarify public multi-argument APIs; account for the project's performance constraints on hot paths.
- Run behavioral tests against real code and use the project's structured logging. A type check does not prove the UI works.
