"""
Modeling approach:
  * define Petri nets in terms of their transactions
  * define transactions in terms of the actions of their arcs
  * define arcs in terms with their action on their in- or outgoing place
  * define places as basic containers
  
Run with python 2 or 3, for the example coded up in in __main__, via
  python petri_net.py --firings 10 --marking 1 2 3 2
  
References:
 * https://en.wikipedia.org/wiki/Petri_net
 * https://www.amazon.com/Understanding-Petri-Nets-Modeling-Techniques/dp/3642332773
"""

class Place:
    def __init__(self, holding):
        """
        Place vertex in the petri net.
        :holding: Numer of token the place is initialized with.
        """
        self.holding = holding

    
class ArcBase:
    def __init__(self, place, amount=1):
        """
        Arc in the petri net. 
        :place: The one place acting as source/target of the arc as arc in the net
        :amount: The amount of token removed/added from/to the place.
        """
        self.place = place
        self.amount = amount
        

class Out(ArcBase):
    def trigger(self):
        """
        Remove token.
        """
        self.place.holding -= self.amount
        
    def non_blocking(self):
        """
        Validate action of outgoing arc is possible.
        """
        return self.place.holding >= self.amount 
        

class In(ArcBase):  
    def trigger(self):
        """
        Add tokens.
        """
        self.place.holding += self.amount
            

class Transition:
    def __init__(self, out_arcs, in_arcs):
        """
        Transition vertex in the petri net.
        :out_arcs: Collection of ingoing arcs, to the transition vertex.
        :in_arcs: Collection of outgoing arcs, to the transition vertex.
        """
        self.out_arcs = set(out_arcs)
        self.arcs = self.out_arcs.union(in_arcs)
        
    def fire(self):
        """
        Fire!
        """  
        not_blocked = all(arc.non_blocking() for arc in self.out_arcs) 
        # Note: Has to be checked differently for arcs that compete for holdings.
        if not_blocked:
            for arc in self.arcs:
                arc.trigger()
        return not_blocked # return if fired, just for the sake of debuging
    

class PetriNet:
    def __init__(self, transitions):
        """
        The petri net runner.
        :transitions: The transitions encoding the net.
        """
        self.transitions = transitions
    
    def run(self, firing_sequence, ps):
        """
        Run the petri net.
        Details: This is a loop over the transactions firing and then some printing.
        :firing_sequence: Sequence of transition names use for run.
        :ps: Place holdings to print during the run (debugging).
        """
        
        print("Using firing sequence:\n" + " => ".join(firing_sequence))
        print("start {}\n".format([p.holding for p in ps]))
        
        for name in firing_sequence:
            t = self.transitions[name]
            if t.fire():
                print("{} fired!".format(name))
                print("  =>  {}".format([p.holding for p in ps]))
            else:
                print("{} ...fizzled.".format(name))
        
        print("\nfinal {}".format([p.holding for p in ps]))
            

def make_parser():
    """
    :return: A parser reading in some of our simulation paramaters.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--firings', type=int)
    parser.add_argument('--marking', type=int, nargs='+')
    return parser


if __name__ == "__main__":    
    args = make_parser().parse_args()

    ps = [Place(m) for m in args.marking]
    ts = dict(
        t1=Transition(
            [Out(ps[0])], 
            [In(ps[1]), In(ps[2])]
            ),
        t2=Transition(
            [Out(ps[1]), Out(ps[2])], 
            [In(ps[3]), In(ps[0])]
            ),
        )
        
    from random import choice
    firing_sequence = [choice(list(ts.keys())) for _ in range(args.firings)] # stochastic execution
    
    #firing_sequence = ["t1", "t1", "t2", "t1"] # alternative deterministic example

    petri_net = PetriNet(ts)
    petri_net.run(firing_sequence, ps)
    
