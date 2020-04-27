class TomographyBuilder(object):
    event_list = []
    station_list = []
    event_builder = None
    
    def __init__(self):
        return None
    
    def Event(self, event = None):
        self.event_builder = EventBuilder(self)
        return self.event_builder(event)
    
    def Station(self, station):
        self.station_list.append(station)
        return self
    
    def execute(self):
        if (self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
        print(self.event_list)
        
        
        
class EventBuilder(TomographyBuilder):
    event_list = []
    hypocenter_list = []
    observation_list = []
    hypocenter_builder = None
    event_builder = None
    tomography_builder = None
    
    def __init__(self, tomography_builder):
        self.tomography_builder = tomography_builder
        
    def Event(self, event = None):
        if(event != None):
            self.event_list.append(event)
            return self.tomography_builder
        
        if (self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
        
        self.event_builder = EventBuilder(self.tomography_builder)
        return self.event_builder
        
    def Hypocenter(self, hypocenter):
        self.hypocenter_builder = HypocenterBuilder(self)
        return self.hypocenter_builder
    
    def Observation(self, observation):
        self.observation_list.append(observation)
        return self

    def getValue(self):
        if(self.event_builder != None):
            self.event_list.append(self.event_builder.getValue())
        self.hypocenter_list.append(self.observation_list)
        self.event_list.append(self.hypocenter_list)
        return self.hypocenter_list
    
    def execute(self):
        self.tomography_builder.execute()
    
class HypocenterBuilder(EventBuilder):
    hypocenter_list = []

    def __init__(self, EventBuilder):
        self.EventBuilder = EventBuilder
        
    def Location(self, location):
        self.location = location
        return self
    
    def Time(self, time):
        self.time = time
        
    def getValue(self):
        self.hypocenter_list.append([self.time, self.location])
    
    
    
    
    
test = TomographyBuilder() \
                            .Event('event') \
                            .execute()
