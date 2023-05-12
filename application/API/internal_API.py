from flask import current_app, session
from application.models import User, db, co2model
import json


class get_co2model:
    def get_model_names():
        names = [
            model[0].strip()
            for model in co2model.query.with_entities(co2model.name).all()
        ]
        if len(names) == 0:
            return ["nothing defined"]
        return [
            model[0].strip()
            for model in co2model.query.with_entities(co2model.name).all()
        ]

    def get_data_file(model):
        return (
            co2model.query.with_entities(co2model.path_datafile)
            .filter_by(name=model)
            .first()[0]
            .strip()
        )

    def get_processing_file(model):
        return (
            co2model.query.with_entities(co2model.path_processingfile)
            .filter_by(name=model)
            .first()[0]
            .strip()
        )


class get_user:
    def get_user_preferences(user_id, model):
        return {
            key: int(value)
            for key, value in json.loads(
                User.query.filter_by(id=user_id).first().preferences
            )
            .get(model)
            .items()
        }

    def check_password(user_id, password):
        user = User.query.filter_by(id=user_id).first()
        return user.check_password(password=password)

    def change_password(user_id, newpassword):
        user = User.query.filter_by(id=user_id).first()
        user.set_password(newpassword)
        db.session.commit()
        return "changed"

    def save_user_preferences(user_id, model, weights):
        user = User.query.filter_by(id=user_id).first()
        dict_pref = json.loads(user.preferences)

        dict_pref[model] = weights
        user.preferences = json.dumps(dict_pref)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
        return "chaged"
