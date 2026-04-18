# UKG 140 OG Bounce Driver: Tutorial Part 9 — Master

## Purpose
Teach the learner how to take the finished premaster of `ukg-140-og-bounce-driver` to a controlled, club-ready final master without destroying:
- punch
- low-end clarity
- groove
- translation

This part should keep the master stage small and disciplined:
- trim
- gentle glue if needed
- subtle saturation / soft clip
- limiter
- translation and export checks

It should not try to repair a broken premaster. If the limiter is removing punch or blurring the kick/bass relationship, the learner should go back to `Part 8`.

Related documents:
- [2026-04-17-ukg-140-og-bounce-driver-production-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-production-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-plan.md)
- [2026-04-17-ukg-140-og-bounce-driver-tutorial-part-08-mix.md](/Users/patrickalfante/music-theory-learner/docs/plans/2026-04-17-ukg-140-og-bounce-driver-tutorial-part-08-mix.md)

## Outcome
By the end of this part, the learner should have:
- one restrained master chain
- one working final limiter stage
- one final export
- one premaster vs master comparison
- one final loudness-matched A/B against the references

## Time Estimate
- `20–30 minutes`

## Prerequisites
- the premaster is translating well and still has healthy headroom
- the learner has completed `Part 8`
- the learner can use:
  - `Utility`
  - `Glue Compressor`
  - saturator / soft clip stage
  - limiter

## What The Learner Should Understand Before Starting
Mastering here is not:
- fixing a muddy low-mid
- rebalancing the groove
- making a weak mix exciting through loudness

Mastering here is:
- finishing
- protecting
- translating

If the mix only works after aggressive limiting, the real problem is still upstream.

## Reference Axis
Use the same reference set as the mix chapter, but judge different things:

- `KETTAMA - It Gets Better`
  - final pressure without harshness
- `Interplanetary Criminal - Slow Burner`
  - whether loudness still preserves pocket
- `Y U QT - U Belong 2 Me (4x4 Mix)`
  - whether the low end stays stable under level
- `Sammy Virji - I Guess We're Not the Same`
  - whether hook and harmony remain readable after limiting

## Files / Assets Needed
- final premaster
- master chain on the `Premaster` or final output lane
- loudness-matched references
- export folder ready inside `Exports / Checkpoints`

## Master Targets
- keep the ceiling around `-1 dBTP`
- use only small glue compression if needed
- keep punch and low-end relationship intact
- do not force loudness until the premaster survives:
  - mono
  - small speaker
  - reference comparison

## Step 1: Check The Premaster Before Mastering
### Action
Play the premaster with the master chain bypassed.

Confirm:
- the kick still lands cleanly
- the bass still breathes with it
- the hook still reads
- the low-mid is not collapsing
- the premaster still has usable headroom

### Why
If the premaster is already unstable, the master stage only makes the problem louder.

### Rule
- do not start limiting until the premaster already sounds like a record

### Screenshot
- `master-01-premaster-check`

## Step 2: Build The Master Chain
### Action
Build the chain in this order:
1. `Utility`
2. `Glue Compressor`
3. soft saturation / soft clip
4. `Limiter`

Starting direction:
- `Glue Compressor`
  - ratio `2:1`
  - gentle threshold
  - aim for small gain reduction only
- limiter ceiling:
  - around `-1 dBTP`

Ableton action order:
1. On the `Premaster` lane, place the devices in that exact order.
2. Rename any plugin or rack labels if needed so the chain reads clearly from left to right.
3. Keep every device bypassed at first.
4. Turn them on one by one from left to right after the whole chain is in place.

### Why
The chain should help the record finish, not change its identity.

### Screenshot Set
- `master-02a-master-chain-overview`
- `master-02b-master-devices`

## Step 3: Apply Only Gentle Glue Compression
### Action
Engage the glue compressor only enough to make the track feel slightly more finished.

Target:
- small gain reduction only
- no obvious pumping
- no flattening of the groove

