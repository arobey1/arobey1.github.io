---
title: "Optimal physical preprocessing for example-based super-resolution"
authors: "Alexander Robey and Vidya Ganapati"
venue: "Optics Express"
date: 2018-10-14
pdf: "https://www.osapublishing.org/DirectPDFAccess/3D491818-582A-4986-A7E8444511B898FD_401259/oe-26-24-31333.pdf?da=1&id=401259&seq=0&mobile=no"
draft: false
github: "#"
---

Fourier ptychographic microscopy is a technique that achieves a high space-bandwidth product, i.e. high resolution and high field-of-view. In Fourier ptychographic microscopy, variable illumination patterns are used to collect multiple low-resolution images. These low-resolution images are then computationally combined to create an image with resolution exceeding that of any single image from the microscope. Due to the necessity of acquiring multiple low-resolution images, Fourier ptychographic microscopy has poor temporal resolution. Our aim is to improve temporal resolution in Fourier ptychographic microscopy, achieving single-shot imaging without sacrificing space-bandwidth product. We use example-based super-resolution to achieve this goal by trading off generality of the imaging approach. In example-based super-resolution, the function relating low-resolution images to their high-resolution counterparts is learned from a given dataset. We take the additional step of modifying the imaging hardware in order to collect more informative low-resolution images to enable better high-resolution image reconstruction. We show that this “physical preprocessing” allows for improved image reconstruction with deep learning in Fourier ptychographic microscopy. In this work, we use deep learning to jointly optimize a single illumination pattern and the parameters of a post-processing reconstruction algorithm for a given sample type. We show that our joint optimization yields improved image reconstruction as compared with sole optimization of the post-processing reconstruction algorithm, establishing the importance of physical preprocessing in example-based super-resolution.