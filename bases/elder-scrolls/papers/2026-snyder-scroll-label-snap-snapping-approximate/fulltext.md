---
id: 2026-snyder-scroll-label-snap-snapping-approximate
title: "scroll-label-snap: snapping approximate recto-surface labels back onto the papyrus surface in Herculaneum scroll CT"
year: 2026
backend: pymupdf
---

scroll-label-snap: snapping approximate recto-surface labels back onto the papyrus surface in Herculaneum scroll CT

A. Q. Snyder

GitHub repository https://github.com/aqsnyder/scroll-label-snap — commit e03c4c088c (2026-11- 11). Documents: README.md, results/review_2026_11.md, results/ink_test.md, results/ink_test_0841.md. Community code repository (Vesuvius Challenge), not peer reviewed; all figures self-reported by the authors. Images omitted.

File: README.md

scroll-label-snap

Moves approximate recto-surface labels in Herculaneum scroll CT back onto the real papyrus surface.

This is work in progress toward a Vesuvius Challenge progress-prize submission. It targets the "label quality" open problem in the 2026 open problems. Surface models are trained on handtraced labels, and those labels drift off the surface. The organizers name this one of the main unwrapping bottlenecks and suggest "label snapping" as a fix.

Status, 4 November 2026: the w052 ink test went against snapping, and on PHerc. 0841 no gain repeats

Three tests of the mesh snapper came in this week. Two were pre-registered.

Ink legibility on a held-out segment (pre-registered). Two blind reviewers compared ink maps from the original and the snapped w052 mesh. They preferred the original 75 times and the snapped mesh 31 times (p = 2 × 10⁻⁵). The loss is spread over the whole segment, not concentrated where the mesh moved most. Details: results/ink_test.md. Ink labels on a scroll the model hasn't seen (pre-registered, suggested by KLAVIS). On three traced PHerc. 0841 segments, snapping made no detectable difference to agreement with the ink labels. On KLAVIS's spiral-fit windings, as run, the drop-in output was about even and the dense output lost up to 0.22 AUC. Part of that loss came from a bug in our depth transfer. With it fixed (post hoc, exploratory), the dense output's pooled loss goes from −0.078 to −0.051 at the plan's seed, and from −0.098 to −0.002 at a second model seed. Neither output shows a loss or a gain that repeats at both seeds, though the intervals still allow a pooled loss of up to about 0.09 AUC. Details: results/ink_test_0841.md. Face placement against an independent reference (by Chase). The test used fresh PHerc. 0139 sites: 173 vertices of model-output surfaces at 28 sites. Chase compared them with the recto face found in two higher-resolution scans. At default settings, 18% of vertices ended within 1 voxel of that face, against 17% before snapping. By design, the snapper keeps each mesh's own offset from the face. With --target-offset 0 and the learned profile off, the share was 43%. His tool, snap_labels, reached 80%.

A follow-up diagnostic (results/depth_sweep.md) looked for the cause: - Not the surface's average depth. Moving a whole mesh 1–2 voxels barely changes the ink map's level, and agreement with

ink labels doesn't change detectably. - The snapper's varying moves. Snapping lowered w052's map level, and so did a mirrored mesh moved as far the other way, a little less. On PHerc. 0841, the mirrored depth cost 0.07 AUC while the snapped one made no detectable difference (read as 0 ± 0.05). The mirrored depth hasn't been rerun without the depth transfer bug's false holes, about 0.5% of hits. - Their vertex-scale bumps, specifically (results/move_scale.md). The drop-in output's moves vary from one vertex to the next. With the moves smoothed over about 20 voxels, w052 keeps its map level, and the mesh keeps 43% of the snapper's gain at the face. With only the bumps, it loses as much as the full snap.

So, for now: - Don't use snapped meshes for ink detection. - Read the drift tests below as consistency (does the snapper put a drifted label back where it was?), not as accuracy against the true face. - The label-cube results and their blind reviews below still stand for what they measured. None of these three tests looked at the cubes. The November review did: snapped labels gain tunnels and merge sheets, and the drift test can't rank the snapper against a plain persample search.

Update, 9 November 2026. - A smooth snap made no detectable difference on PHerc. 0841's ink labels (pre-registered; results/smooth_snap.md). - The smooth snap is the drop-in output with its moves smoothed over 1 vertex. - Against the traced meshes it is +0.008 and +0.006 AUC at two model seeds, and a loss larger than 0.05 is excluded. - It keeps the map level on all three targets, and 35–39% of the snapper's gain at the face. - By the plan, it now goes on to a blind review of its maps. Until then it isn't offered for ink work. - The same ink tests on Chase Hendrick's released finesnap surfaces (results/finesnap_ink_plan.md) ran on 4 November. Their results will be posted here once he has seen them. - Pre-registered next (results/smoothing_tradeoff_plan.md): how little smoothing keeps the map level, and how much of a snap's placement at the face it keeps, for both snappers. - A blind review at matched level (results/ink_review_matched_plan.md) asks whether snapped w052 maps are less legible or only dimmer. One of three reviewers has answered, and the key is still sealed.

Chart by Chase, shared in the Vesuvius Challenge Discord and used with his permission. In his test, scroll-label-snap ran on 13 × 13-vertex crops. That gives its offset estimate and learned profile fewer samples than a whole segment would.

How it works

For each labeled cube:

1. Sample the surface. The labeled surface is sampled every ~3 voxels. 2. Normals come from the shape of the label band. 3. Each normal is oriented to point from papyrus toward the gap. 4. Orientation is made consistent along each sheet, and then across neighbouring sheets. Every wrap's recto faces the scroll centre, so neighbouring sheets should point the same way. 5. Score candidate shifts from −4 to +4 voxels along the normal, by adding two terms: 6. Step edge. A narrow step finds the edge. A wide step checks that papyrus is behind it and a real gap in front, which rejects thin cracks inside a sheet. 7. Learned profile match. Normalized cross-correlation with the cube's own typical crosssection at a label. 8. Choose all shifts at once with an exact graph cut (Ishikawa construction). It minimizes: 9. the score cost 10. an L1 smoothness term between neighbouring samples on the same sheet 11. a hard limit of 1 voxel shift difference between neighbours 12. a weak pull toward the original label 13. a penalty for moving a label outward (toward the gap) to a spot with papyrus on both sides. There the normal is probably flipped, or the label sits on the far face of a sheet, and pushing it further only buries it in the sheet (new in v2).

14. Move the label band along the solved shift field. Each voxel's displacement is blended from nearby samples on the same sheet, and the band is resampled with interpolation, so a moved band keeps clean edges (new in v2; v1 left stair steps). Not-annotated regions (label 2) are never changed. A per-voxel confidence map is written as well.

scroll_label_snap/core.py also contains a port of the existing VC3D refiner (ObjAlphaCompRefinement) as a baseline. tests/test_solver.py checks the graph cut against brute force.

Results on the label cubes

Two sets of cubes, evaluated the same way with the default parameters (tools/eval_folder.py): - Development (20 cubes): the cubes the method was built and tuned on. Full tables in

results/eval_dev.md. - Held-out (100 cubes): other cube pairs picked at random from the bucket. The seed was fixed and pushed before any of them were downloaded, and nothing was tuned on them. Full tables in results/eval_heldout.md.

Per-cube numbers are in the matching .json files. A before/after on cube sample_00005 is in

results/labels_before_after_00005.png. It shows the three largest changes and three random slices.

The existing refiner as a baseline

scroll_label_snap/core.py contains a port of VC3D's alpha-composite refiner (ObjAlphaCompRefinement), the refinement step that exists today. With VC3D's default opacity thresholds (118 and 165 of 255), it does worse than leaving the labels alone here. In these cubes the gap is about 50 and papyrus about 125, so the lower threshold sits just below the papyrus level and the upper one well above it. To make it a fair baseline, it is also scored in three better-set-up versions: - Offset removed. The refiner works to its own convention: it puts the surface just past the first voxel above the threshold, not where these annotators draw it. Each version has its median shift on the clean labels removed. - Thresholds from each cube's own levels, offset removed: the mean brightness of gap and of papyrus (the two Otsu classes). This needs no tuning. - The best fixed thresholds, offset removed: the best of 13 threshold pairs on the development cubes (70 and 110). On the held-out cubes we report that pair, and also the pair that is best on the held-out cubes themselves, as the refiner's ceiling.

The offset removal uses the clean labels, which a real user wouldn't have; the snapper takes its convention from the labels it is given. With these drift fields that difference is small: on the development cubes, each field's median is within 0.15 voxels of zero.

Drift test

Each cube's labels were pushed off the surface by a known smooth random drift (std 1.5 voxels, correlation length 40 voxels). Each method was then run on the drifted labels, and we measured how far the result lands from the original label. This is scored only at trusted points: the 10% of samples (7% held out) where, by the snapper's own edge score, the strongest edge within reach is already at the label and no other edge comes close (258,394 points in development, 717,523 held out). A method that goes to the strongest edge returns to these points almost by construction.

Within 1 voxel:

development

Within 1 voxel: held-

out

Mean error (voxels):

development

Mean error: held-

out

No correction (drifted labels)

Existing refiner, VC3D default thresholds

Existing refiner, default thresholds, offset removed

Existing refiner, thresholds from each cube's own levels, offset removed

Within 1 voxel:

development

Within 1 voxel: held-

out

Mean error (voxels):

development

Mean error: held-

out

Existing refiner, best thresholds on development (70-110), offset removed

Snapper

