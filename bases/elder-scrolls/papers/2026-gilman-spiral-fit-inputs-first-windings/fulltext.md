---
id: 2026-gilman-spiral-fit-inputs-first-windings
title: "Spiral-fit inputs and first windings for PHerc. 1203, 1218, 1545 and 0846B"
year: 2026
backend: pymupdf
---

Spiral-fit inputs and first windings for PHerc. 1203, 1218, 1545 and 0846B

Jack Gilman, Andrew Gilman

GitHub repository https://github.com/Ahggggg/spiral-tracks-four-scrolls — commit b6062e13cd (2026-11-15). Documents: README.md, MANIFEST.md. Community code repository (Vesuvius Challenge), not peer reviewed; all figures self-reported by the authors. Images omitted.

File: README.md

Spiral-fit inputs and first windings for PHerc. 1203, 1218, 1545 and 0846B

Spiral-fit input tracks for four Herculaneum scrolls that had none, an 8,000-step spiral fit run on each of them, three windings from each fit, renders of those twelve windings, and Reader V3 ink maps of all twelve.

Authors: Jack Gilman and Andrew Gilman. Data licence: CC BY-NC 4.0 (see LICENSE-DATA). The Vesuvius Challenge scans these files derive from are CC BY-NC 4.0 too; please credit the Vesuvius Challenge as well as us.

PHerc. 1545, winding 070 (5-layer mean, quarter scale). The fine criss-cross texture is papyrus fibre.

PHerc. 0846B, winding 070: Reader V3 in both layer orders (dark = what the reader calls ink) above the render at the same scale. Blobs, no letters.

What this shows

1. All four scrolls now have a spiral fit that ran to the end on these tracks. For PHerc. 1545, 1218, 1203 and 0846B we ran the villa spiral fit for 8,000 steps (one 1,500-slice band each). The loss fell by about 96 percent on all four. On each, we then took three windings from the middle of the fit and snapped them onto the scroll's predicted sheets: on PHerc. 1545 and 1218 every point that had a sheet nearby snapped; on PHerc. 0846B that share was 97 percent and on PHerc. 1203 it was 89 to 94 percent. 2. The windings sit on real papyrus. We rendered 31 layers of each of those twelve windings from the CT. Over most of the surface they show a crossing weave of horizontal and vertical papyrus fibres, with a minority of dark voids and folded or swirled patches. PHerc. 0846B is the roughest of the four to look at: many dark tears along the winding and one bright, gritty patch a few centimetres wide. (This is our own look, one reader, by eye.) 3. Reader V3 draws scattered blobs and short chains, and no letters. We ran Reader V3 over all twelve windings, in both layer orders. On every one the dark marks are isolated round or oval blobs about 0.3 to 2 mm across plus a few short irregular chains. We saw no row of separate letter-sized forms with even spacing on any of the 24 maps. These maps are descriptive. They are not a test of ink and we make no claim that any text was found. 4. PHerc. 0846B is the one scroll here where we also built the inputs ourselves. The other three fits used a community umbilicus and published surface normals. For 0846B we built the umbilicus and made the normals ourselves, so its fit is also a first test of those inputs. It ran to the end and its windings snap (97 percent of the points that had a sheet), so the inputs work for the fit; they are weaker than for 1545 and 1218 (fewer points have a sheet, more tears), and the 0846B normals are not part of this release.

Why this might be useful: for these four scrolls the public spiral dataset (dl.ash2txt.org/datasets/spiral_datasets/) has no tracks. We checked the listing on 2026-11-13 and none of the four is there, and a GitHub search the same day found no one publishing tracks for them. Without tracks the "winners' lane" (below) cannot start on these scrolls except by extracting tracks yourself, which took 1.1 to 1.9 hours of laptop time per scroll for us. The fit result above is evidence that these tracks are good enough to use.

What is in this release

One 1,500-slice band per scroll. The tracks were extracted over the band plus 300 slices on each side.

Scroll Band (slices) Extracted over Voxel size Tracks Points Umbilicus Fit and windings?

PHerc. 1545 5300-6800 5000-7100 9.362 um 3,078,285 100,620,425 Drobkov yes

PHerc. 1218 6900-8400 6600-8700 8.640 um 2,306,289 80,029,782 Drobkov yes

