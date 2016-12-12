#py-gazzetta-live

It is a small cmd-line app for scraping live play-by-play messages of football players of interest.
The idea is that you insert a list of players you are interested in tracking the current live performance.
The app automatically finds the current live matches and then it inspects them whether they involve some players
of your interest.

##Instructions
- Run *python app.py*
- Enter a separated list of players one by one in this format **PLAYER|TEAM** (ie. **Icardi|Inter**)
- To terminate the list enter an empty line
- Enjoy

##Maintenance
I do not plan to maintain this long-term so I encourage everyone to hack on the source code, there are some questions which I did not yet investigate.
It can be extended to support other useful features.
For my needs a boring cmd-line app did the job.