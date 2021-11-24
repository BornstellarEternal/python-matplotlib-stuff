"""
@brief
            Simple example on how to work with numpy structured data as well as convert it to
            unstructured data (aka numpy arrays). There's also examples on how to setup plots

@tools
            Matplotlib v3.4.3       https://matplotlib.org/
            Numpy v1.21             https://numpy.org/1.21/
            Python v3.8.10          https://docs.python.org/3.8/
"""


#---------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt 
import matplotlib.cm as cm 

import numpy as np 
from numpy.lib import recfunctions as rfn 

import argparse 
from enum import Enum, EnumMeta, unique


#---------------------------------------------------------------------------------------------------
@unique
class Fields(Enum):
    """
    Enumerations for columns in csv header
    """
    ABS = 'abs'
    REL = 'rel'
    DEL = 'del'
    TAG = 'tag'
@unique
class Tags(Enum):
    """
    Enumerations for types of tags
    """
    PFOO = '\"++foo\"'
    NFOO = '\"--foo\"'
    PBAR = '\"++bar\"'
    NBAR = '\"--bar\"'


#---------------------------------------------------------------------------------------------------
class Data:
    """
    __init__                        -   Initialize, by reading in the data
    __str__                         -   Override to print our object nicely
    filter_sdata_by_col             -   Filter columns based on their field name
    filter_sdata_by_tag             -   Filter tag column on a particular value or values
    """
    def __init__(self, filename):

        self.filename = filename
        
        #   Specify the datatype for each field
        datatypes = [
            (Fields.ABS.value, 'i8'),
            (Fields.REL.value, 'i8'),
            (Fields.DEL.value, 'i8'),
            (Fields.TAG.value, '<U25')  
        ]

        #   Read in csv as structured data
        self.sdata = np.genfromtxt(
            self.filename,
            dtype=datatypes,
            delimiter=',',
            skip_header=1   # if you don't skip header, you get weird plots
        )

        #   Convert to unstructured (numpy array)
        self.udata = rfn.structured_to_unstructured(
                self.sdata[[Fields.ABS.value, Fields.REL.value, Fields.DEL.value]])

    def __str__(self):
        return "Structured Data:\n{}\n\nUnstructured Data:\n{}\n\n".format(self.sdata, self.udata)

    def filter_sdata_by_col(self, names):
        return self.sdata[names]
    
    def filter_sdata_by_tag(self, values):
        return self.sdata[np.in1d(self.sdata[Fields.TAG.value], values)]


#---------------------------------------------------------------------------------------------------
def plot_line(ax, data_x, data_y, param_dict={}):
    out = ax.plot(data_x, data_y, **param_dict)
    return out

def plot_scatter(ax, data_x, data_y, param_dict={}):
    out = ax.scatter(x=data_x, y=data_y, **param_dict)
    return out

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A simple matplotlib example")
    parser.add_argument("--file", help="csv file to load", type=str, required=True)
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    # setup our data object by passing in filename, filename is required to run this program
    DataObject = Data(args.file)
    print(DataObject)

    # examples on how we can apply certain filters on structured data
    print("apply filter by column:\n{}\n\n".format(
        DataObject.filter_sdata_by_col([Fields.ABS.value])))
    print("apply filter by tag:\n{}\n\n".format(
        DataObject.filter_sdata_by_tag([Tags.PFOO.value, Tags.NFOO.value])))
    
    # examples of setting up plots
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(8,4))
    
    ax1.set_title("A line plot")
    ax1.grid(True)
    plot_line(ax1, DataObject.udata[:,0], DataObject.udata[:,1], {'c': 'g', 'marker':'o'})
    plot_line(ax1, DataObject.udata[:,0], DataObject.udata[:,2], {'c': 'b', 'marker':'.'})

    ax2.set_title("A scatter plot")
    ax2.grid(True)
    plot_scatter(
        ax2, 
        DataObject.udata[:,0], 
        DataObject.udata[:,1], 
        {'c': DataObject.udata[:,0], 'cmap': 'RdYlGn_r', 'marker': '2'})
    plot_scatter(
        ax2,
        DataObject.udata[:,0],
        DataObject.udata[:,2],
        {'c': DataObject.udata[:,0], 'cmap': 'plasma', 'marker': '1'})
    
    plt.show()


# We might want to just import this file later
if __name__ == "__main__":
    print("\n")
    main()