The refiner's ceiling on the held-out cubes, the pair that is best there (50-110, picked after seeing them), reaches 80% within 1 voxel (mean error 0.69).

A per-sample best score with no graph cut beats the snapper on all 20 development cubes (94% vs 89%, +4.4 points, 95% CI 3.7 to 5.2; held-out cubes not run). The order depends on how trust is defined: trust a point because the edges of its neighbours 4-12 voxels away sit at the label, without reading its own CT, and the snapper leads on all 20 (85.5% vs 82.2%). So this test doesn't show that the graph cut helps or hurts (results/review_2026_11.md).

Consistency is measured at all points. It asks whether correcting the drifted labels lands in the same place as correcting the clean labels.

Within 1 voxel Development Held-out

Existing refiner, default thresholds

Existing refiner, thresholds from each cube's own levels 77%

Snapper

Clean labels. This is the intensity step across each label, papyrus side minus gap side. It is circular: the snapper optimizes edge strength, and a per-sample search with no graph cut scores higher (95% vs 91% on the development cubes, higher on all 20). The drift test picks its points with the same edge score, so it isn't independent of this table.

Papyrus on the correct side of the label Development Held-out

Original labels

Existing refiner, default thresholds

Existing refiner, thresholds from each cube's own levels, offset removed 75%

Snapper

The same figure for the development cubes is results/eval_dev.png.

What this shows: - Most of the refiner's poor default result is its thresholds. Set from each cube's own levels, with its offset removed, it goes from 9% to 80% on the development cubes (18% to 78% held out). That fix is simple and needs no tuning; it may be worth having in VC3D on its own. - The snapper is still ahead of the best-set-up refiner on accuracy. - Within 1 voxel: +9 points on the development cubes and +10 held out. - Mean error: 0.52 vs 0.68 voxels in development, 0.55 vs 0.73 held out. - Over 2 voxels: 3% vs 4% in development, 3% vs 6% held out. - Cube by cube it does as well or better on 19 of 20 development cubes and 94 of 100 held-out cubes. The median held-out cube gains 10 points. - On consistency the two are close. The snapper is within 1 voxel of its own clean-label result more often (81% vs 77% in development, 75% vs 73% held out). Held out, it also has slightly more large differences (14% vs 12% over 2 voxels), so its mean difference is larger (1.04 vs 0.92 voxels). - Against no correction, the snapper is better on 97 of the 100 held-out cubes. It is worse on three: sample_00184, sample_00186 and sample_00478. - Where the refiner wins. The refiner with the cube's own levels scores higher on sample_00018 in development (72% vs 67%) and on six held-out cubes. Two of those gaps are large: sample_00478 (59% vs 49%) and sample_00639 (84% vs 79%). The other four are 2 points or less.

Drift draws, and an earlier number

The drift is random, so per-cube numbers depend on the draw. Earlier versions of this README reported 91% within 1 voxel for the snapper on the development cubes. That run seeded cube k with k // 2 (it ran as two processes, each counting from 0); the current runs seed cube k with k, as the held-out run always did. The code is the same: with the old seeds, all 20 development cubes give exactly the old drifted labels, and sample_00002 and sample_00018 give exactly the old snapper results.

