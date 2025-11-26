from datetime import datetime

class ReportGenerator:
    def __init__(self, event_bus, stats_processor):
        self.event_bus = event_bus
        self.stats_processor = stats_processor
        self.reports_generated = 0
        self._register_events()
    
    def _register_events(self):
        self.event_bus.subscribe('generate_report', self.generate_report)
        self.event_bus.subscribe('game_ended', self.generate_final_report)
    
    def generate_report(self, data):
        self.reports_generated += 1
        stats = self.stats_processor.get_stats()
        
        print("\n" + "="*50)
        print(f"📊 RELATÓRIO INTERMEDIÁRIO #{self.reports_generated}")
        print("="*50)
        print(f"Batalhas: {stats['battles']}")
        print(f"Passos: {stats['steps']}")
        print(f"Menus abertos: {stats['menu_opens']}")
        print(f"Botões pressionados: {stats['buttons_pressed']}")
        print("="*50 + "\n")
    
    def generate_final_report(self, data):
        stats = self.stats_processor.get_stats()
        duration = datetime.now() - stats['start_time']
        
        print("\n" + "="*50)
        print("🏁 RELATÓRIO FINAL - SESSÃO ENCERRADA")
        print("="*50)
        print(f"Tempo de jogo: {duration}")
        print(f"Total de batalhas: {stats['battles']}")
        print(f"Total de passos: {stats['steps']}")
        print(f"Total de menus abertos: {stats['menu_opens']}")
        print(f"Total de botões pressionados: {stats['buttons_pressed']}")
        
        if duration.total_seconds() > 0:
            print(f"\nMédia de ações por minuto: {stats['buttons_pressed'] / (duration.total_seconds() / 60):.2f}")
        
        print("="*50 + "\n")