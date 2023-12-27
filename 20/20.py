import sys
import numpy as np 
from dataclass import dataclass
from queue import Queue

# modules = {}
# 
# def add_mod(typ, name):
#     if typ == '%':
#         modules[name] = FlipFlop(name)
#     elif typ == '&':
#         modules[name] = Conjunction(name)
#     elif name == 'broadcaster':
#         modules[name] = Broadcaster()
# 
# 
# def get_mod(name):
#     return modules[name]
# 
# 
# class Broadcaster(Module):
#     def __init__(self):
#         self.name = 'broadcaster'
#         self.outputs = []
# 
#     def add_output(self, name):
#         self.outputs.append(name)
# 
#     def trigger(self, level):
#         return [(level,name) for name in self.outputs]
#         
# 
# class FlipFlop:
#     def __init__(self, name):
#         self.name = name
#         self.outputs = []
#         self.level = False
# 
#     def add_input(self, name):
#         pass
# 
#     def add_output(self, name):
#         self.outputs.append(name)
# 
#     def trigger(self, level):
#         if not level:
#             self.level = not self.level
# 
#             for name in self.outputs:
#                 mod = get_mod(name)
#                 mod.trigger(self.level)
# 
#             return True
# 
#         return False
# 
# 
# class Conjunction:
#     def __init__(self, name):
#         self.name = name
#         self.outputs = []
#         self.input_levels = {}
# 
#     def add_input(self, name):
#         self.inputs.append(name)
# 

@dataclass
class Pulse:
    src: str
    dest: str
    level: bool
    

# Get input
inputs = {}
outputs = {}
mod_types = {}

with open(sys.argv[1], 'r') as f:
    inp = [line.strip() for line in f.readlines()]

for line in inp:
    src,dests = line.split(' -> ')
    dests = dests.split(', ')
    if src.startswith('%') or src.startswith('&'):
        mod_types[src[1:]] = src[0]
        src = src[1:]
    else:
        assert src == 'broadcaster'
        mod_types[src] = src

    outputs[src] = []
    for dest in dests:
        outputs[src].append(dest) 
        if dest not in inputs:
            inputs[dest] = []
        inputs[dest].append(src)

conj_memory = {c_mod:{inp:False for inp in inputs[c_mod]} for c_mod in mod_types if mod_types[c_mod] == '&'}

pulses = Queue()
pulses.put(Pulse('button', 'broadcaster', False))

while not pulses.empty():
    pulse = pulses.get()
    print(f'{pulse.src} -{"high" if pulse.level else "low"}-> {pulse.dest}')

    dest_mod_type = mod_types[dest]
    if dest_mod_type == 'broadcaster':
        for output in outputs[pulse.dest]:
            pulses.put((output, level))
