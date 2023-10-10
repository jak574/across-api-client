from urllib.parse import urlencode
import requests
from .constants import API_URL
from .functions import tablefy
from marshmallow import Schema
from .jobstatus import JobStatus

SchemaType = type(Schema)


class ACROSSBase:
    # Type hints
    entries: list
    status: JobStatus

    # API descriptors
    _schema: Schema
    _arg_schema: Schema
    _mission: str
    _api_name: str = __name__

    def __getitem__(self, i):
        return self.entries[i]

    @property
    def get_url(self) -> str:
        api_url = f"{API_URL}{self._mission}/{self._api_name}?"
        api_params = urlencode(self.arguments)
        return api_url + api_params

    @property
    def allowed_args(self) -> list:
        return list(self._arg_schema.fields.keys())

    @property
    def arguments(self) -> dict:
        keys = [key for key in self.allowed_args if key in self.__dict__.keys()]
        return {key: self._arg_schema.dump(self)[key] for key in keys}

    @property
    def parameters(self) -> dict:
        return {key: getattr(self, key) for key in self._schema.fields.keys()}

    @parameters.setter
    def parameters(self, params: dict):
        for key in self._schema.fields.keys():
            if key in params.keys():
                setattr(self, key, params[key])

    def get(self) -> bool:
        if self.validate():
            req = requests.get(self.get_url)
            if req.status_code == 200:
                self.parameters = self._schema.loads(req.text).parameters
                return True
            else:
                raise Exception(f"Query failed with HTML code {req.status_code}")
        return False

    def validate(self):
        errors = self._arg_schema.validate(self.arguments)
        [self.status.errors.append(f"{k}: {v[0]}") for k, v in errors.items()]
        if len(self.status.errors) == 0:
            return True
        return False

    @property
    def _table(self) -> tuple:
        """Table of details of the class"""
        if hasattr(self, "entries") and len(self.entries) > 0:
            header = self.entries[0]._table[0]
            table = [t._table[1][0] for t in self.entries]
        else:
            if hasattr(self, "_arg_schema"):
                _parameters = list(self._arg_schema.fields.keys())
            else:
                _parameters = []
            _parameters += list(self._schema.fields.keys())
            try:
                _parameters.pop(_parameters.index("username"))
                _parameters.pop(_parameters.index("api_key"))
            except ValueError:
                pass

            header = [par for par in _parameters]
            table = []
            for row in _parameters:
                value = getattr(self, row)
                if row == "status" and type(value) != str:
                    table.append(value.status)
                else:
                    table.append(value)
            table = [table]
        return header, table

    def _repr_html_(self) -> str:
        if self.status.status == "Rejected":
            return "<b>Rejected with the following error(s): </b>" + " ".join(
                self.status.errors
            )
        else:
            header, table = self._table
            if len(table) > 0:
                return tablefy(table, header)
            else:
                return "No data"
