import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Meme Sprint entry: render entry.png (1024x1024, <=1 MiB) into the
// grader's output directory. The image is drawn by render.py with PIL
// (shapes + text only, no network, no models). Deterministic.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const here = dirname(fileURLToPath(import.meta.url));

mkdirSync(outDir, { recursive: true });
execFileSync("python3", [join(here, "render.py"), join(outDir, "entry.png")], {
  stdio: "inherit",
});

const out = join(outDir, "entry.png");
if (!existsSync(out)) {
  console.error("entry.png was not produced");
  process.exit(1);
}
console.log("wrote", out);
