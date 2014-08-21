"""
Distribution script for the live digital forensic experimentation platform.
"""

from distutils.core import setup

setup(
    
    # Package metadata.
    name="Pypette",
    version="1.0",
    description="Live digital forensic experimentation platform",
    author="Brett Lempereur",
    author_email="b.lempereur@ljmu.ac.uk",

    # Package components.
    packages=[
        "pypette",
        "pypette.analyst",
        "pypette.analyst.volatile",
        "pypette.collate",
        "pypette.collate.model",
        "pypette.technique",
        "pypette.technique.behaviour"
    ],

    # Executable scripts.
    scripts = [
        "bin/pypette-launch.py"
    ],

    # Provides.
    provides = [
        "pypette (1.0)"
    ],

    # Requirements.
    requires = [
        "libvirt (>=1.0.5)",
        "libvirt_qemu (>=1.0.5)"
    ]

)

