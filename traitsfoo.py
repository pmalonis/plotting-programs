
import h5py
import traits.api
from traits.api import Str, Array, Int, Float, Bool
import traitsui.api
import numpy

known_file_attributes = {
    'arf_version': Str,
    'program': Str,
    'sampling_rate': Int}


known_entry_attributes = {
    'name': Str,
    'recuri': Str,
    'timestamp': lambda x: Array(x.dtype, x.shape, x),
    'site': Int,
    'pen': Int,
    'recid': Int,
    'TITLE': Str,
    'max_length': Float,
    'exclude_mspikes': Bool,
    'experimenter': Str,
    'animal': Str}


class ArfFile(traits.api.HasTraits):
    sampling_rate = traits.api.Float
    filename = traits.api.Str


class ArfGroup(traits.api.HasTraits):
    name = traits.api.Str
    recuri = traits.api.Str
#    timestamp =
    site = traits.api.Int
    pen = traits.api.Int
    recid = traits.api.Int
    title = traits.api.Str
    max_length = traits.api.Float
    exclude_mspikes = traits.api.Bool
    experimenter = traits.api.Str
    animal = traits.api.Str


class ArfGroup2(traits.api.HasTraits):
    def __init__(self, group):
        super(ArfGroup2, self).__init__()
        for k, v in a.attrs.items():
            if k in known_entry_attributes:
                self.add_class_trait(k, known_entry_attributes[k](v))
            elif '.' not in k:
                self.add_class_trait(k, traits.api.Str(v))
'''
            if type(v) == numpy.ndarray:
                self.add_class_trait(k, traits.api.Trait(v[0]))
            elif '.' not in k:
                self.add_class_trait(k, traits.api.Str(v))
'''

f = h5py.File('120820_yy7134_0_0.arf')
a = f.values()[0]
sam = ArfGroup2(a)
sam.configure_traits()




















