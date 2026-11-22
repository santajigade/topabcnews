---
title: "Riemann Hypothesis Proof Claim: What Lean Checks Do and Don't Prove"
slug: "riemann-hypothesis-proof-claim-claude-lean-explained"
description: "Levent Alpoge says he proved the Riemann hypothesis with Claude. Lean checks passed, but no human has read it all. What is verified and what the $1M rules need."
date: 2026-11-22T15:56:00+05:30
category: "Science"
tags: ["Riemann hypothesis", "mathematics", "AI", "Lean proof assistant", "Millennium Prize"]
keywords: "Riemann hypothesis proof, Levent Alpoge Claude, Lean formal proof, Millennium Prize"
image: "/images/posts/riemann-hypothesis-proof-claim-claude-lean-explained.webp"
imageAlt: "Riemann Hypothesis proof claim explainer featured image"
author: "Santaji Gadepatil"
sources:
  - name: "Al Jazeera, Riemann hypothesis: Has the world's most famous maths problem been cracked?"
    url: "https://www.aljazeera.com/news/2026/11/21/riemann-hypothesis-has-the-worlds-most-famous-maths-problem-been-cracked"
  - name: "Michael Rubinstein, University of Waterloo, Alpoge/Claude proof of the Generalized Riemann Hypothesis"
    url: "https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/"
  - name: "Clay Mathematics Institute, Millennium Prize rules"
    url: "https://www.claymath.org/millennium-problems/rules/"
  - name: "Clay Mathematics Institute, Riemann Hypothesis"
    url: "https://www.claymath.org/millennium/riemann-hypothesis/"
  - name: "Clay Mathematics Institute, Millennium Problems"
    url: "https://www.claymath.org/millennium-problems/"
---

On November 20, 2026, Levent Alpoge, a mathematician on Anthropic's technical staff, announced that he had found a proof of the Riemann hypothesis with help from the company's AI model Claude. The claim covers both the original hypothesis, proposed by Bernhard Riemann in 1859, and the generalised version for Dirichlet L-functions. The proof was released as code for the Lean proof assistant, about 17 million lines spread over 175,187 files, along with a short four-page explanation instead of a conventional paper.

Computer checks run by mathematicians at the University of Waterloo, MIT and elsewhere have so far passed. But as of November 21, Al Jazeera reported that no human had read through the whole argument. A computer confirming a proof is not the same as mathematicians understanding it.

## What Alpoge Is Claiming

The Riemann hypothesis is one of the seven Millennium Prize Problems set by the <a href="https://www.claymath.org/millennium/riemann-hypothesis/" target="_blank" rel="noopener">Clay Mathematics Institute</a>, each carrying a $1 million prize. It has stayed unsolved for 167 years.

Alpoge wrote that, working with Claude, he believes he has found a proof, and added that "Claude far outpaced me near the finish line." The announcement went up on his personal website. A separate 165-page working draft dated November 21 explains the argument for the Riemann zeta function, and the draft says it was written with Claude, Codex and Gemini.

## The Hypothesis in Plain Words

Prime numbers, such as 2, 3, 5, 7 and 11, cannot be split into a product of two smaller whole numbers. They appear scattered without an obvious pattern. Riemann noticed that how often primes appear is tied to a function called the zeta function. His hypothesis says all the "interesting" points where this function equals zero lie on one vertical straight line, the line where the real part is 1/2.

The Clay Institute notes that this has already been checked for the first 10 trillion such zeros. Checking examples is not a proof, though. A proof would show it holds for every one of them, and that would settle many open questions about how primes are spread out. Kevin Buzzard, professor of pure mathematics at Imperial College London, told Al Jazeera that cryptographers already assume the generalised hypothesis is true, which links it to internet security.

## What the Lean Checks Have Confirmed So Far

Lean is software that checks each logical step of a proof mechanically. If the code compiles and its kernel accepts it, every step follows from the stated rules. Here is what Michael Rubinstein of the University of Waterloo reported on his <a href="https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/" target="_blank" rel="noopener">verification page</a>, with results dated November 21.

| Check | Result reported |
|---|---|
| Do all modules compile? | Yes, all 175,187 |
| Which axioms do the five main theorems rely on? | Only Lean's three standard axioms |
| Replay through Lean's kernel | All 175,187 modules accepted |
| Independent checker (nanoda) | 1,484,729 declarations checked, no errors |
| Can others repeat the checks? | Yes, scripts and a dated log are published |

Others named on the page as running their own checks include Andrew Sutherland of MIT, Simon DeDeo, who replayed all modules through Lean's kernel, Elliot Arledge, who did an independent rebuild and axiom audit, and Bartosz Naskrecki, who runs a dashboard tracking who has checked what.

## What Is Still Unverified

The Lean checks show the code is internally sound. Three questions remain open.

- **Does the code state the right theorem?** Experts still need to confirm that the statements in Lean match what mathematicians mean by the Riemann hypothesis and its generalised form. Rubinstein's page does not report a finished check of this.
- **Why is it true?** Buzzard told Al Jazeera, "At the minute, we don't even know why the theorem is true." He expects people to understand the code "within a week or two."
- **Is the written explanation complete?** The 165-page draft reduces the problem to one inequality over weighted sums of primes, labelled (M). The draft itself says (M) is not proved in the paper and is taken from the Lean development.

Buzzard also said it is not yet clear how much of the work is new ideas and how much is standard machinery the AI built up. Abhishek Saha, professor of mathematics at Queen Mary University of London, told Al Jazeera the claim, if correct, "shatters my model of reality." He also said credit should go to Alpoge rather than to Claude.

## Why the $1 Million Prize Will Not Come Soon

Even if mathematicians accept the proof, the Clay prize has fixed <a href="https://www.claymath.org/millennium-problems/rules/" target="_blank" rel="noopener">rules adopted in 2018</a>. The institute does not take direct submissions. Before it considers a solution, three conditions must all be met:

1. The solution is published in a qualifying outlet.
2. At least two years have passed since publication.
3. The solution has general acceptance in the world mathematics community.

A website post and a code archive do not yet meet the first condition. So the earliest a prize could be considered is two years after a formal publication, and only once the field broadly agrees the proof is correct. The prizes were announced in Paris on May 24, 2000, with a $7 million fund split equally across the seven problems.

## AI and Mathematics: Context From Recent Months

Al Jazeera noted that OpenAI said in September that an unreleased model had solved the Navier-Stokes Millennium problem, which Buzzard described as mainly of theoretical interest compared with Riemann. An earlier AI-assisted result had shown that at least 67.25% of a particular set of values behave as the hypothesis predicts. The new claim, if it holds, would cover all of them.

Anthropic itself has been in the news this month for its stock market debut, covered in our report on the <a href="/anthropic-ipo-price-range-70-78-nasdaq/">Anthropic IPO price range</a>.
