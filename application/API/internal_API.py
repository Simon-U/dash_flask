import json
import os
from application.models import User, db, co2model


class get_co2model:
    def get_model_names():
        """_summary_
        This function provides a list of modles registered in the database
        Returns:
            List: List of models in the co2model in the database
        """
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
        """_summary_
        Function to get the path to the excel data file
        Args:
            model (string): model for which the path to the datafile is needed

        Returns:
            string: returns the string to the data
        """

        return os.path.join(
            os.getcwd(),
            "application/data",
            co2model.query.with_entities(co2model.path_datafile)
            .filter_by(name=model)
            .first()[0]
            .strip(),
        )

    def get_processing_file(model):
        """_summary_
        Function to get the path to the python processing file
        Args:
            model (string): model for which the path to the datafile is needed

        Returns:
           string: returns the string to the data
        """
        return os.path.join(
            os.getcwd(),
            "application/data/processing",
            co2model.query.with_entities(co2model.path_processingfile)
            .filter_by(name=model)
            .first()[0]
            .strip(),
        )


class get_user:
    def check_password(user_id, password):
        user = User.query.filter_by(id=user_id).first()
        return user.check_password(password=password)

    def change_password(user_id, newpassword):
        user = User.query.filter_by(id=user_id).first()
        user.set_password(newpassword)
        db.session.commit()
        return "changed"
