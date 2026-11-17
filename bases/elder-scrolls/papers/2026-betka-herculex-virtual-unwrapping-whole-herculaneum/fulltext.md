---
id: 2026-betka-herculex-virtual-unwrapping-whole-herculaneum
title: "HerculeX: virtual unwrapping of whole Herculaneum scrolls on Apple silicon"
year: 2026
backend: pymupdf
---

HerculeX: virtual unwrapping of whole Herculaneum scrolls on Apple silicon

Adam Betka

GitHub repository https://github.com/adambetka2/HerculeX — commit eace0b23ac (2026-11-17). Documents: README.md, ink/reading/README.md, calibration/unwrap/README.md, runner/README.md, spots/README.md. Community code repository (Vesuvius Challenge), not peer reviewed; all figures self-reported by the authors. Images omitted.

File: README.md

HerculeX is a framework for the virtual unwrapping of the carbonized Herculaneum scrolls from Xray CT. It turns a scroll's scan into flat, measurable sheets of papyrus, reads their ink, and serves the result in a local viewer where you and your agents can inspect and label it. It is built for Apple silicon and runs a whole scroll on one MacBook Pro.

Raw CT in, readable sheet out. HerculeX needs no manual segmentation, published meshes or surface predictions. It finds the papyrus in the CT and unwraps it automatically. Exact winding. HerculeX treats unwrapping as an integer optimization problem and solves it to proven optimality, instead of growing surfaces greedily and accumulating errors. Isometric surfaces. Each piece of sheet keeps its true lengths: 81 to 86 percent of neighboring grid points lie within 10 percent of their true spacing in 3D. Fast on a laptop. A scroll scanned at 9.4 µm goes from CT to a laid-out sheet in about two hours on a MacBook Pro with an M1 Pro chip and 16 GB of memory. Built to be used. Every stage resumes where it stopped, a job board shares the GPU, Neural Engine and network, and the viewer stores your labels in scan coordinates that agents can act on.

Contents

Overview How it works Results Unwrapped scrolls Get started Use the viewer Label a scroll Work with your agent Port to CUDA Repository layout License Citation Contact

Overview

The Herculaneum scrolls were carbonized by the eruption of Mount Vesuvius in 79 AD and cannot be unrolled. The Vesuvius Challenge publishes X-ray CT scans of the scrolls and awards prizes for reading them. HerculeX takes one scroll's scan from the open data and runs it through these stages:

CT scan (OME-Zarr, open data, fetched by byte range) │ scans/ choose the scan, fetch CT bricks as needed

▼ sheet nodes unwrapping/detection a node for each sheet crossing in each 8-voxel cell, with its normal ▼ pieces unwrapping/level exact integer winding levels; single-sheet pieces, flattened isometrically ▼ laid-out sheet unwrapping/level one frame per scan; every piece placed along the roll ▼ layer stacks sampling/ 31 layers along each piece's normals; the written face found from fibers ▼ ink maps ink/ Reader v3: Metal for the 3D stem, the Neural Engine for the 2D body ▼ scroll page website/ a lossless tile pyramid, a zoomable viewer, a card on the start page

Each stage writes its results as atomic units, and each unit records the version of the code that made it. When you stop a stage or change its code, HerculeX reruns only the units that are missing or out of date.

How it works

Sheet nodes

HerculeX reads the scan at about 19 µm per voxel (level 1 of a 9.4 µm scan) and divides it into cells of 8 voxels. In each cell, the structure tensor of the CT gives the local orientation of the sheet, and the intensity profile along the sheet normal has one peak for each sheet that crosses the cell. Each peak becomes a node with a position, a normal and a quality score. The GPU processes each cell in one Metal threadgroup, and tests compare its output with a C implementation of the same algorithm.

The sheet graph

Nodes in neighboring cells are joined by a sheet edge when their normals agree within 30 degrees and they lie on one surface. From every node, HerculeX also casts a ray along the normal; the first sheet that the ray meets lies one turn further out. HerculeX first makes the normals agree along the sheet edges, and then turns them to face out of the scroll's body with one minimum cut.

Exact integer levels

Unwrapping assigns each patch of nodes an integer winding level $f$, the turn of the spiral that the patch lies on. Patches merge on the evidence summed between them: sheet edges attract and rays repel. The levels then solve