Most cubes move by a few points between draws. sample_00018, a hazy cube, goes from 93% with the old draw to 67% with the new one: - What happens. With the new draw, 15% of its trusted points end more than 2 voxels off (8% for the refiner with the cube's own levels). Most of them are about 3 voxels toward the papyrus side, in many small patches, and not where the drift was largest. - Why. This draw reverses the sheet orientation at 32% of the cube's trusted points. The snapper gets 10% within 1 voxel at those points and 93% at the others, the same as the old draw. A per-sample search has the same problem (5% and 98%). Turning the profile term off lifts the reversed points to 44% and lowers the others to 90%, which gives 75% in all and 6.5% more than 2 voxels off. - Next. Keeping sheet orientation stable under drift comes first (Params.orient_cube, with its test pre-registered in results/orient_test_plan.md), then making the learned profile independent of where the input labels sit. A change like that needs a fresh held-out set, since this one has now been used.

tools/drift_draws.py runs both checks: seeds rebuilds an older run's drifted labels with a given seed scheme, and diagnose describes one cube's large misses under one draw. The v1-to-v2 comparison below comes from the earlier runs. We haven't confirmed that v1 used the same draws.

The whole dataset

All 892 cube pairs in the bucket have been snapped with the v2 defaults (tools/snap_folder.py, 12 workers on a Ryzen AI Max+ 395). That is 116 million surface samples in 15.8 CPU-hours, about 1.3 hours of wall time. Per-cube numbers are in results/full_run_summary.csv:

Per cube Median 5th-95th percentile

Surface samples 121,680 49,634-234,488

Share moved by 1 voxel or more 61-77%

Share flagged (label on a reversed face) 6.9% 2.3-17.5%

Mean confidence 0.66-0.89

The most-flagged cubes are also the lowest-confidence ones: samples 00798, 00256 and 00323 have 25-34% flagged. That makes them good places for a human to look first.

Changes since v1

From the earlier development runs, results/eval_v1.md and results/eval_v2.md, with the old drift seeds:

v1 v2

Drift test: within 1 voxel

Drift test: mean error (voxels)

Consistency: within 1 voxel

Extra edge roughness of the band vs. the original labels +11% +6%

Smooth warp. Roughness is the number of exposed voxel faces per band voxel, over all 20 cubes (tools/roughness.py). Moving a band by a smooth shift adds roughness by itself: the drift test's smooth drift (std 1.5, corr. 40) adds +6.1% over these cubes, so the snapper's +6.0% is at that floor. A per-sample search with no graph cut adds +18.8%. See

results/warp_v1_vs_v2.png. Inside-the-sheet guard. On the 120 moves in the blind review, v2 puts 3 of the 8 losses back on the original label (q057, q070, q107). It leaves 90 of the 98 wins within 0.5 voxel of

where v1 put them; 2 went back to the original. See results/review_v1_losses_v2.png;

tools/recheck_review.py produced the per-item numbers in results/review_v1_items_under_v2.json. The guard only penalizes outward moves. We chose that after seeing that penalizing inward moves as well also undid 2 wins, so these review numbers are optimistic. A fresh review is the real test. Drift-test inputs. The drifted labels and the existing refiner's output now go through the smooth warp too, so their rows moved slightly from v1.

Caveats

Trusted points are the easy places. In hazy regions the picture is less clear; the blind review below covers them. A cube's outer layer is not corrected, and these tables don't score it. Samples within 8 voxels of a cube's face stay where they are, which is 10% of the band voxels on the development cubes (7-14% per cube). The tables score only samples at least 10 voxels from a face. The outermost 3 voxels of these cubes hold no labels at all (all label 2). The refiner rows come from our port of ObjAlphaCompRefinement, run on the same samples, normals and drift as the snapper. The better-set-up versions are not how VC3D runs it today. They show how much of the gap to the snapper is down to setup.

Known failure mode

The automatic evaluation flagged hazy cubes (sample 2; samples 8, 17 and 18), where the snapper moves many clean labels 2+ voxels. The blind review found those moves are mostly right: 20 of 21 decisive answers there preferred the snapped label.

The moves the review rejected look different. In 6 of the 8 losses, the original label sits on a face whose gap is on the opposite side from the oriented normal. Either the normal is flipped there, or the label is on the far face of its sheet. v1 then pushed the label outward into papyrus. The v2 guard stops 3 of these 6; the other 3 still go into the sheet.

Of the two remaining losses, one is a small move. In the other, the snapper put the band centre on the papyrus side of the edge, which is where this cube's own labels usually sit (sample 11 places them about 1.5 voxels in). The reviewer preferred the band nearer the edge.

Compare results/compare_sample_00002.png with results/compare_sample_00005.png for what v1 does on a hazy and a clear cube.

Flagged labels: which face does the label belong to?

The snapper flags a label when it sits on a clear face of the opposite polarity (papyrus on the +n side, gap on the −n side) and no face of the expected polarity is within ±4 voxels. That is 3–19% of samples per cube (median 7%); sample 2 is the highest. The flags are written to OUT_DIR/flags/ next to the labels.

The flag can't be turned into an automatic fix, because the scan alone can't say which face such a label belongs to. Two different situations look identical locally: - Far face: the label is on the far face of its own sheet. It should stay on the face it's on. - Crossed gap: the label has drifted across the gap onto the next sheet. It should move back.

The blind reviews show both. Of the 196 moved items across the two reviews, the flag caught: - 7 of the 15 where the reviewer preferred the original - 7 of the 18 marked "can't tell" - only 11 of the 161 where they preferred the snapped label

So flagging about 7% of labels points a human at half the losses. This matches the "humans correct only the uncertain regions" idea in the open problems.

Params(face_polarity=True) snaps flagged labels onto the face they're on instead of searching along +n. At the reviewed points this keeps all 7 flagged losses within 1.5 voxels of the original. It also pulls back 10 of the 11 flagged wins, which the reviewers preferred moved, so it is off by default and the default output is unchanged from v2. The per-item positions are in

results/reversed_face_check.json.

Snapping traced meshes (VC3D tifxyz)

The same scores and graph cut also snap a traced VC3D surface. A tifxyz grid has vertices about 20 voxels apart. It is densified to about 3-voxel samples, which are snapped and then fit back onto the original grid. The normals come from the grid. Which side is recto comes from the scroll's geometry, because every wrap's recto faces the scroll centre. Each mesh keeps its own offset from the papyrus face. Details are in results/mesh_w035.md.

It was developed on segment w035 of PHerc. 0139 at 9.362 µm, the one in the scrollprize.org ink tutorial, using 8 random patches of 24 × 24 vertices. It was then tested on a held-out segment, w052, a different wrap on the same scan. That test was set out before the data was downloaded, and nothing was tuned on it (results/mesh_w052.md).

w035 (development)

w052 (held

out)

Papyrus on the recto side of the face: original → snapped 55% → 88% 70% → 93%

Drift test, within 1 voxel: no correction → snapper 70% → 90% 69% → 94%

VC3D refiner, thresholds tuned on the same patches, offset removed

VC3D refiner, thresholds from each patch's own gap and papyrus levels, offset removed

Snapping onto the m7 surface prediction (the PHerc. 343 winner's method), offset removed

Consistency: snapper / refiner with each patch's own levels / m7 snapping 84% / 75% / 69% 90% / 84% /

Fibre check, patches with the recto signature: snapped / original / m7 snapping 8 / 5 / 7 of 8 8 / 6 / 6 of 8

Which output these numbers score. The snapper's position numbers in this section, and in

results/mesh_w035.md, results/mesh_w052.md and results/w035_whole.md, score snapped_dense.tifxyz (the dense output), the surface as solved. The exception is the one-voxel face check under "A whole segment", which reads the ink test's renders of snapped.tifxyz. snapped.tifxyz (the drop-in output) keeps the input's 20-voxel grid, which can't hold that surface. snapped_fine.tifxyz (5 voxels, meta scale 0.2, written only with --fine-grid 5) can. Scored on the written files, read bilinearly, w035 / w052:

Input mesh

snapped.tifxyz (20

voxels)

snapped_fine.tifxyz (5

voxels)

snapped_dense.tifxyz

(about 3 voxels)

Drift test, within 1 voxel (std 1.5, corr. 40)

70% / 72% / 83% 90% / 94% 90% / 94%

Drift test, within 1 voxel (std 2.0, corr. 80)

42% / 73% / 82% 90% / 92% 90% / 92%

Papyrus on the recto side of the face

55% / 81% / 89% 88% / 92% 88% / 93%

Mean step across the face

8.4 / 46.8 / 64.7 59.7 / 74.8 60.4 / 75.3

The whole of w035 on disk, with channels 0.9 MB 1.4 MB 23 MB 71 MB

tools/eval_mesh.py --output dense|fine|grid scores each one. This table scores position against the snapper's own face (see the note on drift tests in the status section), not reading. The preregistered ink test (results/ink_test_plan.md) rendered snapped.tifxyz, so its result describes the 20-

voxel column: reviewers preferred the snapped map less often than the original's (results/ink_test.md). The fine grid has had no blind review. In an exploratory look at 15 w052 sites, on central 256-pixel crops where such changes run larger than over the whole map, its ink map was dimmer than the 20-voxel file's at both model seeds (mean probability -0.048 and -0.041 against the original, where snapped.tifxyz gave -0.032 and -0.019). So treat it as a geometry output, not one for ink reading (results/review_2026_11.md). tools/render_surface_volume.py renders the fine grid onto the input's pixels. The fine grid's normals are rougher, like the dense surface's: 9.6° from the original mesh's on average, against 4.7° at 20 voxels, so a layer 8 voxels off the surface wanders by about 1.3 voxels instead of 0.65. None of these files has been opened in VC3D.

The w035 results are below.

Where the original mesh sits. Read at its own typical face position, the original mesh has papyrus on the recto side at only 55% of samples. After snapping, 88%. Drift test on w035. Known smooth drifts were applied to the mesh vertices. At 15,324 trusted samples, the share within 1 voxel of the original position went:

Within 1 voxel (drift std

1.5, corr. 40) Within 1 voxel (drift std

2.0, corr. 80)

No correction

VC3D alpha-composite refiner, thresholds tuned on these patches, offset removed

Snapper

Each patch shows the CT read through the original and the snapped mesh, just inside and just outside the recto face, plus a cross-section.

Fibre check. Recto fibres run around the scroll and verso fibres along its axis. So under a surface on a recto face, the fibre direction should turn from across the axis to along it, going deeper into the papyrus. tools/fibre_check.py measures this from the CT alone, except that its depth origin is the snapper's estimate of where the face is. - Snapped surface: shows the pattern in 8 of 8 patches. - Original mesh: 5 of 8, with near-zero size. - Control snapped onto the opposite faces: 4 of 8.

So surfaces moved onto recto-polarity faces show the recto pattern. The effect is small but consistent. It doesn't single out the snapper: a plain gradient search with a light median scores +0.18 on w035 (snapper +0.15) and +0.21 on w052 (snapper +0.20), 8 of 8 patches each, and on w052 the original mesh moved 2 voxels toward the papyrus at every vertex scores +0.18, 8 of 8 (w035: +0.05, 6 of 8). See results/fibre_w035.png.

Review flags. 15% of samples stop at the ±4-voxel search limit (snap_limit), and 10.5% sit on a reversed face (snap_flag). On the input grid, snap_review marks the 17% of vertices where most of the surrounding surface is flagged.

Open question. At this resolution, sheets are often thin layers packed into bundles. Where two recto faces lie within ±4 voxels of a wandering trace, neither the drift test nor the fibre check can say which sheet the tracer meant. That needs expert review, or a downstream check such as ink detection on renders of both meshes.

Ink detection. A pre-registered test has now measured whether a snapped surface reads better, and it reads worse: blind reviewers preferred the ink maps from the original w052 mesh, 75 to 31 (results/ink_test.md). This matches the PHerc. 306B winners, who found that snapping to CT density peaks, after snapping to m7, did not make their letters more legible.

That test rendered snapped.tifxyz. The dense and fine surfaces have not had a blind review.

Options. - --target-offset T, on snap_tifxyz.py and snap_segment.py, puts the mesh T voxels from the face along papyrus → gap (negative = inside the papyrus). On one synthetic scene it lands within 0.24 voxel of T for T from -3 to +3. On real data, Chase's test above put --target-offset 0 about a

voxel inside the two-scan face (median +0.91 voxels with the learned profile off, +1.34 with it on, pinned at 347ea5b4, before the change below). This version has not been run against that reference. - --target-offset and the learned profile. It now moves the learned profile too.

results/ink_test_0841_plan.md uses --target-offset 0 --param smooth_w=0.1, at its pinned commit 627d058, and Chase's test ran --target-offset 0 at 347ea5b4. At both, the profile stays at each tile's own position. The same flags now give other surfaces wherever a tile's own offset is not 0, and whether those sit closer to the two-scan face has not been measured. Read patch by patch, on w035 patch_3 (own offset +1.5), 58.4% of samples differ by at least 1 voxel, and on w052 patch_2 (own offset -1.0), 15.2% do. Patches with an own offset of 0 are identical. Add --param

template_follows_offset=false to get the earlier behaviour. - With --tifxyz, the recto side comes from

--axis, --normals, or the mesh's own curve if it is at least 1,600 voxels across. Shorter pieces of w035 and w052 can fit a tight false circle with a confident, wrong sign. Otherwise the tool stops and asks. --normals ct lets the CT vote decide; that vote is wrong on 4 of the 16 patches here.

A whole segment

tools/snap_segment.py snaps a whole segment tile by tile, reading the scan from the open-data bucket as it goes and caching what it downloads. All of w035 (291 × 262 vertices, 3.1 million samples) took 7 minutes with 8 workers. None of its 279 tiles failed, and the blended result has no seams at tile boundaries. Details are in results/w035_whole.md.

Papyrus on the recto side, read from the renders: 54% for the original mesh, 86% for the snapped one. The 8 patches gave 55% → 88%. Review flags: snap_review marks 17.7% of vertices. w052, whole, for the ink test: 711 tiles in 15 minutes, none failed. The mean |shift| was 1.69 voxels, and snap_review marks 13% of vertices (results/w052_whole_snap_segment.json). One voxel either side of the face (a check suggested by Sean in the Discord, added after the fact): gap outside and papyrus inside at 21% → 42% of pixels on w035, and 22% → 42% on w052. This is close to what the snapper optimises. See results/ink_test.md, which also has two voxels. One offset, in the step-edge term only. The tool uses one offset for the whole segment, the median of 12 sample tiles (+0.5 voxels for w035, range 0 to +1.5). Each tile's learned profile stays where that tile's mesh sits, so a tile whose own offset differs lands between its own depth and the segment's, not at one depth for the whole segment. --recentre-template moves the profile too. It changes the output, so neither this run nor the ink test's runs use it.

pip install "zarr>=2.16,<3" fsspec aiohttp requests # to read the scan from the open-data bucket python tools/fetch_segment.py segments/w035 --segment <tifxyz URL> --volume <OME-Zarr URL> --patches 8 python tools/snap_tifxyz.py snapped segments/w035/patch_* # snapped.tifxyz (same grid) + snapped_dense.tifxyz; add --fine-grid 5 for snapped_fine.tifxyz python tools/eval_mesh.py out/eval_mesh.json segments/w035/patch_* # add --output grid or fine to score those files instead of the dense one python tools/render_mesh.py out/render.png snapped segments/w035/patch_1 --sections python tools/fibre_check.py out/fibre.json segments/w035/patch_* --snapped snapped --png out/fibre.png python tools/snap_to_prediction.py snapped_m7 segments/w035/patch_* # baseline: snap onto a surface prediction (fetch with --extra m7=URL) python tools/snap_segment.py out/w035_whole --segment <tifxyz URL> --volume <OME-Zarr URL> --cache zarr_cache --workers 8 --name w035 python tools/render_segment.py out/w035_whole/w035 out/w035_whole --volume <OME-Zarr URL> --cache zarr_cache # before/after renders

Smoothing a snapped surface

tools/smooth_snap.py takes an original mesh and a snapped one on the same vertex grid, from this snapper or any other, and smooths the snap's moves over the grid (1 vertex by default). The output is a drop-in mesh with the snap's large-scale correction and without its vertex-to-vertex bumps.

Why: those bumps are what lowered the ink model's map level (results/move_scale.md).

What it keeps, for this snapper: the map level on w052 and on three PHerc. 0841 segments, and 35–43% of the snap's gain at the face (results/smooth_snap.md). What isn't shown: that a smoothed surface reads as well as the original. A blind review hasn't been done, so it isn't offered for ink work yet. The default scale is being tested at 0.5 and 0.75 vertices (results/smoothing_tradeoff_plan.md).

python tools/smooth_snap.py out/smooth.tifxyz --original segment.tifxyz --snapped snapped.tifxyz -report out/smooth.json python tools/surface_moves.py out/moves.json --original segment.tifxyz --snapped snapped.tifxyz # how rough are a snap's moves? python tools/face_step_sweep.py out/face.json --render original=orig.zarr --render smooth=smooth.zarr # placement at the face, from renders

Setup

pip install -r requirements.txt

Usage

# one or more cubes python tools/snap_cube.py OUT_DIR images/sample_00001.tif labels/sample_00001.tif

# a whole folder laid out like the dataset (images/ + labels/), in parallel; resumable # writes labels/, confidence/ and flags/ (labels that may be on the wrong face) python tools/snap_folder.py IN_DIR OUT_DIR --workers 12

# evaluation, summary and before/after close-ups python tools/eval_snap.py out/eval.json images/sample_00001.tif labels/sample_00001.tif python tools/summarize_eval.py out/summary out/eval.json python tools/render_compare.py out/cmp.png images/X.tif labels/X.tif OUT_DIR/labels/X.tif z

Each worker peaked at about 1 GB on the development cubes. A 320³ cube takes 30–120 s per core.

Windows

git clone https://github.com/aqsnyder/scroll-label-snap cd scroll-label-snap python -m venv .venv .venv\Scripts\activate pip install -r requirements.txt python tools\snap_folder.py D:\vesuvius\kaggle D:\vesuvius\snapped --workers 12

Data

The tools run on the Vesuvius Challenge surface-label cubes (Hugging Face bucket):

images/sample_NNNNN.tif paired with labels/sample_NNNNN.tif. Each cube is uint8. Most are 320³; 51 of the 892 are 256³ and one is 384³.

Label value Meaning

annotated background

recto surface

not annotated

The data is licensed CC BY-NC 4.0 and is not included here. The example images in results/ are crops of that data. The mesh figures are renders of PHerc. 0139 segments w035 and w052 and their scan, and the ink-map figures are made from those renders. They come from the Vesuvius Challenge open data, also CC BY-NC 4.0. The PHerc. 0841 results use that scroll's open data, under the same licence.

Blind human review

The automatic tests can't say whether a big move on a hazy cube is a fix or a mistake, so a person judges a sample by eye without knowing which label is which.

tools/make_review.py picks, per cube, 3 points where the snapper moved the label by 2+ voxels, 3 where it moved 1-2 voxels and 1 where it didn't move (a control), spread at least 32 voxels apart: 140 comparisons. It adds 14 catch items, where the original label is compared with itself pushed 3 voxels into the gap or 2.5 voxels into the sheet, at points where the snapper and the original agree; a reviewer who can't spot those can't be trusted on the rest. Each item shows a 48 x 48 voxel slice, cut perpendicular to the axis closest to the surface, with a zoomed-out context view and the two candidates side by side. Item order is shuffled, and exactly half the comparisons (and half the catch items) put each candidate on the left. The reviewer answers "A is better", "B is better", "About the same" or "Can't tell" (review/index.html). The page shows only item ids and images; the answer key stays with whoever runs the review until the answers are in.

tools/score_review.py unblinds the answers and reports preferences per stratum, for the hazy cubes, by direction of the move and per cube, with an exact sign test, catch accuracy, left/right bias and answer times.

python tools/make_review.py review/ out/review_key.json data/images data/labels out/labels --seed 0 python tools/score_review.py out/review_key.json answers.json results/review_v1.md

The first review set is 32989576ca01. Its answer key was sealed before any answers came in: the SHA- 256 of the key (as json.dumps(key, sort_keys=True)) is

32989576ca01fe3ce79d7ab8491025ed9730d72ac8529d673898dc4182edcb28, and an encrypted copy is

review/sealed_key_32989576ca01.enc (AES-256-CBC, openssl enc -pbkdf2 -iter 200000). The key, the passphrase and the answers are now in results/.

Result of review v1 (results/review_v1.md)

Where the snapper moved the label, the reviewer preferred the snapped label 98 times and the original 8 times. That is 92% of decisive answers (95% CI 86-96%); 14 of 120 were "about the same" or "can't tell". Big moves (2+ voxels) went 47 to 6 and moderate moves (1-2 voxels) 51 to 2. The hazy cubes flagged by the automatic evaluation went 20 to 1, so the large moves there are mostly fixes, not mistakes.

Five of the eight losses put the label inside a thick sheet instead of on its face. Caveats: - One reviewer, who owns this repo. - The snapped band's stair-step edge can give it away. - The controls and catch items were only clean at the centre point of each 48-voxel window.

Review v2 (set af7d4c85d7f6)

Built with tools/make_review_v2.py --seed 1 on the v2 output, for a reviewer who did not work on the tool: - Fresh points. No item is within 32 voxels of a v1 item. - 111 items: - 40 big moves and 40 moderate moves (2 of each per cube). - 15 controls, where the two labels agree across the whole window (IoU 0.80 or more), not just at its centre. - 16 catch items: the original label pushed 3 voxels into the gap or 2.5 voxels into the sheet, 8 each way. They are only used where both labels agree across the window and the scan confirms the push direction: a dark gap in front, or bright papyrus behind. - A short tutorial first: worked examples (good, too far out, too far in) and 4 practice items that show the right answer after each pick. - Per-reviewer storage. Answers are stored under each reviewer's name, so several people can take the same set. - Sealed key. The SHA-256 of the answer key is af7d4c85d7f6f07106839d0af2de42655095ba677316cb9c3ae9ddec95dc08f6, and an encrypted copy is review/sealed_key_af7d4c85d7f6.enc. The page is review/v2/index.html.

Result of review v2 (results/review_v2.md)

A second reviewer, who did not work on the tool and had never seen these scans, judged the v2 output on fresh items: - Moves: where the snapper moved the label, she preferred the snapped label 63 times and the original 7 times. That is 90% of decisive answers (95% CI 81-95%); 10 of 80 were "about the same" or "can't tell". - Big moves (2+ voxels) went 27 to 6; moderate moves (1-2 voxels) 36 to 1; the hazy cubes 12 to 1. - Checks: she got all 16 catch items and all 4 practice items right. She rated 11 of the 15 controls "about the same". - Losses: four of the seven are the same failure mode found in review v1, where the label sits on a face whose gap is opposite the normal.

Next steps

1. Decide flagged labels with more context. Following each sheet over a larger area, or using the traced mesh's own history, could tell which face a flagged label belongs to. Until then, flagged labels are the place for human review. 2. Use the confidence map: leave or flag low-confidence regions instead of moving them. 3. Keep sheet orientation stable under drift first (Params.orient_cube, off by default; its test on 100 fresh cubes is pre-registered in results/orient_test_plan.md and not yet run). Then make the learned profile independent of the input labels (see "Drift draws" above; in Chase's test, turning it off helped), and test that on a fresh held-out set. 4. Meshes: a smooth snap (not started). The drop in map level is in the moves' vertexscale bumps (results/move_scale.md). Moves smoothed over about one vertex spacing keep the map level; tools/depth_sweep.py filter --low-pass 1 makes such a mesh after the fact. Whether it reads better needs a pre-registered blind review. 5. Meshes: face placement. Run the current --target-offset 0 against the two-scan face; at 347ea5b4 it sat about a voxel inside in Chase's test. Compare with snap_labels in the blind ink test. 6. Ink: a blind review with matched displays. It is the only test here that can separate a dimmer map from a less legible one (results/review_2026_11.md). Pre-register it first.

File: results/review_2026_11.md

Review of the approach, November 2026

An automated review of this repository by Claude Code, asked for by its owner, on 3–4 November 2026. It ran separate checks on its findings and then tried to refute the main ones. The normals, uniform-shift, fine-grid and layer-profile results under "What moves the map" weren't attacked that way. No person has checked this write-up. The working scripts aren't committed; where a number can be reproduced with a tool in this repository, the tool is named.

How to read it. Only the pre-registered tests carry confirmatory weight, and their outcomes stand as recorded. Everything else here is exploratory, and much of it was chosen after seeing earlier results. Numbers on the development cubes come from cubes this repository has already tuned on.

Names. snapped.tifxyz is the drop-in or 20-voxel file, and snapped_dense.tifxyz is the dense surface, with samples about 3 voxels apart. Seeds 42 and 43 are two checkpoints of one ink model, reading the same renders. w052 is the held-out segment of PHerc. 0139. The PHerc. 0841 targets are three traced segments with ink labels, and the windings are KLAVIS's spiral-fit surfaces that cross them.

In short

1. The geometry improved, and the ink did not. The blind review of w052 went against the snapped mesh, 31 to 75. On PHerc. 0841's labels, snapping traced segments made no detectable difference, read as 0 ± 0.05 AUC, and brought no gain. 2. Why the w052 maps lost is not settled. Snapped maps are dimmer, and reviewers followed how strong a panel looked. That may or may not be all of it. Only a blind review with

matched displays can say. 3. The dimming comes from moves finer than about 30–40 voxels, as the owner's preregistered diagnostic (move_scale.md) found. A smooth move of the same overall size doesn't dim, on either scroll, at seed 42. Neither mean depth nor the 20-voxel file's normals lower the map's level much. 4. The PHerc. 0841 winding comparison had a tool bug. Pooled, it accounts for most of the gap between the dense and drop-in outputs, though that reading depends on the posthoc smoothing and on the transfer method. The plan's one clear gain doesn't hold up, for a separate reason: it is −0.081 at seed 43, even with the transfer as run. With the fix, no loss or gain repeats at a second seed, and a pooled loss of up to about 0.09 AUC isn't excluded. See "Later check" in ink_test_0841.md. 5. On sample_00018, the fall from 93% to 67% between drift draws comes from the cross-sheet orientation step, not mainly the learned profile as an earlier README said. Orientation also flips between runs on some other development cubes, but most of the lowest drift scores don't come from it. Params.orient_cube, off by default, replaces that step. Its test on 100 cubes not yet run with it is pre-registered and has not been run. 6. Snapped labels gain tunnels and merge sheets. Going by voxel shares and label topology, per-voxel losses should barely notice and topology-aware losses and metrics should. That is inferred: no model was trained and the official metrics weren't run.

Params.keep_topology keeps the topology, and doesn't settle where contested sheets belong. 7. The drift test can't rank methods. A per-sample search with no graph cut beats the snapper on it, and the order reverses when trust comes from a point's neighbours instead of its own CT. What the graph cut adds shows up elsewhere, and plain smoothing gets most of it. 8. The w052 ink test read the drop-in file, which keeps most of the gain at the face and part of the drift test's. On w035 / w052 it keeps 78% / 82% of the papyrus-side gain, and 9% / 53% of the drift gain at the published drift or 64% / 79% at a larger one.

Ink

The w052 review

The outcome stands: 31 against 75, p = 2.3e-05. Scored by item, because the pooled test counts two reviewers on one crop, it is 33 items net for the original, 10 net for snapped and 17 tied (exact sign-flip p = 1.5e-4).

Reviewers agree on the direction, not item by item (kappa 0.12, interval −0.06 to 0.32). Inference holds for these two reviewers and this set of crops.

Strength and legibility

Snapped maps are dimmer on traced segments. Mean probability falls by about 0.015 on w052 and w035, at both seeds. Of 1024-pixel tiles, 98–100% go down. The strongest pixels fall most. Reviewers follow strength. They do so even when the extra strength is only seed noise: the seed-specific part of the change predicts their answers. It isn't established that strength explains most of the preference. Using the second seed to isolate the part of the change the mesh causes, the snapped share at equal strength is 43% (22–65%) by the panel's standard deviation and 53% (28–79%) by its mean, neither of which can be told apart from the observed 29% or from 50%. By the 99th percentile it is 31% (11–45%), which is below 50%, but the strength slope behind that figure is poorly fixed (0.09, −1.97 to 0.91). More than level may be lost. On 200 unselected w052 tiles, the part of the map that repeats between seeds falls against the noise at fine scales: log2 ratio −0.20 (−0.33 to −0.07) at 4–8 pixels on the fixed display, and −0.29 (−0.44 to −0.14) with histograms matched. This isn't an ink measure: at 15 w052 sites a random move raises it.

A dimmer map may simply be less legible. Strength is how the map loses on the display the review used, not a reason to discount the result.

What moves the map

Whole-map mean probability on w052 against the original, seed 42, re-scored here from the owner's maps. It isn't those plans' tile rule:

Mesh Change in mean p r with original

Snapped

Moves smoothed at σ = 20 voxels −0.0014

Moves smoothed at σ = 40 voxels +0.0003

Moves smoothed at σ = 80 voxels 0.0000

The moves' rest after σ = 40

Mirrored moves

Random phases, same spectrum

Uniform shift, up to ±2 voxels −0.0009 to +0.0001 0.84–0.94

Size isn't the cause. Scaled up to the real move's full spread, the smoothed move still doesn't dim: −0.0008 (−0.0044 to +0.0032) against −0.0182 for snapped at 30 review sites, and +0.0003 pooled on the PHerc. 0841 targets. The 20-voxel file's normals add little. On central 256-pixel crops at seed 42, snapped positions with the original normals change the map as snapping does (ratio 1.07, 1.01 to 1.16, 60 sites). The original positions with snapped normals give −0.0041 (−0.0088 to +0.0005) against −0.0320 at 15 sites, which doesn't exclude about a quarter of the drop. Rougher normals on the finer files weren't separated. Mean depth doesn't lower the level. The map's mean responds flatly to a uniform shift at seed 42: within ±3 voxels on the traced PHerc. 0841 segments, ±2 on traced w052, ±2 on snapped PHerc. 0841 and ±1 on snapped w052. So changing the mesh's offset from the face wouldn't cure the dimming. The maps still change (r 0.84–0.94 on w052), and the owner's pre-registered rule reads the tile losses at ±2 voxels as "partly" (depth_sweep.md). How far a tile moved doesn't predict how far it dims. The fine part of the move still causes it. Same-mesh controls are near zero. The fine grid dims more. At 15 w052 sites, on central 256-pixel crops, seeds 42 and 43: −0.048 and −0.041 against −0.032 and −0.019 for the 20-voxel file. Those crops run larger than the whole map, and no paired interval was computed. The cause of the dimming is unknown. On PHerc. 0841 at seed 42, giving the original stack the snapped layer profile raises the output (+0.013) and lowers AUC (−0.029, −0.051 to −0.007), so this gives no support to the taller step as the cause of the dimming. Those swapped stacks are unnatural inputs.

The table's maps are the owner's own, from Diagnostic 2 (move_scale.md) and the depth sweep (depth_sweep.md), so it isn't a second route to their answer, and those plans' own readings stand. The separate evidence is the PHerc. 0841 low-pass runs and the rescaled smooth move, which point to the same scale.

Labels on an unseen scroll

On the three traced PHerc. 0841 segments, using dense depth, against the traced segment. Every row ran through the depth transfer as run, so each keeps the snapped depth's false holes (about 0.5% of hits). With the transfer fixed, the real shift is +0.010 (−0.018 to +0.038) and +0.016 (−0.009 to +0.042). Seed 43's move of +0.022 is over the rule's 0.02 flag, and the row stays inside 0 ± 0.05. The other rows haven't been rerun:

Move ΔAUC, seed 42 ΔAUC, seed 43

The real shift +0.011 (−0.017 to +0.037) −0.007 (−0.034 to +0.022)

Move ΔAUC, seed 42 ΔAUC, seed 43

Mirrored −0.068 (−0.099 to −0.032) −0.077 (−0.113 to −0.039)

Random phases, same spectrum (two draws at seed 42) −0.113 and −0.105

Half the shift +0.032 (+0.011 to +0.054) +0.003 (−0.015 to +0.022)

Read the real shift as 0 ± 0.05. A rolled-label null runs about 1.8 times the bootstrap's standard error, and a same-mesh seed swap alone moves one target by up to 0.06. So, pooled over 3 targets, a loss of 0.07 is excluded and a loss of 0.03 is not. The real dense move isn't like noise. Its fine detail follows something in the scan. That doesn't show it is right for ink, because it brings no gain. For the drop-in file, the one the primary test used, this isn't detectable. Real, mirrored and random moves can't be separated on AUC (−0.017 mirrored and −0.020 random against the file itself, intervals including 0, seed 42 only). Half the shift is not a gain. It doesn't repeat at seed 43. The strength ordering flips between scrolls. On PHerc. 0841 a random move dims more than the real one. On w052 it dims less, and w052 has no labels to say what that costs. w035's labels are not evidence either way. The model trained on them, and rerendering the same mesh already lowers the separation of ink from non-ink (d′ 8.41 to 6.87) about as much as snapping does (6.87 to 5.30). ink_test.md also calls that outcome not conclusive.

The depth transfer bug

The rerun, its rule and its readings are in ink_test_0841.md and ink_test_0841_rerun/. It can't reach the w052 review, whose renders don't use this tool.

Leftovers: the mirrored PHerc. 0841 row in depth_sweep.md carries the snapped depth's false holes (identical mask, about 0.5% of hits), and so do the mirrored, random-phase and half-shift rows in the table above. They probably stand, since traced with the same holes moves AUC by only +0.006, but that is inferred: none of these rows has been rerun.

Label cubes

Orientation

orient_normals ends with a cross-sheet step that flips any sheet disagreeing with the samples around it. Under drift, this step reverses whole sheets.

How often. 7.34% of development samples go against their own sheet's vote. Against a reference orientation (the candidate's own, on clean labels), 5.68% have the wrong sign. A fibre signature supports the reference on all 20 cubes (block t 6.0 to 24.1). It uses no label polarity and no CT step sign, though its positions and normal lines come from the labels, and it assumes the scroll axis is scan z. sample_00018 at drift seed 17. An earlier README's "the learned profile is the main cause" doesn't hold. Within 1 voxel, its 67.0% stays 66.9% with the clean run's profile, rises to 75.1% with the profile off, and to 93.8% with the clean run's orientation. The draw reverses 32% of its trusted points: within 1 voxel is 10% on those and 93% on the rest.

