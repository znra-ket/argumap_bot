from database import DebateRepository

class DebateService():
    def __init__(self, session):
        self.session = session
        self.repo = DebateRepository(session=session)

    def create_debate(self, user_id, name):
        if self.repo.get_by_name(name=name):
            return False
        return self.repo.create_debate(user_id=user_id, name=name) 

    def get_user_debates(self, user_id):
        return self.repo.get_by_user(user_id=user_id)
    
    def get_messages_by_debate(self, debate_id, user_id):
        debate = self.repo.get_by_id(debate_id=debate_id)

        if not debate:
            return False
        
        if debate.user_id != user_id:
            return False

        return self.repo.get_messages(debate_id=debate_id)
    
    def delete_debate(self, debate_id, user_id):
        debate = self.repo.get_by_id(debate_id=debate_id)

        if not debate:
            return False
        
        if debate.user_id != user_id:
            return False
        
        self.repo.delete(debate_id)
        return True
    
    def activate_debate(self, debate_id, user_id):
        debate = self.repo.get_by_id(debate_id)

        if not debate:
            return False
        
        if debate.user_id != user_id:
            return False
        
        self.repo.activate(debate_id)
        return True

    def deactivate_debate(self, debate_id, user_id):
        debate = self.repo.get_by_id(debate_id)

        if not debate:
            return False
        
        if debate.user_id != user_id:
            return False
        
        self.repo.deactivate(debate_id)
        return True

    def get_debate_by_name(self, name, user_id):
        debate = self.repo.get_by_name(name=name)
        
        if not debate:
            return False

        if debate.user_id != user_id:
            return False
        
        return debate
    
    def get_active_debate(self, user_id):
        return self.repo.get_active(user_id=user_id)