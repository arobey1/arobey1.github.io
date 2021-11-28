---
title: "Learning Robust Output Control Barrier Functions from Safe Expert Demonstrations"
authors: "Alexander Robey, Lars Lindemann, Lejun Jiang, Stephen Tu, Nikolai Matni"
venue: "Preprint"
date: 2021-10-22
pdf: "https://arxiv.org/pdf/2111.09971v1.pdf"
draft: false
github: "https://github.com/unstable-zeros/learning-rocbfs"
---


**Abstract.**  This paper addresses learning safe control laws from expert demonstrations. We assume that appropriate models of the system dynamics and the output measurement map are available, along with corresponding error bounds. We first propose robust output control barrier functions (ROCBFs) as a means to guarantee safety, as defined through controlled forward invariance of a safe set. We then present an optimization problem to learn ROCBFs from expert demonstrations that exhibit safe system behavior, e.g., data collected from a human operator. Along with the optimization problem, we provide verifiable conditions that guarantee validity of the obtained ROCBF. These conditions are stated in terms of the density of the data and on Lipschitz and boundedness constants of the learned function and the models of the system dynamics and the output measurement map. When the parametrization of the ROCBF is linear, then, under mild assumptions, the optimization problem is convex. We validate our findings in the autonomous driving simulator CARLA and show how to learn safe control laws from RGB camera images.