Params.orient_cube, 20 development cubes at 3 drift seeds each. Consistency goes 81.73% to 86.79% (+5.06, 2.07 to 8.35). Drift on points trusted by both goes 89.99% to 91.50% (+1.51, 0.12 to 3.57). The mean orientation change goes from 6.52% (max 34.8) to 0.00% (max 0.01). The intervals are cube bootstraps over the 20 cubes. What this doesn't cover. The test can't see errors both runs share, because the trusted set follows the normals under test. sample_00014 stays about 1.6 points lower, from an offset drop and a template shift, not orientation.

The guard near the scroll centre is tested on a phantom only (61% correct without it, about 100% with it). Meshes aren't affected, because their orientation comes from geometry.

Topology

Measured on all 892 cubes without tuning anything, with working scripts. tools/eval_topology.py gives the Betti numbers, components, fragments, merger events and contact voxels. It matches those scripts on the 20 development cubes and hasn't been run on all 892. It reads no CT, so it doesn't give the dark-line shares below, and it only scores labels it is given, so it doesn't make the moved controls.

Sheets merge. Sizeable components fall from 6,827 to 5,424, with 1,438 merger events in 559 cubes. The band loses its simple shape. Median first Betti number goes 0 to 238, components 7 to 42, and Euler number 7 to −162. Tunnels appear in all 892 cubes, cavities in 786, fragments in 886. Tunnels come from the warp, not the CT. Any non-rigid move makes them: 7,027 tunnels with the published moves on the 20 development cubes, 7,300 with the moves negated, 0 with a rigid move, and 215–464 with a uniform ±1 voxel. The CT search drives about half of the mergers. On the 20 cubes: 50 published and 80– 84 with a per-sample search, against 24 negated, 11–13 from a smooth drift and 4–5 from a uniform ±1 voxel shift. The CT doesn't show that merged sheets were apart. It resolves a dark line at only 42.6% of contact samples, against 65.6% for near pairs that didn't merge. That doesn't show they touch either. What it should cost, inferred, since nothing was trained. Per-voxel losses should be mildly affected (contact is a median 0.22% of the band). Topology-aware losses and metrics computed on these labels should be affected seriously. Cubes with ids 161–280 are 13% of the cubes and hold 39% of the merger events.

