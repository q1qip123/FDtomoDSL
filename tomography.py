class TomographyBuilder(object):
    
    def __init__(self):
        self.event_list = []
        self.station_list = []
        self.event_builder = None
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

    
test = TomographyBuilder().Event('event1').Event('event2').execute()
test2 = TomographyBuilder().execute()