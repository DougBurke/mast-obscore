"""
Routines for dealing with MAST data in PSV format.
"""

import sys
import csv

# A dialect for pipe-separated values
class PSV(csv.Dialect):
    """Pipe-separated values (separator is |).

    At present all we really care about is the delimiter
    and lineterminator fields; the others are guesses.
    """
    
    delimiter = '|'
    doublequote = False
    escapechar = '\\'
    lineterminator = "\r\n"
    quotechar = None
    quoting = csv.QUOTE_NONE
    skipinitialspace = True # not sure about this one
    
csv.register_dialect("psv", PSV)

"""
From

head -1 obscore.csv | tr , '\n' | awk '{ printf "  \"%s\",\n", $1 }' -

"""

_colnames = [
  "s_ra",
  "s_dec",
  "datalen",
  "radecsys",
  "equinox",
  "timesys",
  "specsys",
  "vover",
  "vodate",
  "target_name",
  "ra_targ",
  "dec_targ",
  "title",
  "obs_creator_name",
  "obs_collection",
  "obs_publisher_did",
  "obs_id",
  "creation_date",
  "version",
  "instrument",
  "dssource",
  "em_domain",
  "der_snr",
  "spec_val",
  "spec_bw",
  "spec_fil",
  "em_res_power",
  "date_obs",
  "t_exptime",
  "t_min",
  "t_max",
  "aperture",
  "telescope_name",
  "tmid",
  "fluxavg",
  "fluxmax2",
  "em_min",
  "em_max",
  "min_flux",
  "max_flux",
  "min_error",
  "max_error",
  "access_format",
  "access_url",
  "representative",
  "preview",
  "project",
  "spectralaxisname",
  "fluxaxisname",
  "spectralsi",
  "fluxsi",
  "spectralunit",
  "fluxunit",
  "fluxucd",
  "fluxcal",
  "coord_obs",
  "coord_targ",
  "s_ra_min",
  "s_ra_max",
  "s_dec_min",
  "s_dec_max",
  "s_resolution",
  "t_resolution",
  "s_region",
  "o_fluxucd",
  "calib_level",
  "dataproduct_type",
  "t_span",
  "s_fov",
  "filesize",
  "access_estsize",
]

_ncols = len(_colnames)
_colmap = dict(zip(_colnames, range(0,_ncols)))

def check_row(row):
    """Ensure the number of columns is correct.

    We could also check other items but for now do not
    bother.
    """
    
    if len(row) != _ncols:
        raise ValueError("Row contains {0} columns, expected {1}!\n\n{2}\n".format(len(row), _ncols, row))

def get_column(row, cname):
    """Return the cell for the given column name from the row,
    which is expected to be the return value of a csv reader
    object.

    We assume that check_row() has already been called on this
    row.
    """

    try:
        return row[_colmap[cname]]

    except KeyError:
        raise ValueError("Invalid column name: {0}!".format(cname))

def row2dict(row):
    "Return a dictionary of key=column-name, value=column-value."

    check_row(row)
    return dict(zip(_colnames, row))

def get_reader(fname):
    """Return the CSV reader for the file and the file
    handle for the file. The file is opened read-only.

    """

    if fname == "-":
        fh = sys.stdin
    else:
        fh = open(fname, "r")
        
    rdr = csv.reader(fh, dialect="psv")
    return (rdr, fh)

