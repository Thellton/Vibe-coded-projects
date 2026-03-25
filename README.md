a little explainer, this is principally an archive of select vibe-coded projects from my hard drive that are provided as is and are not intended for actual use. 
however they are intended as an educational resource and for discussion on programming in the ever evolving modern era. 

in this repo, there are three projects. the first is a simple single file python script that I prompted various cloud LLMs to create called "PERF_CALC.py". 
it has no dependencies other than having some form of Python 3.XX (3.10 is what it was developed with) so one can just double click it in windows to launch it.
it is intended for helping understand to some degree the resources required for running LLMs, that being bandwidth, FLOPs, Tk/s, and storage requirements. 
the tab devoted to training is in my opinion inaccurate and highly likely to present an innaccurate idea of how long it would take to train and this is principally because of poor understanding on my part whilst prompting for that part of the script.

the second is a reimplementation of "PERF_CALC.py" in C#. structurally it is the exact same barring the training tab, and whilst I'm not certain of the accuracy if applied to modern architectures, it may be fairly representative for GPT-2. 

the third is a simple tkinter based LLM chat interface. there were a number of features that I intended to add and never got round to, and google's "google-generativeai" package is no longer maintained and is probably non-functional. fortunately, you can run llama-server to use the interface if you wish. 

the third program of these three, to me is the most interesting. it took me a month to arrive at a functioning form of that project in the form of a procedural code form (I never really got object oriented coding when I first tried it back in 2012). when I was working on this with GPT-4 before it was replaced by GPT-4o, by the end of the month, GPT-4o was ignoring instructions and attempting to rewrite the program to be object oriented. at the time, it seems it could tell the program was basically spaghetti code with a bad code smell, but it took the transition from 4 to 4o for ChatGPT to actually stop and essentially say "hey... this is an unmanageable mess... we need to fix that."

anyway, it took one month to write the procedural coded version through back and forth conversation with GPT-4 and frequent context hopping; it took one day for GPT-4o to convert it to object oriented. 