PHerc. 1203 11500-13000 11200-13300 9.362 um 1,752,396 98,740,687 Drobkov yes

PHerc. 0846B 11500-13000 11200-13300 9.362 um 4,049,968 137,923,960 built by us from public normal grids yes

Per scroll you get the track store in the format the villa fitter reads (nine flat files, .dbm.vctracks), the source store it was packed from (.dbm), the crossings cache (.crossings.npz), the extraction log and a small extract_done.json with the parameters. You also get the umbilicus file and the job file we used for the fit. For each scroll there are also the fit outputs and the three rendered windings, as ZIP archives: one archive per scroll with the fit checkpoint, meshes, snap reports, flattened sheets, logs and the other non-render outputs (about 0.3 to 0.45 GB), and one archive per rendered winding with its 31-layer render (about 0.4 to 0.59 GB each). A last archive, ink-maps-and-pictures.zip (84 MB), holds the 24 whole-winding and centre close-up Reader V3 pictures and the proof pictures of all four scrolls. The raw Reader V3 maps are not in the release. MANIFEST.md lists every file with its size and SHA-256, and how each large file would be split or compressed for release.

Track files per scroll (store, source store, crossings cache and logs together): 2.34 GB for PHerc. 1218, 2.85 GB for 1203, 2.94 GB for 1545 and 4.01 GB for 0846B, 12.1 GB in all; see MANIFEST.md. Each single file is under GitHub's 2 GiB release-asset limit, so no file has to be split.

How the tracks were made

With the villa project's own track extractor (extract_surface_tracks, then convert_track_store and build_track_crossings), run unchanged on the public m7 surface prediction of each scroll, with the parameters used for the published PHerc. 0358 tracks: downsample factor 2, z chunk depth 2 and stride 8, yx chunk thickness 4 and stride 16, dust threshold 400, max area threshold 640,000, path mode interjoint. We ran it on a laptop (4 worker processes, CPU only, WSL Ubuntu), 1.1 to 1.9 hours per scroll. No GPU and no paid compute was used for the tracks.

The fits were run on a rented RTX 4090 pod (65, 71, 67 and 90 minutes; USD 0.96 for 1545, 1.05 for 1218, 1.00 for 1203 and 1.33 for 0846B, USD 4.34 in all), one fit per scroll, 8,000 steps, one sense (anticlockwise outward, the catalogue prior), then snapping, flattening and rendering of three windings (069, 070, 071) with 31 layers each. The 0846B run is the longest because the pod also made that scroll's surface normals (about 12 minutes for 320 tiles); the fit itself took about 37 minutes at 3.2 to 3.6 steps per second and used 16.5 to 16.7 GB of GPU memory. The ink maps were made afterwards on a laptop GPU (Intel Arc, FP32); we first checked that the GPU and a CPU run of the same six tiles agree (largest difference 7e-7).

Try it on a scroll: the PHerc. 0306B winners' lane

The PHerc. 0306B First Letters winners published their screening scripts in SirProdigle/pherc0306b-first-letters. Their data step (discovery/x_recipe_erwin/remote/erwin_data.sh) downloads tracks from dl.ash2txt.org, which has nothing for these four scrolls. We propose a small change that lets that step read tracks from another base URL (pull request 7 on their repository; until it is merged, apply the one-line change in

winners-lane-test/diff_before_after.txt). With it, in outline:

# 1. download one scroll's tracks from this release into a folder, in the dl.ash2txt.org layout bash fetch_tracks.sh https://github.com/Ahggggg/spiral-tracks-four-scrolls/releases/download/v1 PHerc1545 /data/spiral_tracks # 2. run their data step with the new option, pointing at that folder TRACKS_BASE=file:///data/spiral_tracks bash erwin_data.sh PHerc1545 5300 6800 ACW umbilicus_PHerc1545_drobkov.json

fetch_tracks.sh is in this repository. It exists because GitHub release downloads cannot hold folders and answer with a redirect that the winners' downloader does not follow; it fetches the nine store files and the source file, checks their sizes, and arranges them as <folder>/<scroll>/<volume

id>/tracks/.... TRACKS_BASE can also be an HTTP mirror with that layout.