Params.keep_topology moves the band one simple voxel at a time. On the 20 development cubes, Betti numbers equal the original's at both connectivities, with 0 merger events. Its limits:

The drift test can't show it is free: of the 3,655 samples it moves more than 1 voxel, only 21 are trusted. Pooled drift goes .8948 to .8951, and consistency .8134 to .8110. Contested pairs stay side by side with a one-voxel wall. Where they belong needs a blind look at contested sites. Tangential wander and moves to the wrong face are unchanged.

What the drift test shows

A per-sample search beats the snapper on it: 93.85% against 89.49%, on 20 of 20 cubes (+4.37, 3.7 to 5.2). A plain gradient with a median gets 90.97%. tools/eval_snap.py now reports these rows. The order depends on how trust is defined. With trust set by the edges of a point's neighbours 4–12 voxels away, which read the same cube's CT but not that point's own, the snapper leads, 85.54% to 82.22%, and the search is ahead on 0 of 20. So this test can't rank these methods. What the graph cut adds, on clean labels against a per-sample search: roughness +5.97% against +18.80% (a smooth drift alone adds +6.1%); tunnels 7,027 against 68,170; joined sheets 50 against 84; landing on a different sheet from the original label, 0.79% against 0.89%; and on CT degraded with synthetic noise, 8.6 and 12.8 points more than the search (against a plain gradient with a median, a tie and 4.3 more). Real hazy cubes don't show it on the published test: on samples 2, 8, 17 and 18 the search is ahead.

