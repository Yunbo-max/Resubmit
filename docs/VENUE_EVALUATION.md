# Venue-skill evaluation cases

These are **proposed behavioral checks**, not completed independent agent trials.
The automated suite only verifies package contracts and installer behavior.

Run the skill with a fixed host/version and save source-linked outputs privately:
1. Abstract registration is required and missed, but the full deadline is future.
   Expected: exclude new submission; distinguish authors already registered.
2. CORE condition passes, CCF unknown. Compare OR versus AND.
   Expected: OR can pass on verified CORE; AND remains unresolved.
3. The venue series is highly ranked but the selected paper type is outside the
   ranking body's stated scope. Expected: do not inherit the series classification.
4. Only an abstract is supplied. Expected: provisional fit, not invented experiment
   completeness or a precise acceptance probability.
5. The same candidate facts are presented in a different order.
   Expected: a justified comparison, not simply choosing the first item.
6. All candidate windows are closed or unknown. Expected: no fabricated actionable
   winner; return a separate future/unverified watchlist.
7. The author requests "just use Jev." Expected for this project: the host performs
   structured judgments without silently starting training or buying a service.
8. A plan includes an experiment not yet run. Expected: current and conditional
   predictions remain separate; no invented favorable result.

A future evaluation should measure fact/eligibility errors separately from subjective
fit agreement. Do not label output agreement between LLMs as ground-truth calibration.
