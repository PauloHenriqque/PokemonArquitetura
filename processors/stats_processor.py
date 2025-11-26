from datetime import datetime

class GameStatsProcessor:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.stats = {
            'battles': 0,
            'steps': 0,
            'menu_opens': 0,
            'buttons_pressed': 0,
            'start_time': datetime.now()
        }
        self._register_events()
    
    def _register_events(self):
        self.event_bus.subscribe('battle_started', self.on_battle)
        self.event_bus.subscribe('step_taken', self.on_step)
        self.event_bus.subscribe('menu_opened', self.on_menu)
        self.event_bus.subscribe('button_pressed', self.on_button)
    
    def on_battle(self, data):
        self.stats['battles'] += 1
        print(f"⚔️  Batalha #{self.stats['battles']} detectada!")
    
    def on_step(self, data):
        self.stats['steps'] += 1
        if self.stats['steps'] % 10 == 0:
            print(f"👟 {self.stats['steps']} passos dados")
    
    def on_menu(self, data):
        self.stats['menu_opens'] += 1
        print(f"📋 Menu aberto ({self.stats['menu_opens']}x)")
    
    def on_button(self, data):
        self.stats['buttons_pressed'] += 1
    
    def get_stats(self):
        return self.stats.copy()