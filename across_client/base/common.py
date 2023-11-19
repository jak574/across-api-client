import json
import warnings
from typing import Type
from urllib.parse import urlencode

import requests

from ..constants import API_URL
from ..functions import tablefy
from .schema import BaseSchema, JobInfo


class ACROSSBase:
    """
    Base class for ACROSS API Classes including common methods for all API classes.
    """

    # Type hints
    entries: list
    status: JobInfo

    # API descriptors type hints
    _schema: Type[BaseSchema]
    _get_schema: Type[BaseSchema]
    _put_schema: Type[BaseSchema]
    _post_schema: Type[BaseSchema]
    _del_schema: Type[BaseSchema]

    _mission: str
    _api_name: str = __name__

    def __getitem__(self, i):
        return self.entries[i]

    @property
    def api_url(self) -> str:
        """
        URL for this API call.

        Returns
        -------
        str
            URL for API call
        """
        argdict = self.arguments
        # If arguments has `id` in it, then put this in the path
        if "id" in argdict.keys() and argdict["id"] is not None:
            id = argdict.pop("id")
            return f"{API_URL}{self._mission}/{self._api_name}/{id}"
        return f"{API_URL}{self._mission}/{self._api_name}"

    @property
    def get_url(self) -> str:
        """
        Return URL for GET request.

        Returns
        -------
        str
            URL for GET API request
        """
        argdict = self.arguments
        # If arguments has `id` in it, then put this in the path
        if "id" in argdict.keys() and argdict["id"] is not None:
            _ = argdict.pop("id")
        return f"{self.api_url}?{urlencode(argdict)}"

    @property
    def arguments(self) -> dict:
        """
        Summary of validated arguments for API call.

        Returns
        -------
        dict
            Dictionary of arguments with values
        """
        # Send username/api_key if set
        if hasattr(self, "username") and hasattr(self, "api_key"):
            argdict = {"username": self.username, "api_key": self.api_key}
        else:
            argdict = {}

        for k in self._get_schema.model_fields.keys():
            if hasattr(self, k) and getattr(self, k) is not None:
                argdict[k] = getattr(self, k)

        return argdict

    @property
    def parameters(self) -> dict:
        """
        Return parameters as dict

        Returns
        -------
        dict
            Dictionary of parameters
        """
        return {
            k: v
            for k, v in self._schema.model_validate(self).__dict__.items()
            if v is not None
        }

    @parameters.setter
    def parameters(self, params: dict):
        """
        Set API parameters from a given dict which is validated from self._schema

        Parameters
        ----------
        params : dict
            Dictionary of class parameters
        """
        for k, v in self._schema(**params).model_dump().items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    def get(self) -> bool:
        """
        Perform a 'GET' submission to ACROSS API. Used for fetching
        information.

        Returns
        -------
        bool
            Was the get successful?

        Raises
        ------
        HTTPError
            Raised if GET doesn't return a 200 response.
        """
        if self.validate_get():
            req = requests.get(self.api_url, params=self.arguments, timeout=60)
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            else:
                # Raise an exception if the HTML response was not 200
                req.raise_for_status()
        return False

    def delete(self) -> bool:
        """
        Perform a 'GET' submission to ACROSS API. Used for fetching
        information.

        Returns
        -------
        bool
            Was the get successful?

        Raises
        ------
        HTTPError
            Raised if GET doesn't return a 200 response.
        """
        if self.validate_del():
            req = requests.delete(self.api_url, params=self.arguments, timeout=60)
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            else:
                # Raise an exception if the HTML response was not 200
                req.raise_for_status()
        return False

    def put(self) -> bool:
        """
        Perform a 'PUT' submission to ACROSS API. Used for pushing/replacing
        information.

        Returns
        -------
        bool
            Was the get successful?

        Raises
        ------
        HTTPError
            Raised if GET doesn't return a 201 response.
        """
        if self.validate_put():
            req = requests.put(
                self.api_url,
                params=self.arguments,
                json=json.loads(
                    self._put_schema.model_validate(self).model_dump_json()
                ),
                timeout=60,
            )
            if req.status_code == 201:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            else:
                req.raise_for_status()
        return False

    def post(self) -> bool:
        """
        Perform a 'PUT' submission to ACROSS API. Used for pushing/replacing
        information.

        Returns
        -------
        bool
            Was the get successful?

        Raises
        ------
        HTTPError
            Raised if GET doesn't return a 201 response.
        """
        if self.validate_post():
            req = requests.post(
                self.api_url,
                params=self.arguments,
                json=json.loads(
                    self._post_schema.model_validate(self).model_dump_json()
                ),
                timeout=60,
            )
            if req.status_code == 201:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            elif req.status_code == 200:
                warnings.warn(req.json()["detail"])
                return False
            else:
                # Raise an exception if the HTML response was not 200
                req.raise_for_status()
        return False

    def validate_get(self) -> bool:
        """Validate arguments for GET

        Returns
        -------
        bool
            Do arguments validate? True | False

        Raises
        ------
        ValidationError
            If arguments don't validate
        """

        self._get_schema.model_validate(self)
        return True

    def validate_put(self) -> bool:
        """Validate if value to be PUT matches Schema

        Returns
        -------
        bool
            Is it validated? True | False

        Raises
        ------
        ValidationError
            If the value to be PUT doesn't match the Schema


        """

        self._put_schema.model_validate(self.__dict__)
        return True

    def validate_post(self) -> bool:
        """Validate if value to be POST matches Schema

        Returns
        -------
        bool
            Is it validated? True | False
        """
        self._post_schema.model_validate(self.__dict__)
        return True

    def validate_del(self) -> bool:
        """Validate if value to be POST matches Schema

        Returns
        -------
        bool
            Is it validated? True | False
        """

        self._del_schema.model_validate(self.__dict__)
        return True

    @property
    def _table(self) -> tuple:
        """
        Table with head showing results of the API query.

        Returns
        -------
        tuple
            Tuple containing two lists, the header and the table data
        """
        if hasattr(self, "entries") and len(self.entries) > 0:
            header = self.entries[0]._table[0]
            table = [t._table[1][0] for t in self.entries]
        else:
            # Start with arguments
            if hasattr(self, "_get_schema"):
                _parameters = list(self.parameters.keys())
            else:
                _parameters = []
            _parameters += list(self.arguments.keys())
            # Don't include username/api_key in table
            try:
                _parameters.pop(_parameters.index("username"))
                _parameters.pop(_parameters.index("api_key"))
            except ValueError:
                pass

            # Removed repeated values
            _parameters = list(set(_parameters))

            header = [par for par in _parameters]
            table = []
            for row in _parameters:
                value = getattr(self, row)
                if row == "status" and not isinstance(value, str):
                    table.append(value.status)
                else:
                    table.append(value)
            table = [table]
        return header, table

    def _repr_html_(self) -> str:
        """Return a HTML summary of the API data, for e.g. Jupyter.

        Returns
        -------
        str
            HTML summary of data
        """
        header, table = self._table
        if len(table) > 0:
            return tablefy(table, header)
        else:
            return "No data"
