# Houston_street_flooding
Experimenting with predicting street flooding during the 2017 Subsurface Hackathon in Houston

## The basic idea

  * Hydrologic models and historical discharge predict flooding in floodplains very well
  * Hydrologic models do not predict local street flooding and ponding
      - Clogged storm drains, etc
  * Detailed topography can help predict localized flooding
      - e.g. Is the area very flat?
      - Are we in a local low point (even one that drains)?

### So, let's train a classifier on features extracted from LIDAR-based DEMs

  * Local slope, relief, etc in a moving window.

### What do we train it on?

  * UFlood/floodmap.io database dump: https://www.dropbox.com/sh/5757a3ujflzdwxo/AAAFD97LMXCRe0YW1HMJDvQ-a?dl=0
  * Crowdsourced street flooding information during Hurricane Harvey
  * Gives us detailed info about which streets flooded, even when houses didn't

### Train it on data from all of Houston, predict on a small area (time constraints)

# Presentation
https://docs.google.com/presentation/d/1djExE4mQNk-_jCY1pz77aR7MoX_Mmvv3-FiGXXmeTbU/edit?usp=sharing

# Prediction for small area
http://bl.ocks.org/d/d0ca5528514c43265517f36440d990f5