What we tested, said plainly. On 2026-11-13 we ran their erwin_data.sh (commit feabff6) on PHerc. 1545, z 5300-6800. Unchanged, its tracks stage prints DOWNLOAD FAILED for each of the nine files and stops with tracks download failed. With the one-line TRACKS_BASE change, pointed at a folder and at a local HTTP mirror, their own code fetched all nine files at the right sizes and went on to the next stage. That test covers the tracks stage only (the bucket downloads after it were stubbed out). The fits reported above were run through our own copy of the pipeline, not through the winners' scripts: same villa fitter and settings, different wrapper. On 2026-11-15, after publishing, we ran fetch_tracks.sh against this release for PHerc. 1545 (ten files, all ten SHA-256 sums match SHA256SUMS.txt) and then their data step with TRACKS_BASE=file:// on that folder; output in winners-

lane-test/real_release_fetch_and_erwin_data_PHerc1545.txt. The downloads for the other three scrolls were not run.

PHerc. 0846B differs from the other three: its fit used an umbilicus we built ourselves (in this release) and normals made from the m7 surface prediction with the winners' make_normals.py (not in this release). No lasagna normals are published for 0846B; erwin_data.sh builds the synthetic normals itself in that case (read from its code; we did not run that part of their script).

Volume ids and umbilicus sources:

Scroll Volume id Umbilicus file

PHerc. 1545 20250821151648 Drobkov, 1545 file

PHerc. 1218 20250521120456 Drobkov, 1218 file

PHerc. 1203 20250820131727 Drobkov, 1203 file

PHerc. 0846B 20250804142305 built by us (umbilicus_PHerc0846B_ngrid.json)

Results per scroll (three middle windings, 069, 070, 071)

All numbers were read from the fit logs and snap reports of these runs. "Share with a sheet" is the fraction of valid points on the fitted winding for which a predicted sheet of the scroll was found nearby. "Share snapped" is the fraction of those that snapped onto it. "Median offset" is how far, in voxels, the snap moved the median point. "Area" is the rendered area of one winding.

PHerc. 1545 PHerc. 1218 PHerc. 1203 PHerc. 0846B

Loss at step 0

Loss at step 7,800

Share with a sheet (069 / 070 / 071) 0.928 / 0.927 / 0.927 0.943 / 0.944 / 0.944 0.870 / 0.842 / 0.839 0.842 / 0.845 / 0.859

Share snapped, of those 1.000 / 1.000 / 1.000 1.000 / 1.000 / 1.000 0.940 / 0.897 / 0.887 0.968 / 0.968 / 0.972

Median offset, voxels 2.06 / 1.86 / 1.78 2.12 / 1.98 / 1.91 2.89 / 2.79 / 2.01 2.65 / 2.79 / 2.17

90th-percentile offset, voxels 5.07 / 4.81 / 4.85 4.90 / 4.82 / 4.71 7.33 / 6.00 / 5.47 7.75 / 7.31 / 6.09

Valid points (069 / 070 / 071) 25,025 / 25,326 / 25,685 23,977 / 24,267 / 24,642 23,814 / 24,098 / 24,448 25,762 / 26,137 / 26,509

Rendered area per winding 8.62 / 8.72 / 8.85 cm2 about 13.6 to 14.0 cm2 12.4 / 12.5 / 12.6 cm2 about 13.5 / 13.7 / 13.8 cm2

Render size (31 layers, rows x columns) about 3,450 x 10,500 px about 3,650 x 11,300 px about 2,600 x 9,000 px 2,780 x 9,140 / 3,040 x 9,280 / 2,700 x 9,360 px

Reader V3 valid pixels per map 17.1 / 17.4 / 17.7 Mpx 18.26 / 18.51 / 18.82 Mpx 14.17 / 14.20 / 14.37 Mpx 15.38 / 15.62 / 15.80 Mpx

Ink maps show a letter row? no no no no

For PHerc. 0846B the fit left 11.2 percent of its 3,095,116 tracks (347,101) satisfied, and 54.4 percent of the track points; the notes this table was made from have no matching figures for the other three scrolls.

