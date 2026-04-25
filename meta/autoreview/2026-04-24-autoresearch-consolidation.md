---
type: meta
title: "Autoresearch Consolidation — 2026-04-24"
created: 2026-04-24
updated: 2026-04-24
tags:
  - meta
  - autoreview
  - consolidation
  - autoresearch
---

# Autoresearch Consolidation — 2026-04-24

Three parallel autoresearch agents completed synthesis sweeps on:

1. **Stability Theory for Latent Recurrence** — Jacobian / Parseval / noise / DEQ / Lyapunov menu targeting F1-F6 routing-lock failures.
2. **Info and Distribution Constraints for Latents** — VIB / CEB / HSIC-IB / VICReg / Barlow / InfoNCE regularizers mapped to F3/F5/F6.
3. **Disentanglement and Sparse Coding for Latents** — Superposition + SAE + causal-disentanglement toolkit for F3 template-lock.

Each agent created sources/concepts/entities/questions pages and appended to `log.md`. Per instruction, they did NOT touch `index.md` or `hot.md`. This file records the consolidation.

## Pages added this batch (counts by type)

| Type | Stability | Info/Dist | Disentanglement | Total |
|---|---|---|---|---|
| Synthesis (questions/) | 1 | 1 | 1 | **3** |
| Sources | 7 | 10 | 5 | **22** |
| Concepts | 5 | 4 | 5 | **14** |
| Entities | 3 | 1 | 3 | **7** |
| **Per-session total** | **16** | **16** | **14** | **46** |

**Net count: 46 new wiki pages this batch.**

### Source breakdown

- **Stability (7):** [[Deep Equilibrium Models]], [[Stabilizing Equilibrium Models by Jacobian Regularization]], [[Resurrecting the Sigmoid Dynamical Isometry]], [[Parseval Networks]], [[Orthogonal Recurrent Networks]], [[Noisy Recurrent Neural Networks]], [[Robust Learning with Jacobian Regularization]].
- **Info/Dist (10):** [[Deep Variational Information Bottleneck]], [[Conditional Entropy Bottleneck]], [[HSIC Bottleneck]], [[VICReg]], [[Barlow Twins]], [[Contrastive Predictive Coding]], [[InfoVAE]], [[Continuous Autoregressive Language Models]], [[KL-Regularized RL is Designed to Mode Collapse]], [[Emergence of Invariance and Disentanglement]].
- **Disentanglement (5):** [[Toy Models of Superposition]], [[Towards Monosemanticity]], [[Sparse Feature Circuits]], [[How does Chain of Thought Think]], [[Step-Level Sparse Autoencoder]].

### Concept breakdown

- **Stability (5):** [[Fixed-Point Iteration]], [[Deep Equilibrium Model (DEQ)]], [[Lyapunov Stability]], [[Spectral Regularization]], [[Jacobian Constraint]].
- **Info/Dist (4):** [[Variational Information Bottleneck]], [[Conditional Entropy Bottleneck]] (concept-flavored; same filename as source paper — see hygiene issues below), [[Whitening-Based Anti-Collapse]], [[Distribution Regularizer Catalog]].
- **Disentanglement (5):** [[Superposition]], [[Sparse Autoencoder]], [[Feature Absorption and Splitting]], [[Matryoshka Sparse Autoencoder]], [[Causal Disentanglement]].

### Entity breakdown

- **Stability (3):** [[Shaojie Bai]], [[J. Zico Kolter]], [[Jeffrey Pennington]].
- **Info/Dist (1):** [[Alex Alemi]].
- **Disentanglement (3):** [[Nelson Elhage]], [[Samuel Marks]], [[Bernhard Schölkopf]].

## Cross-cutting themes spotted across the 3 syntheses

### Theme 1: The same math problem viewed from three angles

The three syntheses converge on a single diagnosis of the F-battery failures expressed in different mathematical vocabularies:

| Failure | Stability framing | Info-theoretic framing | Disentanglement framing |
|---|---|---|---|
| **F3 template-lock** | Rank-1 Jacobian; $\rho(J_f)$ uncontrolled | Posterior collapse; per-dim KL at lower bound | Position-granularity superposition |
| **F5 swap-null** | No-recall fixed point (Labovich countability theorem) | $I(Z;Y|x) \approx 0$; InfoNCE training signal absent | Basis mismatch — content exists but decoder reads orthogonal direction |
| **F6 narrow basin** | Jacobian Lipschitz $L \geq 1.3$ per step → 8× amplification | VICReg variance hinge violation | (Not directly addressed — overlaps with F3 via compressed representation) |

Each framing yields a different intervention family, but the interventions are mutually compatible (not competing). Example: noise injection (stability) ≡ Jacobian-Frobenius reg ≡ variance-hinge regularization at the statistical level.

