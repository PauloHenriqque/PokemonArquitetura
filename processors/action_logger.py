from datetime import datetime

class ActionLogger:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.log = []
        self._register_events()
    
    def _register_events(self):
        self.event_bus.subscribe('battle_started', self.log_battle)
        self.event_bus.subscribe('menu_opened', self.log_menu)
    
    def log_battle(self, data):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Batalha iniciada"
        self.log.append(log_entry)
    
    def log_menu(self, data):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Menu aberto"
        self.log.append(log_entry)