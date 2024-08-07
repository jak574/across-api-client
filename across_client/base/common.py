import warnings
from pathlib import PosixPath
from typing import Any, Type

import requests

from ..constants import API_URL
from ..functions import tablefy
from .schema import BaseSchema


class ACROSSBase:
    """
    Base class for ACROSS API Classes including common methods for all API classes.
    """

    # Type hints
    entries: list

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

    def api_url(self, argdict) -> str:
        """
        URL for this API call.

        Returns
        -------
        str
            URL for API call
        """
        # If arguments has `id` in it, then put this in the path
        if "id" in argdict.keys() and argdict["id"] is not None:
            return f"{API_URL}{self._mission.lower()}/{self._api_name.lower()}/{argdict['id']}"
        return f"{API_URL}{self._mission.lower()}/{self._api_name.lower()}"

    @property
    def schema(self) -> Any:
        """Return pydantic schema for this API class

        Returns
        -------
        object
            Pydantic Schema
        """
        return self._schema.model_validate(self)

    @property
    def parameters(self) -> dict:
        """
        Return parameters as dict

        Returns
        -------
        dict
            Dictionary of parameters
        """
        return {k: v for k, v in self._schema.model_validate(self) if v is not None}

    @parameters.setter
    def parameters(self, params: dict):
        """
        Set API parameters from a given dict which is validated from self._schema

        Parameters
        ----------
        params : dict
            Dictionary of class parameters
        """
        for k, v in self._schema(**params):
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
            # Create an array of parameters from the schema
            get_params = {
                key: value for key, value in self._get_schema.model_validate(self)
            }
            # Do the GET request
            req = requests.get(self.api_url(get_params), params=get_params, timeout=60)
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            elif req.status_code == 404:
                """Handle 404 errors gracefully, by issuing a warning"""
                warnings.warn(req.json()["detail"])
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
            # Create an array of parameters from the schema
            del_params = {
                key: value for key, value in self._del_schema.model_validate(self)
            }
            # Do the DELETE request
            req = requests.delete(
                self.api_url(del_params), params=del_params, timeout=60
            )
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            else:
                # Raise an exception if the HTML response was not 200
                req.raise_for_status()
        return False

    def put(self, payload={}) -> bool:
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
            Raised if PUT doesn't return a 201 response.
        """
        if self.validate_put():
            # Other non-file parameters
            put_params = {
                key: value
                for key, value in self._put_schema.model_validate(self)
                if key != "entries"
            }

            # URL for this API call
            api_url = self.api_url(put_params)
            if "id" in put_params.keys():
                put_params.pop("id")  # Remove id from query parameters

            # Extract any entries data, and upload this as JSON
            if hasattr(self, "entries") and len(self.entries) > 0:
                jsdata = self._put_schema.model_validate(self).model_dump(
                    include={"entries"}, mode="json"
                )
            # Or else pass any specific payload
            else:
                jsdata = payload

            # Make PUT request
            req = requests.put(
                api_url,
                params=put_params,
                json=jsdata,
                timeout=60,
            )
            if req.status_code == 201:
                # Parse, validate and record values from returned API JSON
                for k, v in self._schema.model_validate(req.json()):
                    setattr(self, k, v)
                return True
            elif req.status_code == 503:
                print("ERROR: ", req.status_code, "Service Unavailable for ", req.url)
            else:
                print("ERROR: ", req.status_code, req.json())
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
            Raised if POST doesn't return a 201 response.
        """
        if self.validate_post():
            # Extract any files out of the arguments
            files = {
                key: (
                    # Return either the existing filelike object, or open the file
                    value.name,
                    (
                        getattr(self, key.replace("filename", "file"))
                        if hasattr(self, key.replace("filename", "file"))
                        else value.open("rb")
                    ),
                )
                for key, value in self._post_schema.model_validate(self)
                if type(value) is PosixPath
            }

            # Extract query arguments
            post_params = {
                key: value
                for key, value in self._post_schema.model_validate(self)
                if key != "entries" and type(value) is not PosixPath
            }

            # Extract any entries data, and upload this as JSON
            if hasattr(self, "entries") and len(self.entries) > 0:
                jsdata = self._post_schema.model_validate(self).model_dump(
                    include={"entries"}, mode="json"
                )
            else:
                jsdata = {}

            if files == {}:
                # If there are no files, we can upload self.entries as JSON data
                req = requests.post(
                    self.api_url(post_params),
                    params=post_params,
                    json=jsdata,
                    timeout=60,
                )
            else:
                # Otherwise we need to use multipart/form-data for files, and pass the other parameters as query parameters
                req = requests.post(
                    self.api_url(post_params),
                    params=post_params,
                    files=files,
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
        if hasattr(self, "_get_schema"):
            self._get_schema.model_validate(self)
        else:
            warnings.warn("GET not allowed for this class.")
            return False
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
        if hasattr(self, "_put_schema"):
            self._put_schema.model_validate(self.__dict__)
        else:
            warnings.warn("PUT not allowed for this class.")
            return False
        return True

    def validate_post(self) -> bool:
        """Validate if value to be POST matches Schema

        Returns
        -------
        bool
            Is it validated? True | False
        """
        if hasattr(self, "_post_schema"):
            self._post_schema.model_validate(self.__dict__)
        else:
            warnings.warn("POST not allowed for this class.")
            return False
        return True

    def validate_del(self) -> bool:
        """Validate if value to be POST matches Schema

        Returns
        -------
        bool
            Is it validated? True | False
        """
        if hasattr(self, "_del_schema"):
            self._del_schema.model_validate(self.__dict__)
        else:
            warnings.warn("DELETE not allowed for this class.")
            return False
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
            _parameters += list(self.parameters.keys())
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

    def __repr__(self) -> str:
        # print a string showing the API call and arguments with their values
        # in a way that can be copied and pasted into a script
        args = ",".join([f"{k}={v}" for k, v in self.parameters.items()])
        return f"{self.__class__.__name__}({args})"
