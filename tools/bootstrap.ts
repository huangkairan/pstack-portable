import { existsSync } from "node:fs";
import { join } from "node:path";

export function ensureDependenciesInstalled(): void {
  if (!existsSync(join(import.meta.dir, "node_modules", "commander", "package.json"))) {
    throw new Error(`缺少依赖。先在 ${import.meta.dir} 执行 bun install --frozen-lockfile；工具不会自动联网安装。`);
  }
}