$$ \min_{f \in \mathbb{Z}^{P}} \sum_{(a,b,k)} w_{ab}\,\rho\left(f_b - f_a - k\right) $$

where $k = 0$ for a sheet edge and $k$ is the number of sheets crossed for a ray, and $\rho$ is the absolute value. A ray can miss a faint sheet, so it only bounds the gap from below, and a residual on its permitted side costs half. Because the objective is an L1 norm over differences, its linear program is the dual of a minimum-cost flow and has integral optima. A network simplex solver written in C finds the exact optimum and certifies it. HerculeX solves both senses of winding and keeps the one with the lower cost. It then repeats the solve eight times with randomly reweighted votes, and builds pieces only from the edges that all eight solves keep.

Isometric pieces

HerculeX lays each piece flat in frames carried along its own sheet and writes it as a tifxyz grid at the node spacing. Each grid point is the sheet point at the center of its cell, so neighboring grid points lie one grid step apart in 3D. A harmonic fill bridges holes that reach up to 3 cells from their edge. A piece passes when at least 70 percent of its measured neighbor pairs lie within 10 percent of a grid step.

One frame per scan

HerculeX processes a scan in units of brick rows. It joins pieces of neighboring units across each seam by the sheet edges that cross it, unless confident rays show that the pieces lie stacked. One more exact level solve over all pieces of the scan gives each piece its turn. The layout then places each piece along the roll by its turn and its angle about the scroll's axis, and holds joined pieces together as rigid mosaics.

Layer stacks and the written face

HerculeX smooths each piece's mesh and samples 31 layers along its normals, reading the CT straight from bricks fetched by HTTP range requests. Papyrus is made of two crossed layers of fibers, so the fiber direction of the outer layer tells which face carries the writing.

Ink

HerculeX reads each piece with Reader v3, an open ink detection model, in a 17-layer window that starts at the written face. The reader runs on 512-pixel tiles: a Metal kernel computes the 3D stem, and the Neural Engine runs the 2D body in half precision.

The viewer

Every layer of a scroll (the scan at the surface, the brightest voxels across the sheet, and the ink) is stored as a tile pyramid packed into one file with an index. The browser reads tiles by byte range and decodes them with WebGL. The full-resolution level keeps the scan's original values without loss.

Results

All measurements were made on one MacBook Pro with an M1 Pro chip (10 cores, 16 GB of memory).

Whole scrolls

The following scrolls were unwrapped and read end to end, one after another. None of them has published meshes.

Voxel size

(µm)

Laid out

(cm²)

In mosaics of 4 cm² or more

(cm²)

CT to laid-out

sheet (h)

Ink maps

(h)

PHerc0125 9,801 6,631 1.3¹

PHerc0175B 10,824 5,359

PHerc0191 11,775 6,450 1.7¹

PHerc0358 8,507 4,991

PHerc0813 8,849 4,665

PHerc0826 5,720 3,323

PHerc0846B 6,064 3,521

PHerc1203 7,750 4,490

Total 69,290 39,428

¹ Sheet detection for these scrolls ran separately and isn't included.

The times for ink maps include downloading the CT that the reader needs. Stages typically peak at 3 to 8 GB of memory.

Geometry

Measure Result Data

Neighboring grid points within 10 percent of a grid step in 3D

81 to 86 percent of pairs; 96 to 99 percent of pieces pass the isometry check

All 82,550 pieces of the scrolls above

Correct share and wrong-wrap share against expert meshes

PHerc1667: 0.716 and 0.046; PHerc0139: 0.625 and 0.064; PHercParis4: 0.747 and

Crops with published meshes, used during development

Letters reached by the surface 91 percent of the nodes of the published PHerc0343 First Letters PHerc0343

Ink signal kept, compared with the published mesh read by the same model

89 percent The PHerc0343 First Letters crop

Known limitations

On scrolls without published meshes, nothing measures whether each piece lies on the right wrap. The scan frame doesn't hold every joint across unit seams, so a large mosaic can join two wraps, and order along the roll is approximate. The scores against expert meshes come from the development controls; a separate holdout set for geometry isn't defined yet.

Unwrapped scrolls

