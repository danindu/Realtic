lineartrails
============

Tool to automatically search for linear characteristics. There exists a research
paper about this tool called "Heuristic Tool for Linear Cryptanalysis with
Applications to CAESAR Candidates", which is presented at AsiaCrypt 2015, an
online version is available [here](https://eprint.iacr.org/2015/1200). If you
use this tool in your work, it would be nice to cite the research paper.


Build
-----

`lineartools` requires `tiny2xml` as submodule, so do after `git clone`:

```
git submodule init && git submodule update
```

To build:

```
make
```


Usage
-----

The folder ./examples contains example search configuration for Ascon, ICEPOLE,
Keyak, Minalpher and Proest. To start a search simply call for instance:

```
./lin -I 10 -S 2 -i examples/ascon_3_rounds_typeI.xml
```

* `-I` determines how often status information of the search is displayed.
  `-I -1` deactivates it.
* `-S` determines how often the current and probably partial determined linear
  characteristic is put out. `-S -1` deactivates it.
* `-i` specifies the used xml based search file.

The output of the search are linear characteristics, where Round 0 tags the
linear mask of the input of the first round, Round 1 the output of the first
round, which is also the input for the second round and so on. Half Rounds, e.g.
1.5 represent intermediate result within one round. For instance if one round
consists of a substitution layer followed by a permutation layer, a half round
marks the output of the substitution layer and the input of the permutation
layer.

A search file looks like follows:

```
<config>
<parameters>
  <permutation value="ascon"/>
  <rounds value="3"/>
</parameters>
<char value="
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????1

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????

????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
????????????????????????????????????????????????????????????????
"/>
<search credits = "10000" print_active = "0">
  <phase>
    <setting push_stack = "0.1" alternative_sbox_guesses = "10" sbox_weight_probability = "3"  sbox_weight_hamming = "1">
      <guess sbox_layer="0" active_weight="0" inactive_weight="100"/>
      <guess sbox_layer="1" active_weight="0" inactive_weight="500"/>
      <guess sbox_layer="2" active_weight="0" inactive_weight="500"/>
    </setting>
    <setting push_stack = "0.5" alternative_sbox_guesses = "5">
      <guess sbox_layer="0" active_weight="1" inactive_weight="0"/>
      <guess sbox_layer="1" active_weight="2" inactive_weight="0"/>
      <guess sbox_layer="2" active_weight="3" inactive_weight="0"/>
    </setting>
  </phase>
</search>
</config>
```

In this file, the field `char value` contains the starting point of the search,
where all intermediate masks are considered. Incomplete starting points are
padded with '?'.

The field `credits` determines, how often a contradiction during the search is
backtracked until the current search is re-started. To provide a clear view, the
search only prints better characteristics than already found. With
`print_active` it is determined whether this "best" metric targets active
S-boxes or the bias.

Settings define which S-boxes are guessed and are treated subsequently. So if
there is no guessable S-box in a current setting, the next one is taken.
`push_stack` defines the probability that the current characteristic is pushed
to the stack for a possible later backtracking. `alternative_sbox_guesses`
defines how many other contradicting assignments of linear masks than the best
one defined according to `sbox_weight_probability` and `sbox_weight_hamming`
have to be taken into account until the characteristic is treaded as impossible.
`sbox_weight_probability` and `sbox_weight_hamming` are used to rate masks for
S-boxes. A high value for `sbox_weight_probability` prefers masks that have a
high bias, whereas a high value `sbox_weight_hamming` prefers masks that have a
low hamming weight.

`active_weight` determines the probability that an active S-box will be guessed
(higher values mean higher chance). `inactive_weight` does the same for inactive
S-boxes.

The code snippets describing the behavior of the linear and S-box layer of the
implemented ciphers are taken from their reference implementations, which are
available at <http://bench.cr.yp.to/ebash.html>.

The tool is tested under
- Xubuntu 14.04 (64 bit) using gcc version 4.8.2
- Xubuntu 14.10 (64 bit) using gcc version 4.9.1
- Xubuntu 14.10 (64 bit) using clang (3.8 trunk, Revision 254516)
- Ubuntu 15.04 (64 bit) using gcc version 4.9.2
- OSX Yosemite using Apple LLVM version 6.0

