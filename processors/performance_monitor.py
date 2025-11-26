import time

class PerformanceMonitor:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.frame_count = 0
        self.start_time = time.time()
        self._register_events()
    
    def _register_events(self):
        self.event_bus.subscribe('frame_rendered', self.on_frame)
    
    def on_frame(self, data):
        self.frame_count += 1
        
        if self.frame_count % 3600 == 0:
            elapsed = time.time() - self.start_time
            fps = self.frame_count / elapsed
            print(f"📈 Performance: {fps:.2f} FPS médio ({self.frame_count} frames)")