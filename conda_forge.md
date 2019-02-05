# Intake released on Conda-Forge

Intake is a package for cataloging, finding and loading your data. It has been developed recently by
Anaconda, Inc., and continues to gain new features. To read  general information about
Intake and how to use it, please refer to the [documentation](https://intake.readthedocs.io/en/latest/).

Until recently, Intake was only available for installation via Conda and the `intake` channel
on `anaconda.org`. This reflected the rapid development and short release cycle of the project.
[Conda-Forge](https://conda-forge.org/) is an effort to provide an automated path for
releasing open-source projects to the public, in the context of the Conda package manager ecosystem.
From now on, Intake is available on Conda-Forge, and the recommended installation command is:

```bash
conda install -c conda-forge intake
```

### Preparations for release


In order to make Intake and its data drivers more widely available, we have first packaged and released
the project on PyPI for installation by pip. This is a general precursor step to release for Conda
on Conda-Forge, but it also allows a separate installation route directly with `pip`:

```bash
pip install intake
```

The above line is generally believed to work well, but this method of installation is not yet [as well
tested](https://github.com/ContinuumIO/intake/pull/252) as the Conda path.

Furthermore, we have explicitly added tests for Intake running under Windows. After fixing a number
of path-syntax-related bugs, we are confident that Intake should now work well for all Windows
users.

### Python 2 support?

Intake does not currently run under Python 2, and this has been a design choice in order to be able
to develop more quickly. As much of the python stack (numpy, pandas, etc.) is dropping Python 2 support,
it did not seem too important to put in the effort to add it to Intake, which is of course a new
project without the worries of backwards compatibility.

If it turns out that there is significant pressure to be able to support Python 2 also, then this decision
[may be reversed](https://github.com/ContinuumIO/intake/issues/228). 
There is not much in the codebase that is unfriendly to Python 2, it is purely a question
of developer time. However, some drivers depend on packages that are Python 3-only, and these will
never be back-ported.

### Release in Conda defaults

As of the time of writing, Intake is also being released on the Conda defaults channel (i.e., the
one that is automatically available to any Ana/Conda install). This is a seal of approval that
is much appreciated, and has the practical upshot that the following simpler installation command
will work, and also will likely happen much faster for not having to download the metadata of the 
Conda-Forge channel. The process of preparing packages for defaults is somewhat more involved, since
it requires that dependencies are also on defaults (otherwise there would be no point!).

To install from defaults:

```bash
conda install intake
```

### Status of drivers

Currently (early February, 2019), the following packages have been released on Conda-Forge:

- intake
- intake-elasticsearch ([PR](https://github.com/conda-forge/staged-recipes/pull/7676))
-  intake-accumulo
-  intake-astro
-  intake-avro
-  intake-parquet
-  intake-spark
-  intake-sql
- intake-xarray

and the following on defaults:

- intake

Please see the Intake [project dashboard](https://continuumio.github.io/intake-dashboard/status.html)
for details of releases of each package.