Plain smoothing gets most of that: median and Gaussian reach 91.09% on the drift test, with roughness +7.83%.

Meshes

Which file was scored. The published drift numbers are the dense surface's. The 20-voxel file holds less of that gain: within 1 voxel on w035 / w052 is 70% / 69% for the input, 72% / 83% for the 20-voxel file and 90% / 94% for dense (tools/eval_mesh.py --output). At a larger drift (std 2.0, corr. 80) the 20-voxel file keeps 64% / 79% of that gain, and on clean meshes 78% / 82% of the papyrus-side gain. In 8 w035 windows, papyrus on the recto side goes 53.0% (original), 77.9% (20-voxel), 85.0% (5-voxel), 85.2% (dense). So the published 54% → 86% reads dense, and the w052 ink test read the 20-voxel file. Tiles. Tiles that share all their parameters and overlap by a margin of 6 vertices match a whole solve on 16 of 16 patches. tools/snap_segment.py's current tiles differ from a whole solve by a mean of 0.300 voxels on w035 and 0.147 on w052 (5.2% and 1.5% of samples over 1 voxel). In the real w035 run, they differ from each other in their overlaps by a mean of 0.469 (7.4% over 1). Blending hides that, so the steps show no seams. This isn't changed in this branch. One offset. snap_segment's default offset moves only the step-edge term, not the learned profile, and still does in this branch, so the published runs reproduce. --recentre-template moves both, and it changes the output. A candidate. Moves smoothed over about one vertex spacing nearly keep the map level and keep about 43% of the face gain (move_scale.md). No smooth arm raised AUC. It would need a labelled test at both seeds and a matched review.

Code

The bugs fixed in this branch are listed in its commit messages. The depth transfer's fix is opt-in, --

refine 3 --normal-sigma 10, so that the plan's depth files reproduce.

This branch's speedup of the label pipeline changes no default output on the cubes and patches checked. On paired runs of 4 cubes, total CPU was 0.72 and 0.74 of base. Peak memory per worker on the development cubes was at most 2.04 GB before it and 1.04 GB after it.

Next steps, by value

1. Merge the PHerc. 0841 correction (it is in this branch) and tell KLAVIS, who supplied the windings. 2. Pre-register a blind review with matched displays: 60 matched comparisons plus fixedscale, level-only and catch arms, about 6 minutes per reviewer, with a third reviewer who hasn't seen the first result. It is the only test here that can separate dimmer from less legible. The tool change for it isn't in this branch yet. 3. Run the pre-registered orientation test (orient_test_plan.md). 4. Decide on orientation and topology before releasing any regenerated cubes. Those two options change what a downstream user trains on, and the current labels have the tunnels and mergers above. 5. Rerun the mirrored PHerc. 0841 arm with the corrected transfer. Fix its reading first. 6. Test a smooth snap on PHerc. 0841's labels at both seeds and in a matched review, before offering it. 7. More labelled targets for windings. Five pairs on three targets can't say whether snapping helps or harms windings. Choose the transfer before any map exists. 8. A model trained on snapped surfaces is the direct test of whether cleaner geometry can help ink. Nothing here tests that.

What this review did not cover

No person has reviewed any new map. Nothing general follows about other models or scrolls: this is one ink model and two seeds, one held-out segment, and three labelled segments of one unseen scroll. The Vesuvius Challenge's official topology metrics (TopoScore, VOI) were not run, and VC3D was never opened. There is no head-to-head against other surface-refinement work in the community. The other 872 cubes were not re-snapped at this branch. Linux and other library versions were not tested.

File: results/ink_test.md

Ink-detection test: snapping made the ink less legible

This test was pre-registered in ink_test_plan.md, which was pushed before any surface volume was rendered and before the ink model was run on a snapped mesh. The plan's run log records how the run went. It ran on 3 November 2026 on one Windows PC, CPU only. The data files behind every number here are in ink_test/.

Summary

Primary outcome, w052 (held out): snapping hurts. In a blind review of 60 pairs of ink-map crops, the map from the original mesh was preferred 75 times and the map from the snapped mesh 31 times. That is 29% for the snapped map (95% CI 21–39%), with a two-sided exact sign test p = 2.3 × 10⁻⁵. Each of the two reviewers alone points the same way. Secondary outcome, w035 against its ink labels: the snapped map scores lower, with AUC 0.998 → 0.995 and best F1 0.969 → 0.950. The model was trained on w035, with labels drawn on the original mesh. So, as the plan says, this is not conclusive on its own, but it points the same way. Where it changes: all over. On w052, about half of the 256-pixel tiles lose more than 0.02 of their 99th-percentile ink probability, and a quarter gain as much. The change doesn't follow how far the mesh moved or how much of it was flagged (|ρ| < 0.11 throughout). The snapped mesh does sit on a density edge more often. One voxel either side of the face, it has gap outside and papyrus inside at 42% of w052's pixels, against 22% for the original. That is close to what the snapper optimises, so it shows the snapper works as built. A surface on that edge is evidently not what this ink model needs. Seed 43, the second checkpoint, gives the same picture. The follow-up on PHerc. 0841 is in ink_test_0841.md. On three traced segments, snapping made no detectable difference to agreement with the ink labels. On KLAVIS's spiral-fit windings, as run, the drop-in output was about even and the dense output lost ground, part of it from a bug in our depth transfer (ink_test_0841.md).

Primary outcome: blind legibility review (w052)

The review set, its sealed key and both reviewers' answers are in ink_review.md, with how to check them. Each item showed the two ink maps side by side, with nothing else. The question was "which shows the ink more clearly?"

Reviewer Snapped preferred

Original preferred

About

the same

Can't

tell

Snapped share of

decisive answers