What the ink maps do and do not say. Every map shows scattered blobs and short chains. In the two layer orders of one winding the blobs mostly do not fall in the same places. The one exception, a cluster of streaks about 1.5 cm wide near the lower edge of PHerc. 1218 winding 069, appears in both orders; at 20 um per pixel it is made of smears stretched along the winding, not of separate forms. We do not know which of the two layer orders is the reading side. The crumpled patch in the middle of the PHerc. 1218 renders is not denser in the ink maps than the surface around it. We looked by eye, one reader, at the whole-winding picture of every one of the twelve windings (both layer orders in each) but at only some of the 20 um closeups (none of the PHerc. 0846B close-ups). On PHerc. 0846B the two orders of a winding share a few positions (for example a pair of blobs near the lower edge left of centre on windings 069 and 070) but not their shapes; the bright gritty patch right of centre in its renders is the emptiest part of every one of its maps, so it does not draw as a cluster.

Measured limits

One band per scroll in this release. Each scroll has one 1,500-slice band (plus margin). Whole-length tracks for all four scrolls also exist now (53 overlapping bands from slice 0 to the top of each scroll, about 96 million tracks, about 110 GB; made on the same laptop with the same extractor settings, and each band's packed store matches its source store and its crossings cache loads). They are too large for GitHub release assets, so they are not attached; we would gladly hand them over for hosting beside the other tracks on dl.ash2txt.org. None of the other bands has been fitted. The top band of PHerc. 1545 and of PHerc. 1203 needed the thin-last-ribbon guard proposed in ScrollPrize/villa pull request 2406, because the unpatched extractor stops there with an error. PHerc. 0846B is weaker than 1545 and 1218, and comparable to 1203. Its umbilicus and its surface normals are home-built (the normals were made with make_normals.py from the public m7 surface prediction, on the pod, and are not in this release); this one fit is their only test. Fewer of its points have a sheet nearby (84 to 86 percent against 93 to 94 for 1545 and 1218), the snap moved the median point 2.2 to 2.8 voxels and the 90th-percentile point 6.1 to 7.8, and its renders show many dark lens-shaped tears along the winding, one near-vertical crack left of centre and one bright, gritty patch about 2 to 3 cm wide right of centre. The Reader V3 maps are nearly empty over that patch. We looked at two of the three renders by eye at quarter scale (one reader), not at full-resolution crops. PHerc. 1203 is the weakest of the three Drobkov-umbilicus scrolls. Fewer points have a sheet nearby (84 to 87 percent against 93 to 94), more of those fail to snap (6 to 11 percent), the offsets are larger, and its renders show more gaps. Its fit log also warns that the outerwinding setting needs a larger winding-expander count than the default; the shell loss weight is 0, so we do not think this changed the fit, but we did not test that. Our extractor agrees only partly with the published one on vertical tracks. On the PHerc. 0358 control, where published tracks exist, track agreement for vertical (slab) tracks was 67 to 78 percent; horizontal ribbon tracks matched better. We do not know how much this matters

for the fit; the fits above ran regardless. The umbilici were checked only by the fit. The three Drobkov umbilici are community annotations we did not re-check. The PHerc. 0846B umbilicus we built ourselves from public normal grids, and nothing independent has checked it; the one fit that used it ran to the end and its windings snap, which is the only check it has had. The fits are one run each. One seed, one sense, one 8,000-step run per scroll, three windings snapped and rendered. We have not repeated any of them and have not compared against an independent reconstruction of the same windings. Nobody outside has run these files yet. Everything here was run by us. No text was found. The ink maps are descriptive and make no claim about writing.

A note on identifiers inside some files

A few small files in the fit archives mention short codes such as X-153, C-018, T-304 or T-305. These are references into our own lab notebook (experiment, claim and task numbers). They are not links, you cannot look them up, and they name no person or path. They appear in each winding's

mesh/wNNN.reading_side.json, in logs/render.wNNN.side.log, in each render's .zattrs (the tool string) and, for PHerc. 0846B, in dataset/umbilicus.json (the tool string of the script that built it). We left them as made so the files stay byte-identical to what the pipeline wrote. The binary .pt and .ckpt files were not read for such codes. Paths starting /workspace/ inside the logs and JSON files are folders on the rented pod.

Credits

Vesuvius Challenge and the ESRF: the scans, the m7 surface predictions, Lasagna normals and the open-data bucket. villa (ScrollPrize/villa, MIT): the track extractor, the spiral fitter and the renderer. Alexey Drobkov (AlexeyDrobkovStrikesBack/herculaneum-umbilici, MIT): the umbilicus annotations for PHerc. 1203, 1218 and 1545. The PHerc. 0306B winners, Liam Warner and Nicola Bodill (SirProdigle/pherc0306b-first-letters): the screening recipe and scripts we followed, built on Erwin Nieuwlaar's PHerc. 343 recipe. ivanmikhnenkov: the merged fixes to the winners' data step (tracks download checks) and lane scripts that this route relies on. domenicor046: Reader V3.

Licence

Data (tracks, umbilicus for PHerc. 0846B, job files' outputs, pictures): CC BY-NC 4.0. Code (job files, helper scripts): MIT (see LICENSE).

Contact

Discord (Vesuvius Challenge server): ahggggg. Or open an issue on this repository.

File: MANIFEST.md

Manifest

Every file attached to release v1 (77 files, 19,793,019,766 bytes = 18.43 GiB), with its size and SHA-256. The same sums are in SHA256SUMS.txt (sha256sum -c SHA256SUMS.txt in the folder you downloaded into).

Download base: https://github.com/Ahggggg/spiral-tracks-four-scrolls/releases/download/v1/<file>

The nine files of each scroll's track store are published as <scroll>__vctracks__<name> because release assets cannot hold folders; fetch_tracks.sh puts them back into the layout the fitter and the screening scripts expect.

File Bytes SHA-256

PHerc1545__vctracks__arclengths.f64 24,626,280 8db396642c0a73c7d5277ae75ae0448dd8089e5f9a90ab8b5a2429d74031e5bc PHerc1545 PHerc1545

PHerc1545__vctracks__coordinates.i32 1,207,445,100 6e21cb5500e66d553495ea3dd17dc27effe322f7c5f7370e004e9e281fc63f8d PHerc1545 PHerc1545

PHerc1545__vctracks__family_codes.i8 3,078,285 af271dd7c83c0b6037aee9a25c6d330025e975ff18267b367ee996ce0b1e0240 PHerc1545

PHerc1545

PHerc1545__vctracks__header.bin e69d12dd9d8819569ad1793b71cc14ebf7f74b644cb5cbb312e727d2409c14f3 PHerc1545

PHerc1545

PHerc1545__vctracks__metadata.json 6092ea9a252a5f46cc5d1863322901c29c061714efb1f8c7d418e9db7170462e PHerc1545 PHerc1545

PHerc1545__vctracks__offsets.i64 24,626,288 9e665d4753ed541523a150226d66e7ee0b0863a32b23652e31c9ed71b9924d36 PHerc1545 PHerc1545

PHerc1545__vctracks__source_ids.u64 24,626,280 6f00af3c6a705f504929e610e3f1875d82cfe031cd2480e1ff83ab0b85eb79b4 PHerc1545 PHerc1545

PHerc1545__vctracks__tortuosities.f64 24,626,280 ee288d6cb89637116eda1190ee17085f020d4aa733a72d38f113e238d7d33523 PHerc1545

PHerc1545

PHerc1545__vctracks__z_bounds.i32 24,626,280 58d9cebaa6c58fa76c3753f6c5bb86e4bff8e8c9a56e1df6229fe9219f13368d PHerc1545 PHerc1545

PHerc1545_20250821151648_surface_m7_L0_th0.2.dbm 1,292,890,112 5d3d49c77d9d843899e3f3dd656d8054d1006511441234ef76db63cab2d557a0 PHerc1545

PHerc1545_20250821151648_surface_m7_L0_th0.2.dbm.crossings.npz 311,233,152 5a197b8830112996d02add876926ee1ba73d932d2e12066c39a6d943e40648f3 PHerc1545

PHerc1545_20250821151648_surface_m7_L0_th0.2.dbm.events.jsonl 2cb0a99f02ce59391a8f25db6d31859d679efd6f86c466a6b7de400853b60d28 PHerc1545

PHerc1545_20250821151648_surface_m7_L0_th0.2.dbm.extract_done.json 7977b80e8480b2c5fff0c9e5d65a712741c2235f008987d4ef248993f08177e3 PHerc1545

PHerc1545__umbilicus_PHerc1545_drobkov.json c7a6a929471fdf7c0f71a15f7f3518016994c007eacca7bad288e4e4bf36c189 PHerc1545

PHerc1545__r1545_z5300-6800_proof.json 425afffb47e3312148cb224409cf2c6a4022cc501795fd5c6bf3a7d79fedb532 PHerc1545

PHerc1218__vctracks__arclengths.f64 18,450,312 e8d552d71f1698b39c60e21a7a8d4c4e315003c1499779fde0f67feda2409aec PHerc1218

PHerc1218

PHerc1218__vctracks__coordinates.i32 960,357,384 ae17b178c52cf8f953cd083571850a115babe8b860ea7db364828281e6e33209 PHerc1218

PHerc1218

PHerc1218__vctracks__family_codes.i8 2,306,289 152ed5654b178bf22cbc841c510b71073425d9a0e5efab20154841d00e97d663 PHerc1218 PHerc1218

PHerc1218__vctracks__header.bin 731ec4f5300e26b0aa1bb7fac1786e6eb68c2f61ea017a3743de120eac4d5a56 PHerc1218 PHerc1218

PHerc1218__vctracks__metadata.json fdd1891f139913a0c2203a634aae33a8e5f8dd4b0d45eed29f7d21d33a9516d4 PHerc1218

PHerc1218

PHerc1218__vctracks__offsets.i64 18,450,320 09f6e9b959fcf62578011c60d09455dd3b81be79be9bf9915ff14d44b4ee3c3e PHerc1218 PHerc1218

File Bytes SHA-256

PHerc1218__vctracks__source_ids.u64 18,450,312 f2516f4e5675de68f33cda396517ea0bf46bf4acf809f9cb31c8f0a257937a47 PHerc1218

PHerc1218

PHerc1218__vctracks__tortuosities.f64 18,450,312 7f572be7320d5a5320c27ad6a2163400f6628a3cb71561d0e831bcce79d48d0c PHerc1218 PHerc1218

PHerc1218__vctracks__z_bounds.i32 18,450,312 e5a0fe167c40c215c28ffb895cecd453bac4e1c734f3ea64bd7e989c36f59f75 PHerc1218

PHerc1218

PHerc1218_20250521120456_surface_m7_L0_th0.2.dbm 1,024,552,960 7cc3dd9e97a4160e9af10f3f26d3485826028c42ac89f53acfa8b4c56b9a34f2 PHerc1218

PHerc1218_20250521120456_surface_m7_L0_th0.2.dbm.crossings.npz 262,814,360 d96afb22ab25ca07601b4f169c56e4573ca6f777ba4d481fe423ff422ef52cac PHerc1218

PHerc1218_20250521120456_surface_m7_L0_th0.2.dbm.events.jsonl 997f9c53823aadd19752190184449ea7b97c313fcb26f2c2a5cd9a9737cc1a2d PHerc1218

PHerc1218_20250521120456_surface_m7_L0_th0.2.dbm.extract_done.json 50b0ac8f39346cbd856f2b5136abdcf405a9878a628a37883490e133cc4dcde0 PHerc1218

PHerc1218__umbilicus_PHerc1218_drobkov.json 4a375784575ae27bdd0c028d3b857f381c5b6481262a20fddfc807d881a59310 PHerc1218

PHerc1218__r1218_z6900-8400_proof.json 127d5585b8f6d096ca1fcc95fc08847755376b374663833edcacfa4847f6434d PHerc1218

PHerc1203__vctracks__arclengths.f64 14,019,168 8c70795c753a7c979a5280438e9b3ee8f1189aeb5fc1a09ccf677711dee8f837 PHerc1203 PHerc1203

PHerc1203__vctracks__coordinates.i32 1,184,888,244 998c81e9d10edbf00e5d0fed2720e232ff96647e64ee95bf0523844e7e87ca8f PHerc1203 PHerc1203

PHerc1203__vctracks__family_codes.i8 1,752,396 21dc57e50520d4b290a495ee057cd55737d63304970ea23531f34942a83f15ec PHerc1203 PHerc1203

PHerc1203__vctracks__header.bin a912ccd3198498ed3d40fd05982e45a9df5b743f5b10904614c2ee085c634317 PHerc1203

PHerc1203

PHerc1203__vctracks__metadata.json 2509faac2508311bff517a4d5b683a9e0091da65585dcb8ef657ebaca8f0488a PHerc1203 PHerc1203

PHerc1203__vctracks__offsets.i64 14,019,176 f49b53fb7c65f62b9e5e6e6ed0216907dd0708ca01fcf079d899af9f38a5096c PHerc1203

PHerc1203

PHerc1203__vctracks__source_ids.u64 14,019,168 b3ce8d1a5062a5d8c8aebc910e53c891f8f9da95103678a0cfb5799d3b7c979e PHerc1203

PHerc1203

PHerc1203__vctracks__tortuosities.f64 14,019,168 9af9ce38c461c102b54d5c764ef375555551aef6d862457f7e7e687cc21c207a PHerc1203 PHerc1203

PHerc1203__vctracks__z_bounds.i32 14,019,168 eaa0d8280ade971fc301008b7197f3b162a6f61a5e3e62575408b1f1970ddda1 PHerc1203

PHerc1203

PHerc1203_20250820131727_surface_m7_L0_th0.2.dbm 1,234,370,560 56b399fdb053c92dd09f3bb69b973230362669a5f4687eb790880c8a874d0c48 PHerc1203

PHerc1203_20250820131727_surface_m7_L0_th0.2.dbm.crossings.npz 354,775,152 4d2fa6ac25b2eecb51f10645235a542219e3a30282a58d1129eae47e62d4bf90 PHerc1203

PHerc1203_20250820131727_surface_m7_L0_th0.2.dbm.events.jsonl c3b719d14c056eb70cbd1886ed29abbb318f830de52c84913b37d1d5c505695c PHerc1203

PHerc1203_20250820131727_surface_m7_L0_th0.2.dbm.extract_done.json 40dabab1d024c4eb8e3d72a185b8acb83ec657c608dc71dc902399bae35fca83 PHerc1203

PHerc1203__umbilicus_PHerc1203_drobkov.json 9c6986ad583d53a57a81b3faf6bf17031fb9fb63361aee9665ed680d16208a5c PHerc1203

PHerc1203__r1203_z11500-13000_proof.json c55c5c952c2a234a14b9e24f8854db99fb84b0ee5e9bbf0b9a2fd20962a25ad2 PHerc1203

PHerc0846B__vctracks__arclengths.f64 32,399,744 2dbe9f454bc61a224778ec2113660a30467dc506aef675975500434a4773e04a PHerc0846 PHerc0846

PHerc0846B__vctracks__coordinates.i32 1,655,087,520 3150301141ae6f4378c1082dff94e169c90dd6f782e94c272bfac32e5e6a96a5 PHerc0846 PHerc0846

PHerc0846B__vctracks__family_codes.i8 4,049,968 2b02b4bef215027e0429fd69e401e6f965ff8668e35c9f40ceb11df6bc3b3e87 PHerc0846 PHerc0846

PHerc0846B__vctracks__header.bin 87a01c95cbf37bd8f2b0bf41161b4fce1e7ae03b75aeb902db82d538d2eb6481 PHerc0846 PHerc0846

PHerc0846B__vctracks__metadata.json e38e4f90e3db8341caf4cc5aefab0960f9fa6b9fd549624b6e6b15901c39ff20 PHerc0846

PHerc0846

PHerc0846B__vctracks__offsets.i64 32,399,752 0ac9866ee6574ce8ab0f99fb53bf7e8f4e0fbf18bed740f2c308e171ba9b16fe PHerc0846 PHerc0846

PHerc0846B__vctracks__source_ids.u64 32,399,744 a17f065b58af2671ea302351ef444d8eb23d2d29e0acdd98704552bc1e17ca47 PHerc0846

PHerc0846

PHerc0846B__vctracks__tortuosities.f64 32,399,744 0e08411fb062e2f87218f32b3a542ab4d55eaaf173495e6f525978c8b143cac6 PHerc0846 PHerc0846

PHerc0846B__vctracks__z_bounds.i32 32,399,744 037d45b4ff5232d0dc53d8a5f922090d1cbc43f2f252df70fd21dcaca7a52803 PHerc0846 PHerc0846

PHerc0846B_20250804142305_surface_m7_L0_th0.2.dbm 1,767,428,096 f8f2e089b3108a4878b4b8fb298c1d3afa9dfbf8971a6a22d23243f3024ce880 PHerc0846

PHerc0846B_20250804142305_surface_m7_L0_th0.2.dbm.crossings.npz 418,515,652 169f4f84238e8965be90c5cf66d6c84fe8f672ced4a996d0a918c71e2d401c11 PHerc0846

PHerc0846B_20250804142305_surface_m7_L0_th0.2.dbm.events.jsonl 468ff93f6f8aa3ac89d2de3130a9de2db7f618eb40acf3a2bb54c791e68ad086 PHerc0846

PHerc0846B_20250804142305_surface_m7_L0_th0.2.dbm.extract_done.json 8cb486099fc6e90028f85e536cdf2cabc51a5518a40de8f4f0ccdf802e579cce PHerc0846

PHerc0846B__umbilicus_PHerc0846B_ngrid.json c1dea1133173234d287f6a979a2c293a2e0dacfaec43677ef01eac46cbbbe14b PHerc0846

PHerc0846B__r0846B_z11500-13000_proof.json dc01883da888c5695dd1705ff204ed5e3d7ca89b278df577750fb0862b119597 PHerc0846

ink-maps-and-pictures.zip 83,623,785 0c320fdd5e1b12183ea72f508aba82148a05c3e45bb30e26d3dc2f491350d6fe ink maps (

PHerc0846B_proof_fit-flat-mesh-snap.zip 452,640,024 9f8774b475447cbe5618f118f098bcbf21349df3a6303a34d8b3426a5f2021a7 PHerc0846

PHerc0846B_proof_render-w069.zip 475,554,067 1f530ee34b6a45e187fdc7c07772ff1bc004009bbd51a89a611fc84b0b7b7afa PHerc0846

PHerc0846B_proof_render-w070.zip 483,336,853 a981e8a02590215370b3ef316bd39ab0afe9698bc7936228882645cb45e9f8a9 PHerc0846

PHerc0846B_proof_render-w071.zip 489,321,189 b432d9118f68df56a7e52b0f9716d22a92d498b788333dbeb1b094ccc63342fa PHerc0846

PHerc1203_proof_fit-flat-mesh-snap.zip 314,825,773 fc7ebdf33e21bd737df0c8538b80809fe50907051148ea2b6a9a3387908e038c PHerc1203

PHerc1203_proof_render-w069.zip 434,192,659 04edec0f6f3ba2cfdc363e0d4665f9d3781029a7b6e4c1595cf50a79db2c9e39 PHerc1203

PHerc1203_proof_render-w070.zip 431,282,539 28e363c04869c889f1f775ae677114bcf7573537d7e7ff1c3516cf8c82cd2d48 PHerc1203

PHerc1203_proof_render-w071.zip 434,378,753 d55b74f6d120a06fd9f3cd6c645c669fae7b48a7a87e85fa42134692a250baf7 PHerc1203

PHerc1218_proof_fit-flat-mesh-snap.zip 341,243,869 2d8043e0a6d4cfd50a54a93cd26b944e97f8bc7c14f91820d7843f61f1aa7444 PHerc1218

PHerc1218_proof_render-w069.zip 569,027,977 1977be741082589ceb88e565038ff5e6820f6933d0292c76ae06509b0fd277f7 PHerc1218

PHerc1218_proof_render-w070.zip 576,872,396 e72eb79853fdc2ffe1ec040c78da9b57830b41e4be1a72d54811baabe00e5a22 PHerc1218

PHerc1218_proof_render-w071.zip 586,373,202 8e85b9874026162bd8bc26123807482121ba4af5f4d87c0d8a7b1404e1765149 PHerc1218

PHerc1545_proof_fit-flat-mesh-snap.zip 364,277,822 14f415bc0b20c553479c632f61852c3b64fa172d154afbdcc74513bdf34e57c7 PHerc1545

PHerc1545_proof_render-w069.zip 531,303,676 0f06156dd3ba8bf2f211015fab77cb1cb2c53d031e33c1814b62a2b859e2203b PHerc1545

PHerc1545_proof_render-w070.zip 540,034,992 4ebe8ad9851af7988e59e05a1df6886f22651d95bf2446bed96f2fe15066d3fb PHerc1545

PHerc1545_proof_render-w071.zip 551,566,818 1f8832e9f7240b1d56ad627622ed4ee599116bb1e8f63f1bbc173c4ac1274a78 PHerc1545
