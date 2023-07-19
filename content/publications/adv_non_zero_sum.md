---
title: "Adversarial Training Should Be Cast As a Non-Zero-Sum Game"
authors: "Alexander Robey, Fabian Latorre, Hamed Hassani, George J. Pappas, Volkan Cevher"
venue: "Preprint"
date: 2023-07-19
pdf: "https://arxiv.org/pdf/2306.11035.pdf"
draft: false
github: "#"
mathjax: true
---


**Abstract.** One prominent approach toward resolving the adversarial vulnerability of deep neural networks is the two-player zero-sum paradigm of adversarial training, in which predictors are trained against adversarially-chosen perturbations of data. Despite the promise of this approach, algorithms based on this paradigm have not engendered sufficient levels of robustness, and suffer from pathological behavior like robust overfitting. To understand this shortcoming, we first show that the commonly used surrogate-based relaxation used in adversarial training algorithms voids all guarantees on the robustness of trained classifiers. The identification of this pitfall informs a novel non-zero-sum bilevel formulation of adversarial training, wherein each player optimizes a different objective function. Our formulation naturally yields a simple algorithmic framework that matches and in some cases outperforms state-of-the-art attacks, attains comparable levels of robustness to standard adversarial training algorithms, and does not suffer from robust overfitting.