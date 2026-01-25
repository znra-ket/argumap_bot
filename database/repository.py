from .models import Base, Debate, Message
from .session import close_db

class DebateRepository():
    def __init__(self, session):
        self.session = session

    def create_debate(self, user_id, name):
        try:
            debate = Debate(
                user_id=user_id,
                name=name
            )
            self.session.add(debate)
            self.session.commit()
            self.session.refresh(debate)
            return debate
        except:
            self.session.rollback()
            return False
    
    def get_by_id(self, debate_id):
        return self.session.query(Debate).filter_by(debate_id=debate_id).first()

    def get_by_name(self, name):
        return self.session.query(Debate).filter_by(name=name).first()
    
    def get_by_user(self, user_id):
        return self.session.query(Debate).filter_by(user_id=user_id).all()
    
    def sort_by_time(self, messages: list):
        return sorted(messages, lambda m: m.addet_at)
    
    def get_messages(self, debate_id):
        debate = self.get_by_id(debate_id)

        if debate:
            return self.sort_by_time(debate.messages)
        return []

    def delete(self, debate_id):
        debate = self.get_by_id(debate_id)

        self.session.delete(debate)
        self.session.commit()

    def activate(self, debate_id):
        debate = self.get_by_id(debate_id=debate_id)

        debate.is_active = True
        self.session.commit()

    def deactivate(self, debate_id):
        debate = self.get_by_id(debate_id=debate_id)

        debate.is_active = False
        self.session.commit()

    def get_active(self, user_id):
        return self.session.query(Debate).filter_by(user_id=user_id, is_active=True).first()

class MessageRepository():
    def __init__(self, session):
        self.session = session

    def create_message(self, debate_id, user_id, text, state,from_username):
        try:
            message = Message(
                debate_id=debate_id,
                user_id=user_id,
                text=text,
                state=state,
                from_username=from_username
            )
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
            return message
        except:
            return False

    def get_arguments(self, debate_id):
        return self.session.query(Message).filter_by(debate_id=debate_id, state="Аргумент").all()
    
    def get_theses(self, debate_id):
        return self.session.query(Message).filter_by(debate_id=debate_id, state="Тезис").all()
    
    def get_all_messages(self, debate_id):
        return self.session.query(Message).filter_by(debate_id=debate_id).all()