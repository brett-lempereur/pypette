# Pypette

Pypette is a platform for the experimental investigation of the
behaviour and effects of live digital forensic tools, techniques, and
evidence.  It was created as part of my PhD thesis, completed in 2013
in the School of Computing and Mathematical Sciences at Liverpool John
Moores University.

## Motivation

Live forensics is an increasingly important part of digital
forensics. It is capable of capturing information that would be lost
after powering off a machine (Lessing & Solms, 2008). This includes
decryption keys for full-disk encryption mechanisms (Casey &
Stellatos, 2008), internet login details (Mohanty & Velusamy, 2012),
and the internal state of the operating system (Walters & Petroni,
2007). In addition to these benefits, the workload of digital forensic
laboratories is increasing, and examiners are turning to live digital
forensic techniques to improve their efficiency (Caloyannides,
2009). The need for live digital forensics will increase as users
become increasingly aware of anti-forensic mechanisms and the
complexity of investigations increases (Caloyannides, Memon, & Venema,
2009).

In tandem with the rise in the importance of live forensics, there is
a need for improved approaches to evaluating live forensic acquisition
methods and evidence (Beebe, 2009). With an increasing number of
challenges to digital evidence, we must be able to establish its
accuracy (Erbacher, 2010). We believe, however, that existing
evaluation mechanisms are insufficient to support the acceptability of
live forensic evidence and meet these challenges. These approaches
have focused on evaluation based on a percentage of memory change
before and after acquiring live forensic evidence (Savoldi & Gubian,
2009; Walters & Petroni, 2007; Vӧmel & Freiling 2012). There is a need
to consider the accuracy and effects of live forensics in terms of the
artefacts examiners actually extract from systems, and the mechanisms
used for achieving this.

The development of live digital forensic techniques has been distinct
from the methods available to evaluate them. This has led to ad-hoc
evaluations, with a qualitative consideration of the improvements
offered by techniques relative to the body of work in the
literature. The aim of our work is to transform this into a scientific
process, with repeatable and quantifiable study of the behaviour of
evidence and its acquisition mechanisms, in order to support the
development and acceptance of live digital forensic techniques and
evidence by researchers and practitioners. More specifically, the main
objective of this thesis is to extend existing research on the
evaluation of live forensics by:

* Classifying the purposes and methods behind the evaluation of live
  digital forensic evidence and acquisition mechanisms,
* Developing experimental methods for the evaluation of live digital
  forensic evidence and acquisition techniques,
* Implementing these methods in a framework that can be used by
  researchers and practitioners to conduct sound, repeatable live
  forensic experimentation, and
* Constructing a model and developing an appropriate set of metrics of
  the efficacy and forensic soundness of live digital forensic
  evidence acquisition mechanisms.

Where existing models are insufficient, based on the fluctuation of
the structural contents of memory over time (Savoldi & Gubian, 2009;
Walters & Petroni, 2007), or too abstract, defined in purely
mathematical terms (Vӧmel & Freiling, 2012), we are aiming to provide
a solid basis for the development of live digital forensics. Our work
will also codify a practical approach to constructing these models,
based on sound experimental methods.

## Installation

Pypette should work on any modern Linux environment (tested on Debian
Unstable and Fedora 19), and it also requires the following software
and libraries:

