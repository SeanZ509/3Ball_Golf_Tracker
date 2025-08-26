1)SCHEDULER/AUTO UPDATE LOGIC:

Main initial scan wednesday (when tee time come out), auto update scores from start of the round until first round complete. 
Write results to CSV/R1
At midnight, initial scan. Auto update scores from start of round till round 2 complete
Write results to CSV/R2
At midnight, initial scan. Auto update scores from start of round till round 3 complete
Write results to CSV/R3
At midnight, initial scan. Auto update scores from start of round till round 4 complete
Write results to CSV/R4
(start of round - 4:30AM every tourney day, round complete check if all players finished)
*We should only attempt to make the End of round results once, lets say once all players finished and the round status ends with Complete, then we maketabround once. 
- Need to test :/

NEXT:
Fix 3Ball index and CSS to match 2ball
Figure out how to use 3ball and 2ball together, this small tournament had groups of 3 and 2
(Scan rows of each group, make group that size?)
Change CSV and functions To Database and queries
Can deploy as app after



Cant get to teetimes page easily, cant find link from schedule to get to tourney to not have to use /leaderboard and get the full link to make it easier

