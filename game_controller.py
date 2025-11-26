from pyboy import PyBoy
from event_bus import EventBus
from processors import (
    GameStatsProcessor,
    ReportGenerator,
    AchievementProcessor,
    ActionLogger,
    PerformanceMonitor
)

class GameController:
    def __init__(self, rom_path: str):
        self.event_bus = EventBus()
        self.pyboy = None
        self.rom_path = rom_path
        self.running = False
        
        self.stats_processor = GameStatsProcessor(self.event_bus)
        self.report_generator = ReportGenerator(self.event_bus, self.stats_processor)
        self.achievement_processor = AchievementProcessor(self.event_bus, self.stats_processor)
        self.action_logger = ActionLogger(self.event_bus)
        self.performance_monitor = PerformanceMonitor(self.event_bus)
        
        self.last_position = None
        self.frame_counter = 0
        self.last_hp = None
        self.last_menu_state = None
        self.last_joypad_state = 0
        self.report_interval = 3600
    
    def start(self):
        print("\n🎮 Iniciando PyBoy Event-Driven System...")
        print("="*50)
        try:
            self.pyboy = PyBoy(self.rom_path, window="SDL2")
            self.running = True
            print("✓ Emulador iniciado com sucesso!")
            print(f"✓ ROM carregada: {self.rom_path}")
            print("\nControles (Padrão do PyBoy):")
            print("  Setas ↑↓←→ - Direcionais")
            print("  A - Botão A")
            print("  S - Botão B")
            print("  Enter - Start")
            print("  Backspace - Select")
            print("  ESC ou fechar janela - Sair")
            print("="*50 + "\n")
        except Exception as e:
            print(f"❌ Erro ao iniciar emulador: {e}")
            raise
    
    def detect_movement(self):
        try:
            current_x = self.pyboy.memory[0xD362]
            current_y = self.pyboy.memory[0xD361]
            current_position = (current_x, current_y)
            
            if self.last_position is not None:
                if current_position != self.last_position:
                    self.event_bus.publish('step_taken', current_position)
            
            self.last_position = current_position
        except Exception as e:
            if self.frame_counter % 600 == 0:
                print(f"⚠️  Erro ao detectar movimento: {e}")
    
    def detect_battle(self):
        try:
            battle_type = self.pyboy.memory[0xD057]
            in_battle = self.pyboy.memory[0xD05A]
            
            if (battle_type > 0 or in_battle > 0) and self.last_hp is None:
                self.event_bus.publish('battle_started', f"type_{battle_type}")
                self.last_hp = True
            elif battle_type == 0 and in_battle == 0:
                self.last_hp = None
                
        except Exception as e:
            if self.frame_counter % 600 == 0:
                print(f"⚠️  Erro ao detectar batalha: {e}")
    
    def detect_button_press(self):
        try:
            joypad_state = self.pyboy.memory[0xFF00]
            
            if joypad_state != self.last_joypad_state:
                self.event_bus.publish('button_pressed', 'joypad')
                self.last_joypad_state = joypad_state
        except:
            pass
    
    def detect_menu(self):
        try:
            menu_state = self.pyboy.memory[0xCF13] if hasattr(self.pyboy, 'memory') else 0
            
            if menu_state > 0 and self.last_menu_state == 0:
                self.event_bus.publish('menu_opened', 'menu_detected')
            
            self.last_menu_state = menu_state
        except:
            pass
    
    def process_frame(self):
        if not self.running:
            return False
        
        self.pyboy.tick()
        self.frame_counter += 1
        
        self.detect_movement()
        self.detect_battle()
        self.detect_button_press()
        self.detect_menu()
        
        if self.frame_counter % 60 == 0:
            self.event_bus.publish('frame_rendered', self.frame_counter)
            self.event_bus.publish('button_pressed', 'frame_tick')
        
        if self.frame_counter % self.report_interval == 0:
            self.event_bus.publish('generate_report', None)
        
        return self.running
    
    def stop(self):
        print("\n🛑 Encerrando sessão...")
        self.running = False
        self.event_bus.publish('game_ended', None)
        
        if self.pyboy:
            self.pyboy.stop()
        
        print("✓ Sessão encerrada com sucesso!")