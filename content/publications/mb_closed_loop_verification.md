---
title: "Data-Driven Modeling and Verification of Perception-Based Autonomous Systems"
authors: "Thomas Waite, Alexander Robey, Hamed Hassani, George J. Pappas, Radoslav Ivanov"
venue: "Preprint"
date: 2023-12-11
pdf: "https://arxiv.org/pdf/2312.06848.pdf"
draft: false
github: "https://github.com/waite116/MountainCarVerification"
mathjax: true
---

**Abstract.** This paper addresses the problem of data-driven modeling and verification of perception-based autonomous systems. We assume the perception model can be decomposed into a canonical model (obtained from first principles or a simulator) and a noise model that contains the measurement noise introduced by the real environment. We focus on two types of noise, benign and adversarial noise, and develop a data-driven model for each type using generative models and classifiers, respectively. We show that the trained models perform well according to a variety of evaluation metrics based on downstream tasks such as state estimation and control. Finally, we verify the safety of two systems with high-dimensional data-driven models, namely an image-based version of mountain car (a reinforcement learning benchmark) as well as the F1/10 car, which uses LiDAR measurements to navigate a racing track.