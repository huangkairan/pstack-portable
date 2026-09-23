# swarm

1. Choose a coverage matrix, mutually exclusive exploration slices, a race, or staged elimination. Define each slice's boundary, completion criterion, and synthesis method. Use arena for design or code synthesis competitions.
2. Start with two workers and increase only when the budget warrants it. Each brief states the goal, base revision, allowed write paths, evidence, time limit, and report path. Restrict read-only investigations to read tools.
3. Start native subagents with non-overlapping write paths. If workers must change a shared file, let the parent integrate their results serially.
4. Wait for and inspect artifacts. In a race, cancel other workers after a winner emerges and confirm their status. Keep failures, timeouts, and unknown outcomes visible in the matrix rather than merging them into success.
5. Report coverage, evidence, overlapping findings, gaps, and conclusions. Do not declare the whole task complete while a required slice remains uncovered.
