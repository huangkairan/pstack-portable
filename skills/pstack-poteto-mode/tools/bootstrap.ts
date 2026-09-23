import { existsSync } from "node:fs";
import { join } from "node:path";

export function ensureDependenciesInstalled(): void {
  if (!existsSync(join(import.meta.dir, "node_modules", "commander", "package.json"))) {
    throw new Error(`Dependencies are missing. Run bun install --frozen-lockfile in ${import.meta.dir} first. Tools do not install packages over the network automatically.`);
  }
}
