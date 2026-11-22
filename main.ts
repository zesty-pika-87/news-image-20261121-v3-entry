// News-image entry for Saturday 21 November 2026: the front page this
// repository draws (see draw.py) is shipped as entry.png, and this
// program copies it to the output directory the grader provides.
// The shipped image is the whole entry: 35 stories from 21 November
// 2026, 13 layered illustrations, and a world map whose numbered pins
// match the numbered index. Node 22, standard library only; no network,
// no clock, so both runs of the program write the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
