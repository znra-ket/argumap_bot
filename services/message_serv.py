from database import MessageRepository

class MessageService():
    def __init__(self, session):
        self.session = session
        self.repo = MessageRepository(session=session)

    def create_message(self, debate_id, user_id, text, state, username):
        return self.repo.create_message(
            debate_id=debate_id,
            user_id=user_id,
            text=text,
            state=state,
            from_username=username
        )
    def get_arguments(self, debate_id):
        return self.repo.get_arguments(debate_id=debate_id)
    
    def get_theses(self, debate_id):
        return self.repo.get_theses(debate_id=debate_id) 
    
    def get_messages(self, debate_id): 
        return self.repo.get_all_messages(debate_id=debate_id)