### Theme 2: CPF is load-bearing across all three framings

[[Context-Prediction-Fusion]] is independently re-derived as:
- **Stability:** a "recall-mode" DEQ anchor that makes the fixed point input-dependent (cures F5 via Labovich theorem).
- **Info-theoretic:** an implicit VIB with $h_\text{ctx} \leftrightarrow$ forward encoder and $e_\text{pred} \leftrightarrow$ backward encoder (CEB formalizes it with learnable $\gamma$).
- **Disentanglement:** the auxiliary-variable inductive bias that breaks Locatello's unsupervised-disentanglement impossibility theorem.

This upgrades CPF from "empirically convergent five-group reinvention" to "theoretically load-bearing instantiation of at least three independently-motivated necessary biases." Strongest theoretical footing the project now has.

### Theme 3: Zero-cost interventions cluster at the top of all three ranked menus

- Stability: noise injection ($\sigma = 0.1$, 0% compute, 0.5 day eng).
- Info/Dist: VICReg variance hinge (batch-local, no prior, detach-compatible).
- Disentanglement: orthogonality penalty on latent-position Gram (per-example, batch-level variants).

All three agree: start with zero-cost interventions, validate with the F-battery, escalate to compute-heavier regularizers only if needed. This gives a concrete execution ordering for Branch D V3.

### Theme 4: The F-battery is a measurement artifact of well-known pathologies

F3/F5/F6 are not novel failure modes. They are:
- F3: polysemanticity/superposition at position-granularity ([[Toy Models of Superposition]] 2022).
- F5: no-recall fixed-point non-input-dependence (Labovich 2026 theorem, pre-existing vault source).
- F6: uncontrolled Jacobian spectral radius (Bai-Kolter DEQ literature 2019-2021).

The writeup gains authority by citing canonical literature for each pathology rather than presenting them as novel empirical findings.

### Theme 5: KL-regularized RL is a landmine

[[KL-Regularized RL is Designed to Mode Collapse]] (Oct 2025) proves mode collapse at the global optimum, not as an optimization artifact. Any downstream RL step (GRPO, PPO, DPO) on a CPF-stabilized model will undo the anti-collapse gains unless MARA-style reward shaping is added. This is a negative result that must be cited in the writeup and baked into Branch D / Branch A RL plans.

## New concepts + what branches they enable

| Concept | Primary branch enablement | What it unlocks |
|---|---|---|
| [[Fixed-Point Iteration]] | Branch B | Reframes detach-vs-no-detach as "DEQ or not"; correct diagnostic axis |
| [[Deep Equilibrium Model (DEQ)]] | Branch B (north-star), Branch A (scaling) | Target architecture for "CODI done right"; IFT gradient replaces V2 detach |
| [[Lyapunov Stability]] | Branch D | Orthogonal to CPF attractor-shaping; learned $V(z;x)$ decrease condition |
| [[Spectral Regularization]] | Branch B, Branch D | Weight-level implementation family (Parseval / orthogonal init / spectral margin) |
| [[Jacobian Constraint]] | Branch B, Branch D, Branch A | Most portable intervention menu |
| [[Variational Information Bottleneck]] | Branch D | CPF-as-IB formalism; handle on $\beta$ scheduling and posterior-collapse diagnostics |
| [[Whitening-Based Anti-Collapse]] | Branch B, Branch D | Batch-local, prior-free, detach-compatible — cheap additions to existing harness |
| [[Distribution Regularizer Catalog]] | Branch D | Equation-level menu mapping each regularizer to a specific F-failure |
| [[Superposition]] | Branch C, writeup | Canonical framework for F3 template-lock |
| [[Sparse Autoencoder]] | Branch C | Principled basis for the LTO-vs-DDR probe typology resolution |
| [[Feature Absorption and Splitting]] | Branch C | Failure mode to watch for in naive SAE applications |
| [[Matryoshka Sparse Autoencoder]] | Branch C | Absorption-resistant variant; primary candidate for F3 probe construction |
| [[Causal Disentanglement]] | Branch D, writeup | Impossibility theorem grounds CPF as theoretically necessary |

## Deduped concepts flagged for later merge / disambiguation

### CRITICAL: Filename collision on "Conditional Entropy Bottleneck"

Two pages share the filename `Conditional Entropy Bottleneck.md`:
- **`wiki/sources/Conditional Entropy Bottleneck.md`** — Fischer 2020 source paper, `type: source`.
- **`wiki/concepts/Conditional Entropy Bottleneck.md`** — concept page with title "Conditional Entropy Bottleneck (concept)", `type: concept`, aliases `[CEB, Fischer Bottleneck, Minimum Necessary Information]`.

