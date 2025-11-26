class AchievementProcessor:
    def __init__(self, event_bus, stats_processor):
        self.event_bus = event_bus
        self.stats_processor = stats_processor
        self.achievements = []
        self._register_events()
    
    def _register_events(self):
        self.event_bus.subscribe('step_taken', self.check_step_achievements)
        self.event_bus.subscribe('battle_started', self.check_battle_achievements)
    
    def check_step_achievements(self, data):
        steps = self.stats_processor.stats['steps']
        
        milestones = [100, 500, 1000, 5000]
        for milestone in milestones:
            if steps == milestone:
                achievement = f"🏆 Conquista desbloqueada: {milestone} passos!"
                self.achievements.append(achievement)
                print(achievement)
    
    def check_battle_achievements(self, data):
        battles = self.stats_processor.stats['battles']
        
        milestones = [10, 25, 50, 100]
        for milestone in milestones:
            if battles == milestone:
                achievement = f"🏆 Conquista desbloqueada: {milestone} batalhas!"
                self.achievements.append(achievement)
                print(achievement)