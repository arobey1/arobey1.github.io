---
title: "Learning control barrier functions from expert demonstrations"
authors: "Alexander Robey, Haimin Hu, Lars Lindemann, Hanwen Zhang, Dimos V. Dimarogonas, Stephen Tu, Nikolai Matni"
venue: "CDC 2020"
date: 2020-12-14
pdf: "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9303785&casa_token=dXOexrPhjFAAAAAA:iP8CcJAudz54yoBQVNmC6BiCjTrLISbeCihP_lgvJASH9tdGlRkyhJEwMBHDb9ylRVzkQPD3HQ&tag"
draft: false
github: "https://github.com/unstable-zeros/learning-cbfs"
---

**Abstract.** Inspired by the success of imitation and inverse reinforcement learning in replicating expert behavior through optimal control, we propose a learning based approach to safe controller synthesis based on control barrier functions (CBFs). We consider the setting of a known nonlinear control affine dynamical system and assume that we have access to safe trajectories generated by an expert - a practical example of such a setting would be a kinematic model of a self-driving vehicle with safe trajectories (e.g., trajectories that avoid collisions with obstacles in the environment) generated by a human driver. We then propose and analyze an optimization based approach to learning a CBF that enjoys provable safety guarantees under suitable Lipschitz smoothness assumptions on the underlying dynamical system. A strength of our approach is that it is agnostic to the parameterization used to represent the CBF, assuming only that the Lipschitz constant of such functions can be efficiently bounded. Furthermore, if the CBF parameterization is convex, then under mild assumptions, so is our learning process. We end with extensive numerical evaluations of our results on both planar and realistic examples, using both random feature and deep neural network parameterizations of the CBF. To the best of our knowledge, these are the first results that learn provably safe control barrier functions from data.