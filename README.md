# Blood Type Modeling
This is a quick attempt to resolve a question that came up in a discussion with some friends. I was trying to understand why the recessive blood type 'o' would not disappear over time.

## Results
The o blood type does not die out because there is always a population of 'ao' and 'bo' that 'downconvert' to 'oo'. In other words, just because someone is of blood type 'a' or 'b', that does not mean that an offspring cannot be 'oo'. I had forgotten this in the discussion with friends which was the cause of my confusion.

![Simulation Results](https://github.com/nleehone/blood_type_simulation/raw/master/results.png)

One interesting and unexpected result of the simulation is that there is a strong correlation between the 'ab' and 'o', and between the 'a' and 'b' blood types. When 'a' increases, 'b' decreases, but 'ab' and 'o' are unaffected. **I would love to hear why this might be the case.**

## Optimization
The code started with strings representing the different blood types, but this was too slow. The code was then optimized by using kernprof and the line_profiler. After converting to using integers to represent the blood types the code ran about 100 times faster.