Each picture shows one scroll's whole sheet as HerculeX unrolled it, seen from the written face and cut into rows to fit the page. The ink is shown in purple. Scan data: Vesuvius Challenge.

PHerc0358: 8,507 cm² laid out

PHerc0191: 11,775 cm² laid out

PHerc0175B: 10,824 cm² laid out

PHerc0125: 9,801 cm² laid out

PHerc0813: 8,849 cm² laid out

PHerc1203: 7,750 cm² laid out

PHerc0846B: 6,064 cm² laid out

PHerc0826: 5,720 cm² laid out

To draw any published scroll this way, run ./run.sh website.overview PAGE OUT.jpg.

Get started

Requirements

A Mac with Apple silicon. HerculeX is developed on a MacBook Pro with an M1 Pro chip and 16 GB of memory. Xcode Command Line Tools (xcode-select --install). HerculeX compiles its C, Objective-C and Metal kernels on first use. uv, which installs Python 3.11 and the locked dependencies. About 40 GB of free disk space for each scroll, plus 25 GB for CT in transit. An external drive works; see Data folders. A fast internet connection. Reading a whole scroll downloads several hundred gigabytes of CT.

Install

git clone https://github.com/adambetka2/HerculeX.git && cd HerculeX UV_PROJECT_ENVIRONMENT=runtime/python uv sync --locked --extra ink ./run.sh ink.model.weights fetch ./run.sh check cpu

ink.model.weights fetch downloads Reader v3 at a pinned revision and checks its SHA-256 digest.

check cpu runs the tests that need neither the GPU nor the Neural Engine.

Data folders

HerculeX keeps all data in two folders, defined in storage/data_roots.py:

data/library/ what the pipeline reads: the scan catalog, model weights, hand labels, the spots database data/outputs/ what the pipeline makes: sheet nodes, pieces, layouts, layer stacks, the viewer's pages

To use another drive, set HERCULEX_DATA to move both folders, or HERCULEX_LIBRARY and HERCULEX_OUTPUTS to move either one. A symbolic link in data/ also works. HerculeX downloads the scan catalog, the CT and the model on first use; you don't need to configure anything else.

Unwrap a scroll

Add three jobs to the job board. Each job starts when the previous one finishes:

S=PHerc0826 ./run.sh board add $S-sheets --gpu --link --share --memory 5 --setting HERCULEX_LIST_CT_BRICKS=1 -- \ ./run.sh runner.pipeline run sheets $S ./run.sh board add $S-pieces --memory 5 --cores 3 --restartable --after $S-sheets -- \ ./run.sh runner.pipeline run pieces $S ./run.sh board add $S-sheet --gpu --engine --link --memory 5 --cores 5 --after $S-pieces --setting HERCULEX_KEEP_STACKS=0 -- \ ./run.sh runner.pipeline run sheet $S ./run.sh board status

The sheets job detects sheet nodes, the pieces job unwraps them, and the sheet job lays out the pieces, reads their ink and publishes the scroll's page. The scroll then appears on the viewer's start page. To run the same stages without the board, run ./run.sh runner.pipeline run all $S.

Read ink

The sheet job reads ink with Reader v3. To read ink without publishing, run:

./run.sh runner.pipeline run ink PHerc0826

To average several depths into a separate read, set HERCULEX_FACES=depths and

HERCULEX_DEPTH_SHIFTS=-4,-2,0,2,4. To read with another checkpoint of the same network, set

HERCULEX_WEIGHTS to its path and HERCULEX_MODEL_NAME to the name that the viewer shows.

Open the viewer

./run.sh website.site_server

Then open http://localhost:8765/sheets/index.html.

Use the viewer

The start page shows one card for each scroll, labeled with the scroll, the ink model, the surface and the date, and the total area read. Click a card to open the scroll's page: the whole unrolled sheet, from the full scroll down to one voxel per pixel.

The yellow outline marks the current place. Press N and P to step through the largest continuous areas.

Zoom in to read the ink. These letter forms are on PHerc0125 and PHerc0191, at places circled during review.

Heat mode shows the strength of the ink in color, from weak (blue) to strong (red).

Mode Keys

Purple or yellow Ink above a threshold, over the scan Y toggles yellow; , and . change the threshold; ; and ' change the scan's brightness

