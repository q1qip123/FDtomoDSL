class TomographyBuilder(object):
    def __init__(self):
        self.event_list = []
        self.station_list = []
        self.velocity_model = None
        self.event_builder = None
        self.velocity_model_builder = None
        return None
    
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
            
        
class EventBuilder(TomographyBuilder):    
    def __init__(self, tomography_builder):
        self.hypocenter_list = []
        self.observation_list = []
        self.hypocenter_builder = None
        self.observation_builder = None
        self.tomography_builder = tomography_builder
        
    def Event(self, event = None):  
        return self.tomography_builder.Event()
        
    def Hypocenter(self, hypocenter):
        if(hypocenter != None):
            self.hypocenter_list.append(hypocenter)
            return self
        
        self.hypocenter_builder = HypocenterBuilder(self)
        return self.hypocenter_builder
    
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
        
class VelocityModelBuilder(TomographyBuilder):
    def __init__(self, tomography_builder):
        self.reference_model = None
        self.coordinate = None
        self.coordinateBuilder = None
        self.tomography_builder = tomography_builder
        
    def ReferenceModel(self, reference_model):
        self.reference_model = reference_model
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
    
    def execute(self):        
        self.tomography_builder.execute()

class HypocenterBuilder(EventBuilder):
    def __init__(self, event_builder):
        self.hypocenter_list = []
        self.event_builder = None
        self.event_builder = event_builder
        
    def Location(self, location):
        self.location = location
        return self
    
    def Time(self, time):
        self.time = time
        
    def getValue(self):
        self.hypocenter_list.append([self.time, self.location])
        
    def execute(self):
        self.event_builder.execute()
    
class ObservationBuilder(EventBuilder):    
    def __init__(self, event_builder):
        self.observation_list = []
        self.time = None
        self.station = None
        self.event_builder = event_builder
        
    def Observation(self, observation = None):
        return self.event_builder.Observation()
    
    def Station(self, station):
        self.station = station
        return self
        
    def Time(self, time):
        self.time = time
        return self
        
    def getValue(self):
        self.observation_list.append([self.station, self.time])
        return self.observation_list
        
    def execute(self):
        self.event_builder.execute()

def CoordinateBuilder(VelocityModelBuilder):
    def __init__(self, velocity_model_builder):
        self.velocity_model_builder = velocity_model_builder
        self.cooridinate = []
        self.mesh = None
        self.origin = None
        self.space = None

    def Mesh(self, mesh):
        self.mesh = mesh
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
    
    def execute(self):
        self.velocity_model_builder.execute()

    
TomographyBuilder() \
    .Event('event') \
    .Station('station') \
    .VelocityModel() \
        .Coordinate('coordinate') \
        .ReferenceModel('reference_model') \
    .execute()