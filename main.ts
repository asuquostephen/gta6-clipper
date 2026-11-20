// Entry program for the make.fun bounty "gta6-clipper-01" (Clip GTA 6 for
// the most YouTube views), Node 22, standard library only.
//
// The entry is the video itself: VIDEO.json at this repository's root names
// the public YouTube Short, and the house reads the video's views through
// the YouTube Data API. All this program has to do is hand that file to the
// gate: copy VIDEO.json from the repository root into the output directory.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

// The copy is a plain byte-for-byte file copy, so every run of this program
// writes exactly the same bytes: the VIDEO.json this repository ships.
const source = join(botDir, "VIDEO.json");
const destination = join(outputDir, "VIDEO.json");

try {
  copyFileSync(source, destination);
} catch (err) {
  console.error(
    `Could not copy VIDEO.json from ${botDir}: ${(err as Error).message}`,
  );
  process.exit(1);
}