Heat The strength of the ink in color I

Layers The scan at the surface, the brightest voxels across the sheet, the ink ↑ and ↓

Places The largest continuous areas, largest first N and P

Swap ink A second ink map over the same sheet, when a page has one T

Label Mark ink, mark blank papyrus, circle a spot, erase, undo G, C, X, Z

View One voxel per pixel, mirror, turn, invert, Greek letters from the scrolls, full screen 0, H, U, K, F

To move, use W, A, S and D or drag. To zoom, use E and R or scroll. Press ? to list every key.

Label a scroll

Click Label to open the labeling tools:

Mark (G) draws ink strokes, shown in red. Blank marks papyrus without ink, shown in blue. Spot (C) circles a place that may hold letters, shown in green. Erase (X) and Undo (Z) remove marks. Hide marks (L) hides them while you read.

The viewer saves each mark the moment you draw it. Marks go to a local database in

data/library/marks/, one append-only log for each scan, with one JSON line per mark:

{"time": "2026-11-16T23:28:30Z", "kind": "spot", "width_mm": 0.3, "layer": "ink", "points": [[6471.271, 153.686], [6471.263, 153.797], ...], "id": "5f6f5624...", "layout": "1dc7e9db88c3"}

Points are in millimeters on the unrolled sheet. The layout field names a snapshot of the piece layout that the mark was drawn on, saved beside the log, so each mark stays tied to the same papyrus even after you rebuild the layout. To map spots back into the scan, run:

./run.sh spots.catalogue

This builds the spots table (Parquet, in data/library/studies/shared/spot-candidates/db/). For each circle, the table lists the scroll, scan and page, the pieces and windings under the circle, its area, and its bounding box in scan voxels, ready for an agent or a script to use.

Work with your agent

HerculeX is designed to be driven by a coding agent while you read. AGENTS.md gives the agent the rules and commands it needs, and each folder's README describes its files. A typical session looks like this:

1. Ask your agent to unwrap a scroll, for example "Unwrap PHerc0826." The agent queues the three jobs from Unwrap a scroll. 2. When the read finishes, the scroll's page appears on the start page. To add any other page to the start page, the agent runs ./run.sh website.site_pages card PAGE, which labels the card from the page itself. 3. Read the scroll in the viewer, and circle places that may hold letters. 4. Ask your agent to work on your circles while you keep reading. The agent builds the spots table, rebuilds each spot as a continuous surface, reads it at every depth from -15 to +15, and publishes a page for each spot under /sheets/spot-candidates/, where you choose the depth and record a verdict. See spots/README.md.

Port to CUDA

HerculeX is tuned for Apple silicon: unified memory, a Metal GPU and the Neural Engine. Everything above the kernels is Python, NumPy and C. To run it on a Linux machine with an NVIDIA GPU, fork the repository and give your coding agent this task:

Port HerculeX to Linux with one CUDA GPU. Keep each stage's output identical within the tolerances of its tests. 1. unwrapping/detection: write a CUDA kernel for gpu_nodes.metal (one block for each 8-voxel cell, the same Node record). cpu_nodes.py and node_kernels.c are the reference; tests/test_sheet_nodes_golden.py compares them. 2. ink/model: portable_reader.py already reads Reader v3 in PyTorch with tile_reader.py's tiling, norms and blending. Run it on "cuda" in float16 or bfloat16 in place of depth_stem.metal and the Neural Engine body (neural_engine.py, engine_calls.m), and change the device "mps" to "cuda" everywhere else. 3. runner/compiled_kernels.py already builds the C kernels with cc on Linux; drop the Objective-C sources. 4. runner/job_board.py: one GPU slot and no Neural Engine slot; set the memory limits for the new machine. 5. Run ./run.sh check, then unwrap one scroll end to end, and compare its record.json files and page with a Mac run.

Repository layout

scans/ the scan catalog of the open data, and byte-range fetches into brick stores unwrapping/ sheet detection, exact winding levels and pieces, the scan frame and the layout sampling/ layer stacks along each piece's normals, and the written face ink/ Reader v3: download, tile reader, Neural Engine body, portable reader; the ink stage website/ tile pyramids, the viewer, the start page, the local server and its label store spots/ circled spots to depth sweeps, verdicts and submissions calibration/ unwrapping scored against published meshes and a synthetic scroll runner/ the pipeline, the job board, compiled kernels storage/ data folders and binary formats records/ measured results of the calibration studies tests/ end-to-end tests on synthetic scrolls, and tests of fast paths against reference code docs/ images and the generator of the title art

