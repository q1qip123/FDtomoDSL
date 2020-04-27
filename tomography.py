class TomographyBuilder(object):
    event_list = []
    station_list = []
    event_builder = None
    
    def __init__(self):
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
    
    def execute(self):
        if (self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
        print(self.event_list)
        
        
        
class EventBuilder(TomographyBuilder):
    hypocenter_list = []
    observation_list = []
    hypocenter_builder = None
    observation_builder = None
    tomography_builder = None
    
    def __init__(self, tomography_builder):
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
    
class HypocenterBuilder(EventBuilder):
    hypocenter_list = []
    event_builder = None

    def __init__(self, event_builder):
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
    observation_list = []
    time = None
    station = None
    event_builder = None
    
    def __init__(self, event_builder):
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
        self.hypocenter_list.append([self.station, self.time])
        return self.hypocenter_list
        
    def execute(self):
        self.event_builder.execute()

    
test = TomographyBuilder().Event().Hypocenter("hypo")\
                                    .Observation('obs1').Observation().Station('sta').Time('time') \
                                    .execute()
