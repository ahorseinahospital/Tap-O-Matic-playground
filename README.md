# What's here

This is a fork of [Tap-O-Matic DDV](https://github.com/abluenautilus/Tap-O-Matic-DDV), itself a fork of [Tap-O-Matic](https://github.com/cormallen/tap-o-matic). I appreciate all of the work that's been put into this module and the OG Time machine. 
Thanks to OAM for making it open source to begin with.  

This a personal playground for vibe coding alternative firmware for Tap-O-Matic (, Time Machine and potentially other daisy modules in the future), and hopefully 
learning something in the process. 
None of it is commercial, there are no warranties or guarantees of any kind, 
so if you're reading this and about to do literally anything with these files, 
the outcome is on you! 

Currently contains only one module, Fox Tail, which is a harmonic oscillator based on Arturia Pigments. 
Fox Tail reuses the hardware part completely keeping the audio logic entirely separate from the OG firmware, thanks to the nice state of the inherited code.

# Fox Tail

A 96-partial additive oscillator: eight geometric bands that fill in as you push
their sliders, an inharmonicity control, and Cluster / Shepard shapers on top.

**[Read the manual](https://ahorseinahospital.github.io/Tap-O-Matic-playground/docs/fox-tail-manual.html)**
— what every control does, patch recipes, calibration, troubleshooting.

Build it with `make MODULE=foxtail` (see the manual's appendix for the toolchain),
or flash `build/Fox-Tail.bin` via https://flash.daisy.audio with the module in DFU
mode. There's also a browser emulator running the identical engine —
`./emulator/run.sh`, then http://localhost:4343.
