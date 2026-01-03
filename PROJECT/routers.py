class DayRouter:
    """
    Routes Day model to bot_db for read-only access.
    All other models go to default database.
    """

    route_app_labels = {"api"}
    bot_tables = ["day", "attendance", "botuser"]

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.bot_tables:
            return 'bot'  # read Day from bot database
        return None  # use default DB for other models

    def db_for_write(self, model, **hints):
        # Do not allow writes to Day in bot_db
        if model._meta.model_name in self.bot_tables:
            return None
        return None  # default DB for other models

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both models are in the same DB
        db_list = ("default", "bot")
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Prevent migrations on Day model in bot_db
        if model_name in self.bot_tables:
            return False
        # Allow other models in default DB
        if db == 'default':
            return True
        return None
