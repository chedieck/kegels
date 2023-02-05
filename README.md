Kegels
---


[Kegel exercises](https://en.wikipedia.org/wiki/Kegel_exercise) are exercises for strengthening the pelvic-floor muscles.

This repo intends to provided a way to do them in a guided way. E.g:
- Hold for N seconds, release for M...
- Go on holding tighter for the length of N seconds... Then keep it fully held for another N seconds... Then go releasing slowly for N seconds... Then keep it fully released for N seconds...

<p align="center" >
<img width="50%"  src="https://user-images.githubusercontent.com/21281174/216840180-16bbeb2d-d198-4486-87a8-3e85dccf183a.png"> 
<p>
<p align="center" >

# Configuring
Edit the file `main.py`, some example routines `first_routine()` and `second_routine()` are provided. You can modify those, create another ones, and them just call them on `main()`.

# Installing & Using
- `git clone https://github.com/chedieck/kegels.git`;
- `cd kegels`
- `pip install termcolor` is the only requirement;
- `python main.py` will run one of the example routines.

Furthermore, you can make some alias like `alias kegels='python ~/path/to/repo/main.py'` so you can just open up a terminal and run `kegels`.
