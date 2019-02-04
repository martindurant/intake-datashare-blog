# Scientific data dissemination with Intake

He we discuss dissemination of data: the transformation of a high-profile data-set into
a form appropriate for big-data analysis.

The Gaia project released [Data Release 2](https://www.cosmos.esa.int/web/gaia/dr2) (DR2)
of 1.7 billion point source astronomical objects earlier this year. As a publicly funded
international scientific collaboration, the data is available for free on the project's
website: http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/

The contents of the linked directory contains 61234 gzip-compressed CSV files, each with
a typical size of 5-10MB each, to a total of about 550GB of data. There is, in addition,
a query interface, which is very useful for finding specific objects, or set of objects
meeting specific requirements (such as proximity to some point on the sky).

## Conversion

CSV files are ubiquitous, the most common file format for data in a tabular layout, and
very common even for pure array data. Parsing CSVs can be a pain, however, since
there is no absolute way to know the data types of each column *a priori*, leading to
possible parsing errors without further information. The encoding is not space-efficient,
and takes considerable CPU power to parse into a binary representation.
Much smaller file-sizes can be achieved by
compression, such as gzip in this case, which comes at the cost of CPU cycles after reading
bytes into memory, and the inability to access just a piece of some file. 

From a big-data processing point of view, the
very large number of small files is not great, since there is an overhead associated with starting
HTTP connections. Furthermore, CSV files do not allow for efficiently accessing just a limited number of
columns in the data - you have to scroll through every line of the file, even if you only parse
some of the columns of each. Finally, plain HTTP is not a great protocol for accessing files,
since it is typically not possible to find the file size, checksums, creation time etc., that
one would normally like as minimum information about a file.

An alternative version of the same data has been posted at 
`gcs://pangeo-data/gaia_dr2.parquet`. This version has 1750 files of about 300MB each, a total
of about 500GB. Clearly, the total is not much different (this data is also gzip compressed),
but now allows for efficient chunk-wise and column-wise access to the data and parallel
processing, with well-defined data types and encoding.

## Using the data

