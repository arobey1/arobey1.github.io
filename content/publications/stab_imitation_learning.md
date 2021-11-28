---
title: "On the Sample Complexity of Stability Constrained Imitation Learning"
authors: "Stephen Tu, Alexander Robey, Tingnan Zhang, and Nikolai Matni"
venue: "Preprint"
date: 2021-08-06
pdf: "https://arxiv.org/pdf/2102.09161.pdf"
draft: false
github: "#"
mathjax: true
---

**Abstract.** We study the following question in the context of imitation learning for continuous control: how are the underlying stability properties of an expert policy reflected in the sample-complexity of an imitation learning task? We provide the first results showing that a surprisingly granular connection can be made between the underlying expert system’s incremental gain stability, a novel measure of robust convergence between pairs of system trajectories, and the dependency on the task horizon $T$ of the resulting generalization bounds. In particular, we propose and analyze incremental gain stability constrained versions of behavior cloning and a DAgger-like algorithm, and show that the resulting sample-complexity bounds naturally reflect the underlying stability properties of the expert system. As a special case, we delineate a class of systems for which the number of trajectories needed to achieve $\epsilon$-suboptimality is sublinear in the task horizon $T$, and do so without requiring (strong) convexity of the loss function in the policy parameters. Finally, we conduct numerical experiments demonstrating the validity of our insights on both a simple nonlinear system for which the underlying stability properties can be easily tuned, and on a high-dimensional quadrupedal robotic simulation.