(95% CI)

Sign test p

Catch items

right

The repository owner 33% (22–46%) 8 of 8

Someone who hadn't worked on the tool

25% (16–39%) 8 of 8

Pooled 29% (21–39%) 2.3 × 10⁻⁵

The 10 controls were random places with no ink condition. - The repository owner: snapped 2, original 3, about the same 3, can't tell 2. - The other reviewer: snapped 2, original 6, about the same 2.

Secondary outcome: agreement with the w035 ink labels

This is scored on 1,071,121 pixels inside the supervision mask (31% ink). Every pixel is valid in both renders and non-zero in the map from the official surface volume.

Map AUC, seed 42 Best F1, seed 42 AUC, seed 43 Best F1, seed 43

Official surface volume

Our render, original mesh

Our render, snapped mesh 0.9949

Snapped − original

w035 is biased toward the original mesh: the labels were drawn on a render of it, and the model was trained on them. So a lower score for the snapped mesh is not conclusive, as the plan says. It goes the same way as the primary outcome.

Descriptive: where does it change?

The unit is a 256 × 256-pixel tile with at least half its pixels valid. "Flagged" samples are those of the dense snapped mesh marked reversed-face or at the search limit.

w052, seed

w052, seed

w035, seed

w035, seed

Tiles

Median change in the tile mean

Median change in the tile 99th percentile

Tiles losing / gaining more than 0.02 (99th percentile) 53% / 24% 52% / 24% 45% / 24% 47% / 18%

Whole-map mean probability, original → snapped 0.319 → 0.305 0.322 → 0.305 0.323 → 0.308 0.329 → 0.312

Spearman ρ of the 99th-percentile change with mean |shift|

+0.06 (p = 0.07) −0.04 (p = 0.19) −0.05 (p = 0.36) −0.03 (p = 0.61)

Spearman ρ of the 99th-percentile change with the flagged share

+0.07 (p = 0.04) −0.07 (p = 0.04) −0.10 (p = 0.04) −0.04 (p = 0.43)

The correlations of the change in the tile mean are as small (|ρ| ≤ 0.10). Some notes on reading this: - The tiles differ little in how far they moved. The middle half of w052's tiles have a mean |shift| of 1.50–1.90 voxels and 12–24% flagged samples. So this can't rule out that moving further hurts more. What it does show is that the loss isn't confined to a few badly snapped places. - The probability scale is narrow. The model was trained with label smoothing, so its probabilities run from about 0.25 to 0.75. A change of 0.02 in the 99th percentile is about 4% of that range. - A check after the fact, by ink level. Ranking tiles by the mean of both maps' 99th percentiles, 56–72% of tiles drop in every quartile. So the loss is not limited to inky tiles or to blank

ones. Ranking by the original map alone would seem to show gains in blank tiles, but that is regression to the mean.

In the tiles that lose most, whole ink blobs in the original map are gone in the snapped one. In the tiles that gain most, blobs appear that the original doesn't show.

The w035 figures are in ink_test/.

Sanity check

Our w035 map from the original mesh was compared with the map from the official surface volume. The Pearson r is 0.862 over 25.2 million pixels, with a mean absolute difference of 0.039. This fits the renderer check, where our render matched the official volume layer by layer with a mean correlation of 0.932.

The mesh one and two voxels from the face

This check was added after a suggestion by Sean in the Vesuvius Challenge Discord; it is not part of the plan.

tools/face_step_check.py reads each render D voxels outside and D voxels inside the recto face, at the mesh's own face offset. That offset is +1.25 voxels on w052 and +0.50 on w035. The scan is thresholded with Otsu's method, pooled over both renders. These are shares of all valid pixels:

Gap outside Papyrus inside Both Brighter inside than outside

w052, 1 voxel: original → snapped 53% → 68% 59% → 70% 22% → 42% 59% → 81%

w052, 2 voxels 56% → 71% 65% → 82% 36% → 59% 63% → 83%

w035, 1 voxel 56% → 71% 49% → 65% 21% → 42% 54% → 77%

w035, 2 voxels 59% → 77% 51% → 73% 32% → 58% 55% → 80%

The snapper puts the steepest edge at the mesh's own offset, which is close to what this measures, so the gain is expected. It shows that the snapper does what it is built to do. It doesn't show that the snapped surface is where the ink is, and the review says it is not better for reading.

What this means

Don't use snapped meshes for ink detection, at least with ink_9um and the default settings and drop-in output tested here. Why it hurts is not known. Two candidates, neither tested: The model was trained on renders of traced meshes. It may depend on how those sit relative to the papyrus, so moving the surface, even onto an edge, moves the ink away from where the model expects it. The steepest density edge may not be where the ink is. Checked since (depth_sweep.md): It isn't the surface's average depth: moving the whole mesh 1–2 voxels barely changes the map level. It comes with the snapper's varying moves. A mirrored mesh, moved by the same amounts the other way, also lowers w052's map level, a little less. More exactly, it is their vertex-scale bumps (move_scale.md). The same moves smoothed over about 20 voxels keep the map level.

File: results/ink_test_0841.md

PHerc. 0841 follow-up: snapping and agreement with ink labels

This test was pre-registered in ink_test_0841_plan.md, pushed at 627d058 before any surface in it was snapped, rendered or run through the ink model. KLAVIS suggested it in the Vesuvius Challenge Discord and supplied the four spiral-fit windings and the first numbers. It ran on 3 November 2026 with the ink model, settings and PC of the w052 test (ink_test.md). The data files are in ink_test_0841/.

Summary

The labelled segments themselves (A). Snapping made no detectable difference on any of the three. At the plan's seed, all three moved up slightly: ΔAUC +0.006, +0.004 and +0.022, pooled +0.011. Every interval includes 0. KLAVIS's windings (B), five winding–segment pairs: Drop-in output (the one KLAVIS scored): as run, one gain, w056 on w00, of +0.104 (95% CI +0.032 to +0.184). The other four show no detectable difference. Pooled: +0.019. The gain doesn't repeat: the same pair gives −0.081 at seed 43 with the same transfer, and +0.014 and −0.008 with the transfer fixed. Dense output: as run, two losses (−0.19 and −0.22), and three with no detectable difference. Pooled: −0.078. Part of this was a bug in the depth transfer: with it fixed, pooled −0.051 and −0.002 at seeds 42 and 43. KLAVIS's second try (--target-offset 0 --param smooth_w=0.1, dense): as run, three losses. Pooled: −0.070. With the transfer fixed, pooled −0.050 and +0.002. In short: snapping made no detectable difference on traced segments (read as 0 ± 0.05 AUC). On rough windings, the dense output lost ground as run, and part of that came from a bug in our depth transfer. With it fixed (post hoc, exploratory), the pooled loss is −0.051 at the plan's seed and −0.002 at a second model seed, and neither output shows a loss or a gain that repeats at both seeds (see "Later check" below).

How it ran

Labels to 9.366 µm. Each target's 2.403 µm grid fits its 9.366 µm grid with a median residual of 0.10–0.12 voxels (f ≈ 3.90, o ≈ 1.4–1.45), well under the 1-voxel limit. Layer direction: forward on all three targets. The 99th percentiles were 0.769 forward against 0.714 reverse on w00, 0.761 / 0.686 on …144552896, and 0.765 / 0.737 on … 174252405. Snapping the targets. The snapper settled the recto side at 98% of vertices on each target, so none was left out of A. Each target's dense snap: face offsets of +0.00, +0.50 and +0.50 voxels; mean |shift| 1.94–1.97 voxels; 75% of samples moved by 1 voxel or more; 16–19% of vertices marked for review. Pairs. A winding is paired with a target when the winding as received reaches at least 20,000 of the target's supervised pixels:

Target (supervised pixels) w055_fr0 w056_fr0b w058_fr0 w063_fr0b

w00 (1,600,311) 574,678 12,014

…144552896 (983,772) 377,468 307,141

…174252405 (1,279,388) 102,390 893,960

A. The labelled segments, traced and snapped

Target Scored

pixels

Ink share

Traced: AUC

/ best F1

Snapped (dense):

AUC / best F1

ΔAUC (95%

CI) Reading

w00 1,595,783 0.752 / 0.507 0.758 / 0.515 +0.006 (−0.035 to +0.046)

no detectable difference

…144552896 982,317 0.707 / 0.552 0.711 / 0.554 +0.004 (−0.041 to +0.053)

no detectable difference

…174252405 1,275,522 0.717 / 0.493 0.739 / 0.515 +0.022 (−0.025 to +0.071)

no detectable difference

Pooled, weighted by pixels

3,853,622 +0.011

B. KLAVIS's windings

These are AUC differences from the winding as received, with 95% intervals from the block bootstrap. Bold marks an interval that excludes 0.

Winding on

target

Scored

pixels

Ink share

As received:

AUC Drop-in output Dense output

Offset 0, smooth 0.1,

dense

w056 on w00 450,459 +0.104 (+0.032 to +0.184)

−0.031 (−0.140 to +0.081)

−0.016 (−0.130 to +0.108)

w055 on … 278,139 −0.069 (−0.173 to +0.045)

−0.187 (−0.301 to −0.070)

−0.189 (−0.299 to −0.083)

w056 on … 197,746 −0.027 (−0.109 to +0.058)

−0.220 (−0.334 to −0.117)

−0.204 (−0.326 to −0.093)

w058 on … 69,444 +0.038 (−0.080 to +0.175)

−0.155 (−0.367 to +0.019)

−0.170 (−0.348 to −0.015)

