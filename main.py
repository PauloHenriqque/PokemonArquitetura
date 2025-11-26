from game_controller import GameController

def main():
    print("""
╔══════════════════════════════════════════════════╗
║   EVENT-DRIVEN PYBOY - TWITTER PLAYS POKEMON      ║
║   Arquitetura Orientada a Eventos                ║
╚══════════════════════════════════════════════════╝
    """)
    
    rom_path = r"D:\Pokemon_ Red Version\Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb"
    
    controller = None
    
    try:
        controller = GameController(rom_path)
        controller.start()
        
        print("🎮 Jogo iniciado! Jogue normalmente.\n")
        print("💡 Dica: Feche a janela do emulador ou pressione Ctrl+C para encerrar.\n")
        
        while controller.running:
            try:
                if not controller.process_frame():
                    break
            except KeyboardInterrupt:
                print("\n\n⏸️  Ctrl+C pressionado - Encerrando sessão...")
                controller.running = False
                break
                
    except KeyboardInterrupt:
        print("\n\n⏸️  Ctrl+C pressionado - Encerrando sessão...")
        if controller:
            controller.running = False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if controller is not None:
            try:
                controller.stop()
            except:
                pass