* Python (at least 2.7).
* The [Volatility Framework](http://www.volatilityfoundation.org) on
  your path.
* A recent version of the [QEMU](http://wiki.qemu.org/Main_Page)
  hypervisor.
* The [Libvirt](http://libvirt.org) virtualisation API and its Python
  bindings.

The supplied `setup.py` script uses the `distutils` library.

## Usage

This section provides a brief overview of how to use the
experimentation platform.

### Establishing the Experiment

All experiments with Pypette are conducted from virtual machine
snapshots, to allow for the repeated execution and statistically sound
evaluation of results. This snapshot should be configured to either
contain some representative example of the type of information under
consideration, or to reflect general computer configurations where a
live digital forensic tool is under evaluation.  The snapshot should
be created using Libvirt's GUI or command-line interface, and its
unique identifier can be discovered from the command-line.

### Configuration

The experiment definition encodes the parameters of an experimental
evaluation of live digital forensics. These parameters specify the
general procedure for an experiment and the specific combination of
live digital forensic technique and analysts required for the
evaluation. The experiment controller uses this definition to reify
live digital forensic technique and analyst implementations to conduct
a live digital forensic experiment. Our platform uses the same
experiment definition format for all live digital forensic techniques
and analysts, so that any technique and analyst implementation uses
the same configuration infrastructure and will not need to implement
its own. This separates the implementation of an experiment from its
definition, allowing users without programming experience, but with
some technical expertise, to conduct live digital forensic
experimentation.  An example experiment definition is included in the
distribution.

The structure of the definition document is relatively simple, with
all experiment definition documents describing:

* The name of the experiment,
* The number of executions for which it is to be repeated,
* The hierarchical name of the live digital forensic technique
  implementation,
* The set of key-value pairs that form the parameters of the
  technique,
* The list of hierarchical names and corresponding sets of key-value
  parameter pairs of the live digital forensic analyst
  implementations, and
* An optional set of key-value parameter pairs that act as default
  parameters for each analyst and technique in the experiment.

We merge the set of local parameters for a live digital forensic
technique or analyst with the global set of parameters in the
experiment. The implementation of this algorithm is left- biased, in
that in the event of a local and global parameter with the same name,
it always preserves the local parameter. An informal convention arose
in our concrete analyst and technique implementation, where all
parameter names include the hierarchical prefix of their associated
analyst or technique to avoid namespace clashes when defining
experiment-wide parameters. We impose no constraints on the values of
parameters except that they be well-formed YAML expressions, however,
the keys of parameters must always be strings.

### Launching Experiments

When the virtual machine and experiment definition have been written,
the experiment can be launched using the "pypette-launch.py" command
that is installed with the Pypette platform.

## Further Work

[ ] Integrate the analysis toolchain into the platform distribution.
[ ] Complete a general-purpose agent implementation in Golang.
[ ] Write better documentation.

## References

Lessing, M., & Solms, B. (2008, sep). Live Forensic Acquisition as
Alternative to Traditional Forensic Processes. Proceedings of the
Conference on IT Incident Management & IT Forensics (IMF 2008)
(pp. 1--9). Mannheim, Germany: IEEE.

Casey, E., & Stellatos, G. (2008, apr). The Impact of Full Disk
Encryption on Digital Forensics. ACM SIGOPS Operating Systems Review,
42(3), 93--98.

Mohanty, I., & Velusamy, R. (2012). Recovery of Live Evidence from
Internet Applications. Berlin, Germany: Springer.

Caloyannides, M. (2009, mar). Forensics Is So "Yesterday". IEEE
Security & Privacy Magazine, 7(2), 18--25.

Caloyannides, M., Memon, N., & Venema, W. (2009, mar). Digital
Forensics. IEEE Security & Privacy Magazine, 7(2), 16--17.

Beebe, N. (2009). Digital Forensic Research: The Good, the Bad and the
Unaddressed. Boston, MA, USA: Springer.

Erbacher, R. (2010, apr). Validation for Digital
Forensics. Proceedings of the Seventh International Conference on
Information Technology: New Generations (ITNG 2010)
(pp. 756--761). Las Vegas, Nevada, USA: IEEE.

Savoldi, A., & Gubian, P. (2009). Blurriness in Live Forensics: An
Introduction. Berlin, Germany: Springer.

Walters, A., & Petroni, N. (2007, feb). Volatools: Integrating
Volatile Memory Forensics into the Digital Investigation
Process. Proceedings of the 2007 BlackHat DC Conference, (pp. 1-
-18). Washington, DC, USA.

Vӧmel, S., & Freiling, F. (2012, jun). Correctness, Atomicity, and
Integrity: Defining Criteria for Forensically-Sound Memory
Acquisition. Digital Investigation, 9(2), 1--13.
