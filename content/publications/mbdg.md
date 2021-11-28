---
title: "Model-Based Domain Generalization"
authors: "Alexander Robey, George J. Pappas, Hamed Hassani"
venue: "NeurIPS 2021"
date: 2021-11-26
pdf: "https://papers.nips.cc/paper/2021/file/a8f12d9486cbcc2fe0cfc5352011ad35-Paper.pdf"
draft: false
github: "https://github.com/arobey1/mbdg"
---

**Abstract.**  Despite remarkable success in a variety of applications, it is well-known that deep learning can fail catastrophically when presented with out-of-distribution data. Toward addressing this challenge, we consider the domain generalization problem, wherein predictors are trained using data drawn from a family of related training domains and then evaluated on a distinct and unseen test domain. We show that under a natural model of data generation and a concomitant invariance condition, the domain generalization problem is equivalent to an infinite-dimensional constrained statistical learning problem; this problem forms the basis of our approach, which we call Model-Based Domain Generalization. Due to the inherent challenges in solving constrained optimization problems in deep learning, we exploit nonconvex duality theory to develop unconstrained relaxations of this statistical problem with tight bounds on the duality gap. Based on this theoretical motivation, we propose a novel domain generalization algorithm with convergence guarantees. In our experiments, we report improvements of up to 30 percentage points over state-of-the-art domain generalization baselines on several benchmarks including ColoredMNIST, Camelyon17-WILDS, FMoW-WILDS, and PACS.