w063 on … 694,316 +0.011 (−0.060 to +0.071)

−0.018 (−0.090 to +0.054)

−0.010 (−0.085 to +0.060)

Pooled, weighted by pixels 1,690,104 +0.019

Each pair is scored on the part of the target its winding covers. So these numbers can't be compared with part A, or across pairs. The best-F1 differences are in the score files and go the same way.

Reading

The drop-in output. KLAVIS found it about even with his own scoring, which reads depth about every 20 voxels: −0.011, −0.005, −0.001 and +0.022 per winding. With depth carried over at every pixel, it is about even here too, within 0.05 and leaning negative: pooled +0.019 as run, −0.047 at seed 43 with the same transfer, and −0.022 and −0.027 with the transfer fixed. The one gain as run is on the pair where the winding as received scored lowest (AUC 0.553). It doesn't hold up: at seed 43, with the same transfer, that winding scores 0.666 and the pair gives −0.081. The dense output. It follows the scan at about 3-voxel detail. As run, it lost about 0.2 AUC on two of the five pairs, and 0.16 on a third, where the interval just includes 0. Part of that was a bug: the depth transfer dropped 19.5% of the dense output's hits and 11.5% of the drop-in output's, and the model's map changes around the holes. The bug accounts for more of the gap to the drop-in output than of the loss against the winding as received. Whether the detail itself costs anything isn't settled. With the transfer fixed, dense minus drop-in is −0.029 and +0.026 at seeds 42 and 43, both including 0. That result depends on the fix: −0.051 without its smoothing and −0.040 with an exact intersection, both excluding 0 (see "Later check" below). On the traced segments, the dense output showed no detectable loss (part A).

Not the same measure as the w052 review. This test measures agreement with ink labels, on a scroll the model hasn't seen. The w052 test measured legibility by eye, with the drop-in output.

Later check: a bug in the depth transfer (post hoc, exploratory)

This was added after everything above. It is exploratory and changes no pre-registered outcome: the tables above remain the plan's outcome. KLAVIS suggested the test and supplied the windings and the first numbers. KLAVIS's own scoring doesn't use this tool, so those first numbers aren't affected. The rerun, its rule and its readings came from an automated review (review_2026_11.md), and no person has reviewed the new maps.

The bug. The plan asks for a hit within 2 voxels of a surface sample. tools/depth_transfer.py at 627d058 measured that to the sample nearest the target's pixel, not the sample nearest the hit. So correct hits failed, more often the deeper the surface lay. Those pixels stayed empty and rendered as zeros through all 21 layers.

An exact ray-mesh intersection, written separately, shows how many hits were dropped:

Surface Hits dropped

Traced targets

Snapped targets 0.5%

Windings as received 8.9%

Drop-in output 11.5%

Dense output 19.5%

Second try 21.1%

So it isn't specific to 3-voxel surfaces, though they lost about twice as much. On the dense output, the share rises from 1.9% under 1 voxel of depth to 57% at 8–10 voxels.

The rerun. 98542c1 adds --refine and --normal-sigma, off by default. With them off, all 26 depth files reproduce bit for bit. Everything was redone with --refine 3 --normal-sigma 10 at seeds 42 and 43, with the plan's model, settings and scoring. The smoothing and its scale were chosen after the plan. Two checks ran at seed 42 only: refinement without the smoothing, and the exact intersection. The readings were fixed in ink_test_0841_rerun/rule.md before these maps existed, but after one pair had been scored, so they aren't blind. The rule wasn't pushed then, so only local file times show the order. The tables are in ink_test_0841_rerun/.

Pooled over the five pairs. Each version is scored by the plan's pixel rule, so the fixed rows score about a third more pixels (2,237,195 against 1,690,104), mostly deeper ones. Bold marks an interval that excludes 0. The plan reported pooled means only; these intervals come from the rerun's rule.

Contrast As run, seed 42 (the

plan's outcome)

Same transfer, seed

43 (post hoc) Fixed, seed 42 Fixed, seed 43

Drop-in − as received

+0.019 (−0.024 to +0.061)

−0.047 (−0.089 to −0.002)

−0.022 (−0.052 to +0.011)

−0.027 (−0.063 to +0.008)

Dense − as received

−0.078 (−0.129 to −0.028)

−0.098 (−0.139 to −0.059)

−0.051 (−0.093 to −0.004)

−0.002 (−0.037 to +0.041)

Second try − as received

−0.070 (−0.121 to −0.020)

−0.063 (−0.105 to −0.024)

−0.050 (−0.093 to −0.003)

+0.002 (−0.032 to +0.038)

Dense − drop-in −0.097 (−0.142 to −0.054)

−0.051 (−0.090 to −0.011)

−0.029 (−0.061 to +0.004)

+0.026 (−0.006 to +0.059)

Snapped − traced (part A)

+0.011 (−0.017 to +0.037)

−0.007 (−0.034 to +0.022)

+0.010 (−0.018 to +0.038)

+0.016 (−0.009 to +0.042)

The readings fixed in advance.

Is the dense output's gap to the drop-in output an artefact? Supported at both seeds. With the fix, both pooled intervals include 0, no pair's interval is below 0, and the gap narrows by 0.068 and 0.077. That depends on the post-hoc smoothing. At seed 42, refinement without smoothing gives −0.051 (−0.086 to −0.016): not supported. It depends on the transfer method. At seed 42, the exact intersection gives −0.040 (−0.073 to −0.004): partly. No pair moves more than 0.05 between it and the fix (largest 0.025). The holes as the mechanism, per pair. Among pairs with a dense-minus-drop-in loss as run, two things were tested: giving the drop-in output the dense output's holes, and filling the dense output's holes. Both did what the mechanism predicts on 1 of 4 pairs at seed 42, and 1 of 3 at seed 43. Against the winding as received, with the fix. Drop-in: no detectable pooled difference at both seeds. Dense and second try: seeds disagree (the interval excludes 0 at seed 42 and includes it at seed 43). No pooled or per-pair row repeats at both seeds, in either direction. Part A. Pooled, the fix moves snapped − traced by 0.000 at seed 42, and by +0.022 at seed 43 (+0.025, +0.021 and +0.0205 per target). The rule flags moves over 0.02: all four are flagged at seed 43, none at seed 42. Per target at seed 43, same transfer: +0.020, −0.056 (−0.111 to −0.003) and −0.002. Fixed: +0.044 (+0.007 to +0.079), −0.035 and +0.019. Neither that loss nor that gain repeats at seed 42. Noise. Pooled differences between the two seeds run up to 0.066. These are smaller than their own seed difference, so they aren't reported as effects: as run: the drop-in output (+0.019, −0.047); fixed: dense − drop-in (−0.029, +0.026), the second try (−0.050, +0.002), and the dense output at seed 43 (−0.002); per pair: the as-run gain on w056 on w00, whose seed difference is 0.185.

The fixed dense output at seed 42 (−0.051) clears its seed difference (0.049) by 0.002. No random-move control was run on windings. On the traced targets, small moves change the pooled AUC by at most 0.021, and random moves with the same spectrum by −0.08 to −0.11.

Added afterwards (not in the fixed readings).

Which pixels decide. The rule defines two pixel sets and doesn't say which decides. The readings above use primary, a choice made after the results were read. On secondary pixels (the as-run pixels), the artefact reading is the same and the smoothing still changes its category (partly, −0.040). The exact intersection reads supported (−0.035, −0.073 to +0.000), though that depends on the bootstrap draw, and the second try reads no detectable pooled difference at both seeds (−0.043, +0.001). On identical pixels, the gap narrows by +0.074 (+0.028 to +0.119) and +0.081 (+0.038 to +0.122). Mostly this is the holes, not the depth change: filling only the holes gains +0.074 and +0.071 on the pixels the plan's rule scores. It holds when pooled, not pair by pair. Only w056 on …144552896, the pair that prompted this check, passes alone at both seeds. Without it, the gap narrows by +0.059 and +0.069 on identical pixels, and by +0.048 and +0.065 on each version's own primary pixels, where +0.048 misses the rule's 0.05. Averaged per target, the intervals are −0.034 to +0.200 and +0.002 to +0.171. The zeros don't act through the normaliser. In a 2 × 2 test of holes in the input against holes in the normaliser's statistics, the input carries the effect (+0.075, +0.068 on the dense output) and the statistics almost none (+0.004, +0.005). The map's level on non-ink pixels is raised out to about 32 pixels from a hole. So the plan's rule removes hole pixels but not the pixels they affect. The fix adds a different population. 22–31% of the pixels each pair scores with the fix are new. They sit deeper (median 6.2–7.2 voxels, against 2.4–3.5), and sheet spacing here is 9–14 voxels, close to the plan's 10-voxel limit.

What this changes (also added afterwards).

Dense against drop-in. Pooled, most of that gap came from this bug. The first version of this page (e093829) gave the 3-voxel detail as the cause. As a full explanation, that doesn't stand. Dense against as received. The fix removes 35% of the pooled loss at seed 42 and 98% at seed 43 (36% and 92% on identical pixels). The two pairs flagged above stay negative: w055 −0.115 and −0.054, w056 on …144552896 −0.074 and −0.020. Not shown: that snapping is harmless on windings. No loss repeats, but no gain does either, and the intervals still allow a pooled loss of up to about 0.09. This is 5 pairs on 3 targets, and the two seeds are two checkpoints reading the same renders. The w052 test isn't touched. Its renders don't go through this tool, and they have almost no small holes (0.32 and 0.47 per megapixel, original and snapped).
