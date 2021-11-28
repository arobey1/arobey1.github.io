---
title: "Learning Robust Hybrid Control Barrier Functions from Data"
authors: "Lars Lindemann, Haimin Hu, Alexander Robey, Hanwen Zhang, Dimos V. Dimarogonas, Stephen Tu, and Nikolai Matni"
venue: "CoRL 2020"
date: 2020-10-16
pdf: "https://arxiv.org/pdf/2011.04112.pdf"
draft: false
github: "https://github.com/unstable-zeros/learning-hcbfs"
---

**Abstract.** Motivated by the lack of systematic tools to obtain safe control laws for hybrid systems, we propose an optimization-based framework for learning certifiably safe control laws from data. In particular, we assume a setting in which the system dynamics are known and in which data exhibiting safe system behavior is available. We propose hybrid control barrier functions for hybrid systems as a means to synthesize safe control inputs. Based on this notion, we present an optimization-based framework to learn such hybrid control barrier functions from data. Importantly, we identify sufficient conditions on the data such that feasibility of the optimization problem ensures correctness of the learned hybrid control barrier functions, and hence the safety of the system. We illustrate our findings in two simulations studies, including a compass gait walker.