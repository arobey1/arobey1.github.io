---
title: "SmoothLLM: Defending LLMs Against Jailbreaking Attacks"
authors: "Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas"
venue: "Preprint"
date: 2023-10-07
pdf: "https://browse.arxiv.org/pdf/2310.03684.pdf"
draft: false
github: "https://github.com/arobey1/smooth-llm"
mathjax: true
---

**Abstract.** Despite efforts to align large language models (LLMs) with human values, widely-used LLMs such as GPT, Llama, Claude, and PaLM are susceptible to jailbreaking attacks, wherein an adversary fools a targeted LLM into generating objectionable content.  To address this vulnerability, we propose SmoothLLM, the first algorithm designed to mitigate jailbreaking attacks on LLMs.  Based on our finding that adversarially-generated prompts are brittle to character-level changes, our defense first randomly perturbs multiple copies of a given input prompt, and then aggregates the corresponding predictions to detect adversarial inputs.  SmoothLLM reduces the attack success rate on numerous popular LLMs to below one percentage point, avoids unnecessary conservatism, and admits provable guarantees on attack mitigation.  Moreover, our defense uses exponentially fewer queries than existing attacks and is compatible with any LLM.