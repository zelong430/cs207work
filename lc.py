
import itertools
from collections import defaultdict
import os
import reprlib

def lc_reader(filename):
    lclist=[]
    dict_of_facets = {}
    temp_label = []
    temp_value = []
    with open(filename) as fp:
        i = 0
        for line in fp:
            i += 1
            if line.find('#')==0:
                temp = line[1:].strip().split()
                if i == 1:
                    temp_label = temp
                elif i == 2:
                    temp_value = temp
                #print (temp)
                dict_of_facets = dict(zip(temp_label, temp_value)) 
            else:
                lclist.append([float(f) for f in line.strip().split()])
    return lclist, dict_of_facets

class LightCurve:
    
    def __init__(self, data, metadict):
        self._time = [x[0] for x in data]
        self._amplitude = [x[1] for x in data]
        self._error = [x[2] for x in data]
        self._timeseries = zip(self._time, self._amplitude)
        self.metadata = metadict
        self.filename = None
    
    @classmethod
    def from_file(cls, filename):
        lclist, metadict = lc_reader(filename)
        instance = cls(lclist, metadict)
        instance.filename = filename
        return instance
    
    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self.timeseries,0,10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)        
    #your code here    
    @property
    def time(self):
        return self._time
    @property
    def amplitude(self):
        return self._amplitude
    @property
    def timeseries(self):
        return self._timeseries
    
    def __len__(self):
        return len(self._time)
    def __getitem__(self,position):
        return (self._time[position], self._amplitude[position])

class LightCurveDB:
    
    def __init__(self):
        self._collection={}
        self._field_index=defaultdict(list)
        self._tile_index=defaultdict(list)
        self._color_index=defaultdict(list)
    
    def populate(self, folder):
        for root,dirs,files in os.walk(folder): # DEPTH 1 ONLY
            for file in files:
                if file.find('.mjd')!=-1:
                    the_path = root+"/"+file
                    self._collection[file] = LightCurve.from_file(the_path)
    
    def index(self):
        for f in self._collection:
            lc, tilestring, seq, color, _ = f.split('.')
            field = int(lc.split('_')[-1])
            tile = int(tilestring)
            self._field_index[field].append(self._collection[f])
            self._tile_index[tile].append(self._collection[f])
            self._color_index[color].append(self._collection[f])
     
    #your code here
    def retrieve(self, facet, value):
        for var in vars(self):
            if facet in var:
                return (vars(self)[var][value])


