"""
Main - Arquivo Principal do Projeto
Mini Projeto: Twitter Plays Pokémon - Event-Driven Architecture
"""
import sys
import traceback

print("DEBUG: Iniciando imports...")

try:
    from game_controller import GameController
    print("DEBUG: GameController importado com sucesso")
except Exception as e:
    print(f"ERRO ao importar GameController: {e}")
    traceback.print_exc()
    sys.exit(1)


def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════╗
║   EVENT-DRIVEN PYBOY - TWITTER PLAYS POKEMON     ║
║   Arquitetura Orientada a Eventos               ║
╚══════════════════════════════════════════════════╝
    """)
    
    # Caminho da ROM
    rom_path = r"D:\Pokemon_ Red Version\Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb"
    
    controller = None
    
    try:
        print("DEBUG: Criando GameController...")
        # Inicializa controlador
        controller = GameController(rom_path)
        print("DEBUG: GameController criado")
        
        controller.start()
        print("DEBUG: Controller.start() executado")
        
        # Loop principal
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
        traceback.print_exc()
    finally:
        # SEMPRE executa o stop para gerar relatório final
        if controller is not None:
            try:
                controller.stop()
            except Exception as e:
                print(f"Erro ao parar controller: {e}")
        print("\n👋 Programa finalizado.")


if __name__ == "__main__":
    print("DEBUG: __main__ iniciado")
    try:
        main()
    except Exception as e:
        print(f"ERRO FATAL: {e}")
        traceback.print_exc()