### Petri nets in python

A quick implementation of a Petri net runner in python.
  
Run with python 2 or 3, for the example coded up in in `__main__`, via

```bash
python petri_net.py --firings 10 --marking 1 2 3 2
```

#### Modeling approach
  * define Petri nets in terms of their transactions
  * define transactions in terms of the actions of their arcs
  * define arcs in terms with their action on their in- or outgoing place
  * define places as basic containers
  
#### Documentation

https://youtu.be/VW0RAonW8Aw
  
#### References:
 * https://en.wikipedia.org/wiki/Petri_net
 * https://www.amazon.com/Understanding-Petri-Nets-Modeling-Techniques/dp/3642332773