### Why
The drum pocket and hook punctuation are easy to damage here.

### Rule
- if the groove gets smaller, back off immediately

### Screenshot
- `master-03-glue-compression`

## Step 4: Add Soft Saturation / Clip Carefully
### Action
Use subtle saturation or soft clipping only to add a little density before the limiter.

Target:
- slightly firmer body
- no brittle top-end
- no blurry kick/bass relationship

### Why
This stage should reduce limiter strain, not become a tone-design experiment.

### Screenshot
- `master-04-soft-clip-stage`

## Step 5: Set The Limiter
### Action
Raise the limiter until the track reaches controlled club strength without losing:
- punch
- groove
- hook readability

Keep the ceiling around `-1 dBTP`.

Exact first-pass action:
1. Start playback from the loudest section of the song:
   - usually around `97.1.1` to `113.1.1`
2. Set the limiter output ceiling to around `-1 dBTP`.
3. Raise the limiter input / gain slowly while listening, not in one big jump.
4. Stop the moment the kick starts sounding flatter or the bass loses movement.
5. If you cannot get enough level without damage, go back to `Part 8` instead of forcing the limiter harder.

### Why
Loudness is the last move, not the first.

### Rule
- if loudness removes punch, stop and go back to the premaster

### Screenshot
- `master-05-limiter-settings`

## Step 6: Compare Premaster vs Master
### Action
Level-match the premaster and final master as closely as possible for comparison.

What to listen for:
- did the kick get blurrier?
- did the sub get smaller or less stable?
- did the hook get less readable?
- did the groove get flatter?

### Why
The mastered file should feel more complete, not like a more damaged version of the premaster.

### Expected Answer
- the master should feel denser and more finished
- it should not feel meaningfully flatter than the premaster

### Screenshot
- `master-06-premaster-vs-master`

## Step 7: Run Translation Checks One Last Time
### Action
Check the final master in:
- mono
- small speaker / phone
- everyday playback if possible

Then compare against loudness-matched references again.

### Why
The limiter can expose problems that were hidden in the premaster.

### Screenshot Set
- `master-07a-final-mono-check`
- `master-07b-final-reference-ab`

## Step 8: Export The Final Files
### Action
Export:
- final master
- premaster

Keep both in the project export folder so the learner can revisit them later.

Recommended organization:
- `Exports / Checkpoints / premaster`
- `Exports / Final / master`

Exact first-pass export workflow:
1. Set the Arrangement loop braces or export range so they cover the full song:
   - start `1.1.1`
   - end `145.1.1`
2. Export the premaster first with the master chain bypassed.
3. Name it clearly, for example:
   - `ukg-140-og-bounce-driver-premaster.wav`
4. Then export the mastered version with the chain active.
5. Name it clearly, for example:
   - `ukg-140-og-bounce-driver-master.wav`
6. Put each file in the correct folder immediately instead of leaving exports on the desktop or downloads folder.

### Why
Keeping the premaster and final master side by side is useful for:
- learning
- revision
- future tutorial packaging

## Troubleshooting
### Problem: “The limiter removed punch.”
Fix order:
1. lower the limiter drive
2. reduce the soft clip stage
3. go back to the premaster and fix the kick/bass balance there

### Problem: “The master is louder but smaller.”
Fix order:
1. back off master compression
2. reduce clipping
3. re-check low-mid crowding in the premaster

### Problem: “The track folds in mono after mastering.”
Fix order:
1. re-check the stereo map from `Part 8`
2. narrow the wrong lanes
3. confirm the important identity still exists in the center

### Problem: “The references still sound much louder.”
Fix order:
1. confirm the A/B is loudness-matched
2. judge tone and punch first, not raw volume
3. accept that forcing more loudness may cost more than it gives

## What Must Be Captured For Later Lesson Conversion
- master chain screenshot
- limiter settings screenshot
- premaster vs master comparison notes
- final export paths
- final master bounce
