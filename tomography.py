class TomographyBuilder(object):
    def __init__(self):
        self.event_list = []
        self.station_list = []
        self.event_builder = None
        self.velocity_model_builder = None

    def Event(self, event = None):
        if(event != None):
            self.event_list.append(event)
            return self
                
        if (self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
            
        self.event_builder = EventBuilder(self)
        return self.event_builder
    
    def Station(self, station):
        self.station_list.append(station)
        return self
    
    def VelocityModel(self, velocity_model = None):
        if (velocity_model != None):
            self.velocity_model = velocity_model
            return self
        
        self.velocity_model_builder = VelocityModelBuilder(self)
        return self.velocity_model_builder
    
    def execute(self):
        if (self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
        
        if (self.velocity_model_builder != None):
            self.velocity_model = self.velocity_model_builder.getValue()
            
        result = []
        result.append(self.event_list)
        result.append(self.station_list)
        result.append(self.velocity_model)
        print(result)
            
        
class EventBuilder():    
    def __init__(self, tomography_builder):
        self.observation_list = []
        self.earthquake_builder = None
        self.observation_builder = None
        self.tomography_builder = tomography_builder
        
    def __getattr__(self, name):
        def _method_missing(*args, **kwargs):
            if(name == 'Event'):
                return self.tomography_builder.Event(args[0])
            elif(name == 'Station'):
                return self.tomography_builder.Station(args[0])
        return _method_missing
            
    def Earthquake(self, earthquake):
        if(earthquake != None):
            self.earthquake_list.append(earthquake)
            return self
        
        self.earthquake_builder = EarthquakeBuilder(self)
        return self.earthquake_builder
    
    def Observation(self, observation = None):
        if(observation != None):
            self.observation_list.append(observation)
            return self
        
        if (self.observation_builder != None):
            self.observation_list.append(self.observation_builder.getValue())
            
        self.observation_builder = ObservationBuilder(self)
        return self.observation_builder

    def getValue(self):
        self.hypocenter_list.append(self.observation_list)
        return self.hypocenter_list
    
    def execute(self):
        if (self.hypocenter_builder != None):
            self.hypocenter_list.append(self.hypocenter_builder.getValue())
        
        if (self.observation_builder != None):
            self.observation_list.append(self.observation_builder.getValue())
        
        self.tomography_builder.execute()
        
class VelocityModelBuilder():
    def __init__(self, tomography_builder):
        self.vp_model = None
        self.vs_model = None
        self.coordinate = None
        self.coordinateBuilder = None
        self.tomography_builder = tomography_builder
        
    def __getattr__(self, name):
        def _method_missing(*args, **kwargs):
            if(name == 'execute'):
                return self.tomography_builder.execute()

        return _method_missing
        
    def ReferenceModel(self, vp_model, vs_model):
        self.vp_model = vp_model
        self.vs_model = vs_model
        return self

    def Coordinate(self, coordinate = None):
        if (coordinate != None):
            self.coordinate = coordinate
            return self
        
        self.coordinateBuilder = CoordinateBuilder(self)
        return  self.coordinateBuilder
    
    def getValue(self):
        if (self.coordinateBuilder != None):
            self.coordinate = self.coordinateBuilder.getValue()
        
        return [self.coordinate, self.reference_model]

class EarthquakeBuilder():
    def __init__(self, event_builder):
        self.event_builder = event_builder
        self.location = None
        self.time = None
        
    def __getattr__(self, name):
        def _method_missing(*args, **kwargs):
            if(name == 'Station'):
                return self.event_builder.Station(args[0])
        return _method_missing
        
    def Location(self, location):
        self.location = location
        return self
    
    def Time(self, time):
        self.time = time

    def Earthquake(self, time):
        return NotImplemented
        
    def getValue(self):
        self.hypocenter_list.append([self.time, self.location])
    
class ObservationBuilder():    
    def __init__(self, event_builder):
        self.observation_list = []
        self.time = None
        self.station = None
        self.setting = None
        self.event_builder = event_builder
        
    def __getattr__(self, name):
        def _method_missing(*args, **kwargs):
            if(name == 'Observation'):
                return self.event_builder.Observation(args[0])
        return _method_missing
        
    def Observation(self, observation = None):
        return self.event_builder.Observation()
    
    def Station(self, station):
        self.station = station
        return self
        
    def Time(self, time):
        self.time = time
        return self
        
    def Setting(self, setting):
        self.setting = setting
        return self

    def getValue(self):
        self.observation_list.append([self.station, self.time])
        return self.observation_list


def CoordinateBuilder():
    def __init__(self, velocity_model_builder):
        self.velocity_model_builder = velocity_model_builder
        self.cooridinate = []
        self.coarse_mesh = None
        self.fine_mesh = None
        self.origin = None
        self.space = None

    def __getattr__(self, name):
        def _method_missing(*args, **kwargs):
            if(name == 'ReferenceModel'):
                return self.velocity_model_builder.ReferenceModel(args[0])
        return _method_missing    

    def Mesh(self, coarse_mesh, fine_mesh):
        self.coarse_mesh = coarse_mesh
        self.fine_mesh = fine_mesh
        return self
    
    def Origin(self, origin):
        self.origin = origin
        return self
    
    def Space(self, space):
        self.space = space
        return self

    def getValue(self):
        self.cooridinate.append([self.mesh, self.origin, self.space])
        return self.cooridinate


    