Each folder has a README that describes its files, commands and outputs.

License

HerculeX is released under the MIT License. Reader v3 by Domenico Russo and the Vesuvius Challenge villa code are MIT-licensed; HerculeX downloads them at pinned revisions. The scan data belongs to the Vesuvius Challenge and is subject to its terms. The title art is drawn by

docs/art/minoan.js.

Citation

@software{herculex2026, author = {Betka, Adam}, title = {HerculeX: virtual unwrapping of Herculaneum scrolls from X-ray CT}, year = {2026}, url = {https://github.com/adambetka2/HerculeX} }

Contact

Email adambetka2@gmail.com, or open a GitHub issue.

File: ink/reading/README.md

ink/reading

These modules run the ink stage over every laid-out piece, and read selected places again at other depths.

piece_reading.py

Runs the ink stage. For each piece, it samples the layer stack, writes the scan images, finds the written face, and reads the ink map. It fetches the next CT store while it reads the current one.

spot_depths.py Reads the places circled with the viewer's Spot tool again at three nearby depths, and writes a page of them.

passage_reads.py Reads listed pieces again from freshly sampled stacks with each checkpoint you name, at depths -4 to +4 and as a mean over depths, and writes a page beside the site's map.

same_output_models.txt Lists, one line per checkpoint, its current read digest followed by earlier digests that give

byte-identical maps.

# The pipeline's ink stage: lay the pieces out again if they changed, then read them. ./run.sh runner.pipeline run ink SCROLL [--scan ID]

# Read one scan directly. ORDER.json optionally lists the stores and pieces to read first. ./run.sh ink.reading.piece_reading SCROLL SCAN [ORDER.json]

# Fetch the CT of a read's first STORES stores without reading, for example while the GPU is busy. ./run.sh ink.reading.piece_reading ahead SCROLL SCAN STORES [ORDER.json]

# Read every circled spot on a published sheet at three depths. ./run.sh ink.reading.spot_depths SCROLL SCAN SHEET_NAME [MARKS.json] [PAGE_NAME]

# Read the pieces listed in PLACES.json again with one or more checkpoints. ./run.sh ink.reading.passage_reads SCROLL SCAN PLACES.json PAGE_NAME WEIGHTS...

For a whole scroll, run the read as a job on the job board.

Outputs

The ink stage writes each piece's images and ink map to faces/level-0/UNIT/ in the scan's folder (unwrapping/level/SCROLL/SCAN/ in the outputs). It keeps each piece's layer stack in

stacks/level/SCROLL/SCAN/ in the outputs, and deletes each unit's fetched CT store after the unit is read. If a read fails, the CT it fetched stays in place for the next attempt.

Settings

Variable Default Effect

HERCULEX_WEIGHTS Reader v3 Reads with another checkpoint of the same network.

HERCULEX_SAMPLERS Sets the number of processes that build stacks ahead of the reader.

HERCULEX_WINDOWS stacks/level/ in the outputs Sets the folder for kept layer stacks.

HERCULEX_KEEP_STACKS Set to 0 to skip keeping layer stacks.

HERCULEX_KEEP_BRICKS unset Set to 1 to keep each unit's CT store after its read, so a later read of the same units fetches only the bricks that new pieces add.

HERCULEX_FACES level-0 Writes a separate read to faces/NAME/ instead of the published read.

HERCULEX_DEPTH_SHIFTS Averages reads at these comma-separated layer shifts, for example -4,-2,0,2,4.

HERCULEX_UNITS every unit Reads only these comma-separated units.

A separate read uses the same written face as the published read. Set HERCULEX_FACES whenever you set HERCULEX_DEPTH_SHIFTS, so that the separate read doesn't replace the published one.

runner.review_page publishes only a full read in faces/level-0/; to view a separate read, use

website.sheet_tiles and website.site_pages part.

File: calibration/unwrap/README.md

calibration/unwrap

These tools score sheet detection and unwrapping on two kinds of control: bands of scans that have published meshes, and a synthetic scroll whose windings are known exactly.

sheet_controls.py Builds a band of every scan that has published meshes, as sheet nodes with mesh truth, in the library's controls/sheets/.

mesh_reference.py Extracts the reference vertices of a band from the published meshes and works out which meshes lie on the same sheet.

mesh_surfaces.py Provides the grid surfaces, normals and scroll axis that references and predictions share.

sheet_scoring.py Unwraps every control and scores its recovery, purity and frame agreement.

sheet_wrap_truth.py Builds the wrap truth of each control from its reference meshes.

sheet_wrap_score.py Scores node labels against the wrap truth.

sheet_wrap_study.py Unwraps every control and measures the contiguous correct area against the wrong-wrap rate.

sheet_wrap_report.py Prints several wrap studies side by side as a Markdown table.

sheet_wrap_survey.py Measures the contiguous area of every survey band and compares it with the published

meshes.

continuous_area.py Reports how much of a scan's readable area lies in continuous areas of 4 cm² or more.

raw_sheet_ruler.py Counts the sheets in the raw scan along straight lines through a unit and compares them with the levels that the unit's solve assigns.

synthetic_scroll.py Builds a crushed scroll of exactly known windings, voxel by voxel, for the tests.

# List the planned control bands, then build them for every scroll or for the scrolls you name. ./run.sh calibration.unwrap.sheet_controls plan ./run.sh calibration.unwrap.sheet_controls build [SCROLL ...]

# Score the controls. Add joint to score two halves of each control joined across a seam. ./run.sh calibration.unwrap.sheet_scoring [joint] [CONTROL ...] ./run.sh calibration.unwrap.sheet_wrap_study [CONTROL ...]

# Measure the continuous area of one scan. ./run.sh calibration.unwrap.continuous_area SCROLL SCAN

# Compare a unit's levels with sheets counted in the raw scan. It fetches CT, so run it on the board with --link. ./run.sh calibration.unwrap.raw_sheet_ruler SCROLL SCAN UNIT PLANE0 PLANE1 OUT.json

HERCULEX_STUDY_WORKERS sets the number of worker processes for sheet_wrap_study (default 3).

File: runner/README.md

runner

The runner package runs the pipeline on one Mac. It defines the stages, makes each stage resumable, and uses a job board to share the GPU, the Neural Engine, the network link and memory between long jobs.

pipeline.py Defines the pipeline's stages and runs or resumes each one from its records.

sheet_stage.py Takes a scan's pieces to the website: it lays them out, reads every piece, and then publishes the scroll's page.

review_page.py Publishes a read scan as its whole-scroll page and puts its card on the start page.

stage_queue.py Provides what every stage shares: code digests, atomic units, unit claims and stage locks.

job_board.py Runs one queue for every long job, with resource slots, memory limits, priorities and a swap guard.

wait_for_queue.py Exits once none of the named board jobs can still run, however they end.

memory_trace.py Runs a module or script and reports where its memory footprint peaks, line by line, including C and GPU memory.

compiled_kernels.py Compiles the C and Objective-C kernels once per source digest into runtime/kernels/.

Run a scroll

Run every command from the repository root. Fetch Reader v3 once with ./run.sh ink.model.weights

fetch. Then queue three board jobs for the scroll:

S=PHerc0826 ./run.sh board add $S-sheets --gpu --link --share --memory 5 --setting HERCULEX_LIST_CT_BRICKS=1 -- \ ./run.sh runner.pipeline run sheets $S ./run.sh board add $S-pieces --memory 5 --cores 3 --restartable --after $S-sheets -- \ ./run.sh runner.pipeline run pieces $S ./run.sh board add $S-sheet --gpu --engine --link --memory 5 --cores 5 --after $S-pieces --setting HERCULEX_KEEP_STACKS=0 -- \ ./run.sh runner.pipeline run sheet $S ./run.sh board log $S-sheet

Each job starts when the one before it finishes. The last job reads every piece and publishes the scroll's page, with its card on the start page.

Stage What it does Uses

sheets Detects sheet nodes in the scroll's survey scan and fetches the CT as it goes. GPU, link

pieces

Unwraps the nodes into pieces, joins them across unit seams, and fits the scan's frame. CPU

layout Places the pieces on one sheet. CPU

Stage What it does Uses

ink SCROLL Lays the pieces out again if they changed, then reads every piece into an ink map.

GPU, Neural Engine, link

sheet Runs ink, then publishes the scroll's page and its card on the start page. GPU, Neural Engine, link

all SCROLL Runs sheets, pieces and sheet at once, each following the one before, without the board. All

Every stage resumes from its finished units. If a job fails, fix the cause and run ./run.sh board retry

NAME. Add --scan ID to a single stage to use a scan other than the survey scan, or --band to sheets,

pieces or all to process only a central band of the scan. To see what is done, run ./run.sh

runner.pipeline status [SCROLL]; to rebuild the index of finished units, run ./run.sh runner.pipeline

index.

The sheet stage ends with runner.review_page SCROLL SCAN. It composes the tiles of the scan and the ink, writes the viewer page and its card on the start page, and, if the local site is running, checks the tiles and marks over HTTP. To publish a read scan again, run ./run.sh runner.review_page SCROLL

SCAN.

Settings

Variable Default Effect

HERCULEX_WEIGHTS Reader v3 Reads with another checkpoint of the same network.

HERCULEX_MODEL_NAME Reader v3, or the checkpoint's file name Names the ink model on the page and its card.

HERCULEX_KEEP_STACKS Set to 0 to skip keeping each piece's layer stack.

HERCULEX_BRICKS cache/bricks/ in the library Puts the CT brick cache on another drive.

HERCULEX_LIST_CT_BRICKS unset Set to 1 on sheets to list the published bricks first and skip masked-out ones.

HERCULEX_SITE http://127.0.0.1:8765 Sets the local site that the sheet stage checks after it publishes.

HERCULEX_BOARD runtime/board/ Sets the folder for the board's database, logs and dispatcher lock.

HERCULEX_BOARD_MARGIN_GB Sets the memory, in GB, that the board leaves free.

Job board

./run.sh board add NAME [OPTIONS] -- COMMAND ./run.sh board status | log NAME [LINES] | room GB | wait NAME | forecast [NAME] | usage [HOURS] ./run.sh board hold|release|cancel|retry|remove NAME ./run.sh board resize NAME GB ./run.sh board change NAME [--priority N] [--cores N] [--share 0|1] [--restartable 0|1]

status lists the jobs and why each waiting job waits, room GB checks whether that much memory fits now, wait blocks until a job ends, and forecast estimates when the queue or one job ends. The main options of board add are these:

--gpu, --engine and --link claim the GPU, the Neural Engine and the network link.

--memory GB is the job's peak memory. If you leave it out, the board uses the last peak of jobs of the same kind.

--cores N is the number of CPU cores the job uses (default 1).

--after JOB ... waits until those jobs are done; --priority N orders waiting jobs; --held waits for release.

--setting KEY=VALUE ... sets environment variables for the job.

--share marks a job that mostly downloads and uses the GPU in short bursts, such as sheet detection. It can run beside the one job that holds the GPU or the link: one sharing job on the

GPU and two on the link. The Neural Engine is never shared.

--restartable lets the board stop the job and run it again later.

When a GPU job is held back only by cores or memory that lower-priority restartable jobs hold, the board stops one of them, at most one a minute, and the stopped job runs again once there is room. A job that a waiting GPU job needs within two steps, such as its layout, can make room the same way, but it stops only sharing jobs. When swap grows too large, the board stops the largest restartable job of the lowest priority. A job that exits with code 75 goes back to the queue and runs again later.

Before you run a test or a quick GPU check by hand, run ./run.sh board room GB to check that it fits beside the running jobs. The first board command starts a dispatcher in the background. If you change job_board.py, stop the dispatcher with kill $(cat runtime/board/dispatcher.lock); the next board command starts it again with the new code.

File: spots/README.md

spots

The spots package turns each circle that you draw with the viewer's Spot tool into a depth sweep that you can judge. For each circle, it narrows the sheet to the pieces under the circle, rebuilds them as continuous surfaces, reads them at every depth from -15 to +15, and stores the results in a Parquet database. Use it to find and judge candidates for a First Letters submission (10 legible letters in 4 cm²).

sources.py Finds the scroll, scan, page and pieces that each marks log belongs to.

catalogue.py Locates every standing Spot circle on its pieces and in the scan, and writes the spots table.

surfaces.py Narrows a spot's pieces to the circle, rebuilds them on the m7 surface prediction, and renders 67 layers along the normal.

sweep.py Reads every rendered surface at every depth, in both stack orders, with Reader v3 and any readers you list.

images.py Lays the sweep out as the page showed it, stretches each model's reads once, builds a z-score ensemble, and writes a page per spot.

pilot.py Runs one spot through its stages; each stage resumes where it stopped.

database.py Keeps the Parquet tables spots, surfaces, reads and verdicts, and records verdicts.

flatten.py Shifts each pixel's column of a rendered stack along the normal so that the stack follows its own papyrus layers.

reflatten.py Gives a mesh grid a near-isometric flattening, laid out by its 3D edge lengths and resampled on a

regular grid.

# Build the spots table from the live marks and print each spot's ID. ./run.sh spots.catalogue

# Run the named stages for one spot, or all of them in order. ./run.sh spots.pilot SPOT [build] [grow] [render] [read] [images]

# Show the table sizes, or print one table as JSON lines. ./run.sh spots.database [TABLE]

# Record a verdict. ./run.sh spots.database verdict SPOT SURFACE --by NAME --readable no|traces|letters|passage [--letters N] \ [--stack ensemble] [--side inward] [--depth D] [--reading TEXT] [--note TEXT]

On the job board, each spot is two jobs: a build on the network link and a read on the GPU and the Neural Engine.

./run.sh board add spot-SPOT-build --link --memory 3 -- ./run.sh spots.pilot SPOT build render ./run.sh board add spot-SPOT-read --gpu --engine --memory 5 --after spot-SPOT-build -- ./run.sh spots.pilot SPOT read images

The pages are at http://localhost:8765/sheets/spot-candidates/index.html. The index lists every circle and links to the sweep page of each spot that has one. On a sweep page, the arrow keys step through the depths and the stacks.

Choose the circles

Every standing circle is a target. To target only recent circles, set HERCULEX_SPOTS_SINCE=YYYY-MM-DD; older circles stay in the table, marked as not targets.

The tools find circles on any page that the pipeline published. For a page made another way, such as a rebuilt surface, add an entry to the library's marks/sheets.json in the form {key, scroll, scan,

route, page, pieces}, with pieces relative to the outputs folder.

How a spot is read

The method follows the published code of the PHerc0343 First Letters entry.

Surfaces. original is the piece as the pipeline reads it. m7 moves every node along its normal onto the nearest sheet in the published m7 surface prediction for the scan. grown, made by the optional grow stage, extends the m7 surface past its edges and into its holes wherever the prediction holds a sheet within 6 voxels along the normal, and is cut to the circle's box and margin. Render. Each surface is rendered as 67 layers one voxel apart. Depth d is the layer number minus 33, so d = 0 is the surface and positive depths point away from the scroll axis. Sweep. A reader reads a 17-layer window centered on every d from -15 to +15, in both stack orders: outward and inward (reversed). You decide from the images which side holds the writing. Readers. The sweep reads with Reader v3 and with any other checkpoint of the same network that you list in the library's weights/sweep-readers.json as {"name": "path under

weights/"}. Reader v3 alone reads the original surface. Images. Each model's reads are stretched once over all depths, never per depth, from their median to their 99.9th percentile; the CT is stretched from its 1st to its 99.5th percentile. The ensemble averages the models' z-scores, and ensemble 5 depths also averages it over d-2 to

d+2. A page opens at the depth where the ensemble's 97th percentile inside the circle peaks. You can mirror or turn the view.

Most circles cover several pieces, often from different windings, that the layout places side by side. Each piece is rebuilt and read on its own as one continuous surface, and the pieces are laid out together only for the images. As a result, letters that cross two pieces of different windings don't join up.

Data

All spot data is stored in SPOT_CANDIDATES, the library's studies/shared/spot-candidates/ folder:

Folder Contents

db/ The Parquet tables.

m7/ The fetched chunks of the m7 prediction.

spots/SPOT/ The surfaces, CT bricks, stacks and reads of each spot.