Obsidian wikilinks to `[[Conditional Entropy Bottleneck]]` will be ambiguous — Obsidian may resolve to whichever file it finds first in its index, and this depends on resolution order. The concept page even links to `[[Conditional Entropy Bottleneck]]` in its own `related:` field, which will either self-loop or point to the source paper depending on Obsidian's heuristic.

**Recommended action:** rename the concept file to `Conditional Entropy Bottleneck (concept).md` or `CEB (concept).md` to match its frontmatter title, OR merge the two pages and use heading anchors for the source/concept split.

Leaving this as a wiki-lint / next-sweep action — do not fix during consolidation (rule: do not modify new pages in this pass).

### Duplicate concept-vs-source pattern for VIB (handled cleanly)

[[Variational Information Bottleneck]] (concept) vs [[Deep Variational Information Bottleneck]] (source paper, Alemi et al. 2017). These have distinct filenames, so no collision. This is the correct pattern the CEB pages should follow.

### No other duplicates spotted

- DEQ appears in both the stability synthesis (primary topic) and is referenced in the disentanglement synthesis as a related concept, but only the stability session created pages. No duplicate concept pages.
- No competing "Information Bottleneck" / "VIB" pages between sessions.

## Wiki-hygiene issues spotted

1. **CEB filename collision** (see above). Most important.
2. **Concept page self-reference.** `wiki/concepts/Conditional Entropy Bottleneck.md`'s `related:` field lists `[[Conditional Entropy Bottleneck]]` — this self-links (or, given the collision, points to the source page). Intentional if meant to cross-link source↔concept, but the wikilink target is ambiguous.
3. **Entities mentioned in Info/Dist synthesis prose but not created as wiki entities:** Ian Fischer (CEB author), Naftali Tishby (IB founder), Aaron van den Oord (InfoNCE/CPC), Yann LeCun (VICReg/Barlow senior), Shengjia Zhao / Jiaming Song / Stefano Ermon (InfoVAE). These are mentioned by plain-text name in the synthesis's "Key Entities" section (not wikilinks), so they don't break any links — but they're obvious missing-entity candidates for a follow-up entity-completion pass.
4. **Source-page frontmatter date drift.** Many new source pages show `created: 2026-04-23` but were written during the 2026-04-24 autoresearch session. Harmless but worth noting — the date reflects the autoresearch session start date (Apr 23 in UTC, Apr 24 local?) rather than file creation time. No action needed.
5. **"Stability Theory" source page Deep Equilibrium Models frontmatter lacks created date** (found in `grep created:` scan — shows empty). Minor hygiene issue; the autoresearch agent's template may have omitted it. Not load-bearing for navigation.
6. **Broken wikilinks in syntheses:** none spotted. Every `[[...]]` target in the three syntheses resolves to an actual wiki page. Examples verified: `[[Latent Thoughts Tuning]]`, `[[Routing vs Reasoning]]`, `[[Context-Prediction-Fusion]]`, `[[Feature Collapse]]`, all stability/info/disentanglement concept and source links.
7. **Tag vocabulary drift:** stability synthesis uses `tags: [research, stability-theory, synthesis, latent-reasoning]`; info/dist uses `tags: [research, domain/information-theory, domain/regularization, domain/latent-reasoning, domain/anti-collapse]`; disentanglement uses `tags: [research, domain/interpretability, domain/latent-reasoning, domain/mechanistic]`. Two different tag conventions — some use `domain/...` prefix, one does not. Flag for wiki-lint pass to normalize.

## Summary

**Net new pages: 46** (3 syntheses + 22 sources + 14 concepts + 7 entities).

**Vault totals after this batch:**
- Sources: 86 → 108
- Concepts: 17 → 33
- Entities: 70 → 77
- Syntheses: 0 → 3 (new top-level category in `wiki/questions/`)

**Major structural change:** `wiki/questions/` elevated to first-class top-level section in `index.md`. Prior convention had `questions/` as ad-hoc; now it's the home of consolidated autoresearch syntheses.

**Principal action items for next pass:**
1. Rename `wiki/concepts/Conditional Entropy Bottleneck.md` to disambiguate from source paper.
2. Normalize tag vocabulary across the three syntheses (`domain/` prefix).
3. Consider creating entity pages for Ian Fischer / Aaron van den Oord / Yann LeCun / Naftali Tishby if we deepen in info-theoretic directions.
4. Wiki-lint sweep to catch any missed hygiene issues.
5. Follow-up autoresearch questions already queued:
   - Attention-block Jacobian spectrum (from stability synthesis open Q1).
   - Wasserstein/Sinkhorn for latent CoT (info/dist Q1 — literature gap).
   - SAE on actual CODI latents — does it find features at "empty" positions? (disentanglement Q1 — empirical test).
