// Entry point for the news-image-20261125 entry.
//
// The poster is drawn ahead of time by draw_poster.py and shipped in this
// repository as entry.png. This program only copies that exact file to
// the grader's output directory, so both runs write identical bytes.
// Standard library only, no network.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
