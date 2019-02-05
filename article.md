# Distributing data with Intake

This article demonstrates to case studies of how data can be made available to
users with the conveniences provided by [Intake](https://intake.readthedocs.io/en/latest/).

This is part of a series of blog articles 
([announcement](https://www.anaconda.com/blog/developer-blog/intake-taking-the-pain-out-of-data-access/)),
[caching](https://www.anaconda.com/blog/developer-blog/intake-caching-data-on-first-read-makes-future-analysis-faster/), 
and [filename parsing](https://www.anaconda.com/blog/developer-blog/intake-parsing-data-from-filenames-and-paths/))
promoting the new Intake project. Read the documentation, join the
conversation on [github](https://github.com/ContinuumIO/intake) and try it out with
```bash
> conda install -c intake intake
```

**Summary**: There is a wealth of publicly-available data out there on the Web, in
both tabular and other formats. Intake provides a framework within which it's easy
to add data loading code and reference data resources, so that the code and data
can be distributed, and users can find and instantly access the data, 

## Introduction

There is a huge amount of data out there. Many data-sets are available publicly, for free.
However, these data span all sorts
- different domains of knowledge and use
- many types of data, not just tabular: arrays, text, nested/structured objects, and
  more; all in various formats
- scales of data from single files you can comfortably download in seconds, to large multi-file
  archives requiring cloud resources to process. 

It takes a large amount
of effort to find useful data-sets, and figure our the peculiarities of each one. Much
data are hidden within complex search web interfaces, without direct links, and yet others
are only accessible through custom APIs, which require time and effort to understand and use -
and may even require registration to acquire an API access key. In each case, the description
of what the data is and its intended use case is probably given, but, again, not in a uniform,
standard way.

Intake can help with this process.
 
## Case Study: MNIST digits data
 
The Modified National Institute of Standards and Technology 
([MNIST](http://yann.lecun.com/exdb/mnist/)) database of handwritten
digits is a very commonly referenced resource for demonstrating machine learning applied to
real-life images. It is a set of 28x28pix images, each with a handwritten digit (0-9) in
grey-scale, with 60,000 training samples, 10,000 testing samples and corresponding ground-truth
labels for each. Crucially, this is *not* tabular data, and no Pandas one-liner function can
read the files.
The data are, however, already available via multiple python libraries such as
[keras](https://www.tensorflow.org/api_docs/python/tf/keras/datasets/mnist/load_data); but the
point is, that we could have avoided repeatedly rewriting code to read this data for each library
that might use it, and return it to the user is a common format for analysis (in this case,
numpy arrays).

The idea to pursue this case study was born from the appearance of the 
[mnist](https://github.com/datapythonista/mnist/) library by 
[@datapythonista](https://github.com/datapythonista), python code that concerns itself with
downloading and parsing the unique format of the MNIST data files. Notice that much of this
code deals with reading remote data, decompressing it locally, and presenting a user API, and the 
[portion](https://github.com/datapythonista/mnist/blob/master/mnist/__init__.py#L64) that is
unique to the data format is just a small fraction of the total, in terms of lines of code. 

The Intake version of MNIST digits can be found 
[here](https://github.com/martindurant/mnist-data-intake). It contains the same
[parsing function](https://github.com/martindurant/mnist-data-intake/blob/master/intake_mnist/plugin.py#L73)
as before, and *very little* boiler-plate code to make that into an Intake driver. You can
install the package using `pip`, and reference the catalog file:
```
>>> import intake
>>> cat = intake.open_catalog('https://github.com/martindurant/mnist-data-intake/'
                             'raw/master/intake_mnist/cat.yaml')
>>> list(cat)
['mnist']
>>> cat.mnist.describe()
{'container': 'numpy',
 'description': 'MNIST digit images and labels.\n'
                'Select training or test datasets, which will be decompressed and cached\n'
                'locally. The labels and images are selectable as partitions, each is\n'
                'returned as an array.\n',
 'user_parameters': [{'allowed': ['train', 'test'],
   'default': 'train',
   'description': 'Data section to choose, [train|test]',
   'name': 'train_or_test',
   'type': 'str'}]}
```

We can see a few features that we get for free with Intake:
- specification of the output data type in a familiar container: numpy ndarrays
- automatic download and decompression of the data on first access
- descriptive text, which would allow us to search and find this dataset within a hierarchy of data-sets
- a user parameter to select between training or test datasets

Actually reading the data is trivial, following the instructions above. We find that the first number is, 
apparently, a 5.

```
>>> s = cat.mnist()  # gets trainign data by default
>>> arr = s.read_partition('images')
>>> import matplotlib.pyplot as plt
>>> plt.imshow(arr[0], cmap='gray'
>>> s.read_partition('labels')[0]
5
```
![Number 5](./5.png)

However, there is an even easier way to distribute the code and catalog reference: conda.
The repo contains a [simple recipe](https://github.com/martindurant/mnist-data-intake/tree/master/conda)
very like the examples provided with Intake itself. The architecture-independent package is
now easy to build, and as a user, all you need to do it
```bash
conda install -c intake intake-mnist-data
```
and now you get the same data-set available under `intake.cat.mnist` (which shows up
automatically in the data selector GUI), and the benefits of conda for managing versions
and updates.

## Case study: Philadelphia municipal data

Many government bodies routinely make available large amounts of interesting data which can
be analysed from a socio-economic and civic planning standpoint. For example, consider
the Chicago Data Portal's [Crimes database](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2).
A nice informative slide informs us what can be expected in the data, fields, etc, and
handy visualisation and query interfaces.  
Unfortunately, API query access requires registration and an API key (as well as a custom
query system). The full data is available as a CSV, but it's link is not readily discoverable
without clicking within the page, and the single [file](https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD),
turns out to be 1.5GB. That the server does not declate the file-size or allow bytes-range
requests is important, because it means that random access to load just some particular
chunk of the data is not possible. Nevertheless, this could be made into
an Intake catalog entry, with appropriate warnings over the file-size, and probably local
caching.

Turning to another municipality, Philadelphia does publish the API by which details of
data can be obtained, including the links to concrete data files. A 
[request](https://www.opendataphilly.org/api/3/action/package_list) yields a JSON response
with the names of all of the data packages listed, names like "airport-buildings". Further
requests can the find the resources associated with each package:

```
> https://www.opendataphilly.org/api/action/package_show?id=airport-buildings
{result: {
    id: "ccd6728d-7b92-4402-8d98-a67afd361450",
    metadata_created: "2015-05-29T15:33:24.328301",
    ..
    resources: [
        ..
            {format: "CSV",
            url: "http://data.phl.opendata.arcgis.com/datasets/1531a6999c0f40d3b1a6764a0a54f32b_0.csv",
            created: "2015-06-03T19:16:45.199061",
            }
        ]
    }
}
``` 
We find a number of metadata entries, and a set of resources, of which one is a URL to a CSV
file, with some file-specific metadata. 

To create an Intake catalog to this wealth of data, there are two concrete options: to make a 
"catalog"-type driver, like the [sql_cat](https://intake-sql.readthedocs.io/en/latest/api.html#intake_sql.SQLCatalog)
one, which can pull the list of entries and details for each on demand. That would, again, require
users to install code in order to make use of it. The second option is to use similar logic to
make a YAML catalog file by scanning through all of the data packages. The only disadvantage to the
second approach, is that the catalog is a fixed view of the database and would need to be
updated by rerunning the scanning code.

