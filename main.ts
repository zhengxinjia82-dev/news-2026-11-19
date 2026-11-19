// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. A starting point, not a winner: replace the image. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
// 19 Nov 2026 entry: IMG_4962.png is the four-story infographic drawn by draw.py (Trump–Xi–Putin summit,
// Crimea bridge, ICJ Rohingya ruling, Anthropic IPO); this program hands those exact bytes in. The file is
// named IMG_4962.png because the photo was uploaded to GitHub via Photos, which renamed entry.png;
// the output is still entry.png, as the gate requires.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./IMG_4962.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
