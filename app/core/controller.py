import logging

from sqlalchemy.orm import Session
from app.core.database import engine


class BaseController(object):
    """ Base View to create helpers common to all Webservices.
    """

    def __init__(self, db: Session = None):
        """Constructor
        """
        self.close_session = None
        if db:
            self.db = db
        else:
            self.db = Session(engine)
            self.close_session = True

        self.model_class = None

    def read(
            self,
            offset: int = 0,
            limit: int = 100,
            sort_by: str = 'id',
            order_by: str = 'desc',
            qtype: str = 'first',
            params: dict = {},
            **kwargs):
        """Get a record from the database.
        """
        columns = dict()
        for param in self.model_class.__mapper__.attrs.keys():
            if kwargs.get(param) is not None:
                columns[param] = params.get(param)

        try:
            query_model = self.db.query(self.model_class)
            for column in columns:
                item_param = None if columns.get(column) == 'null' else columns.get(column)
                query_model = query_model.filter(
                    getattr(self.model_class, column) == item_param)

            sort_by = getattr(self.model_class, sort_by)

            return getattr(query_model.order_by(
                getattr(sort_by, order_by)()).offset(offset).limit(limit), qtype)()

        except Exception as error:
            logging.error(error)

        finally:
            if self.close_session:
                self.db.close()

    def create(self, data: dict):
        """Create a record in the database.
        """
        db_data = self.model_class(**data)
        try:
            self.db.add(db_data)
            self.db.commit()
            self.db.refresh(db_data)
            return db_data

        except Exception as error:
            logging.error(error)
            return None

        finally:
            if self.close_session:
                self.db.close()

    def update(
            self,
            data: dict,
            model_id: int = None,
            params: dict = list()):
        """Edit a record in the database.
        """
        try:
            query_model = self.db.query(self.model_class)
            if model_id:
                query_model = query_model.filter(
                    self.model_class.id == model_id
                )

            if params:
                for item in params:
                    if params.get(item) is not None:
                        query_model = query_model.filter(
                            getattr(self.model_class, item) == params.get(item)
                        )

            query_model = query_model.one_or_none()

            if query_model:
                for item in data:
                    if data.get(item) is not None:
                        setattr(query_model, item, data[item])

                self.db.merge(query_model)
                self.db.commit()
                self.db.refresh(query_model)

                return query_model

        except Exception as error:
            logging.error(error)
            return None

        finally:
            if self.close_session:
                self.db.close()
