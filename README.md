# Flux extraction tool for weak emission lines using a proxy of a stronger line

This tool is used for identify the location and line width of the emission lines accurately and systematically. Even for non-detections, we want to measure the best possible line flux upper limits. 
The main idea of the tool is to use the strongest line in the same observation (e.g., CO near to H30α) to produce a spatial and velocity mask to extract weak emission line flux and achieve the best S/N, assuming the emitting region and line profiles are the
similar for the strong molecular line and the weak emission line.
For the first order estimation, we used the bright continuum emission as the proxy to identify the possible source region. 
For a more accurate estimation of the source location, moment 0 map of the strongest line was created using the CASA task immoment. The off-the-target noise (σ) in this moment 0 map was measured within a specified box outside the target. We used this moment 0 map, and σ to select the region for line flux extraction.
