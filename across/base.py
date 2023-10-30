from urllib.parse import urlencode
import requests
from .constants import API_URL
from .functions import tablefy
from marshmallow import Schema
from .jobstatus import JobStatus


class ACROSSBase:
    """
    Mixin for ACROSS API Classes including common methods for all API classes.
    """

    # Type hints
    entries: list
    status: JobStatus

    # API descriptors type hints
    _schema: Schema
    _get_schema: Schema
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
        api_params = urlencode(self.arguments)
        return f"{self.api_url}?{api_params}"

    @property
    def arguments(self) -> dict:
        """
        Summary of validated arguments for API call.

        Returns
        -------
        dict
            Dictionary of arguments with values
        """
        return {k: v for k, v in self._get_schema.dump(self).items() if v is not None}  # type: ignore

    @property
    def parameters(self) -> dict:
        """
        Return parameters as dict

        Returns
        -------
        dict
            Dictionary of parameters
        """
        return {k: v for k, v in self._schema.dump(self).items() if v is not None}  # type: ignore

    @parameters.setter
    def parameters(self, params: dict):
        """
        Set API parameters from a given dict which is validated from self._schema

        Parameters
        ----------
        params : dict
            Dictionary of class parameters
        """
        _ = [
            setattr(self, k, v)
            for k, v in self._schema.load(params).__dict__.items()
            if v is not None
        ]

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
        if self.validate():
            req = requests.get(self.api_url, params=self.arguments)
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                self.parameters = self._schema.loads(req.text).parameters  # type: ignore
                if self.status.status == "Accepted":
                    return True
                else:
                    return False
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
            Raised if GET doesn't return a 200 response.
        """
        if self.validate():
            req = requests.put(
                self.api_url, params=self.arguments, json=self._put_schema.dump(self)
            )
            if req.status_code == 200:
                # Parse, validate and record values from returned API JSON
                self.parameters = self._schema.loads(req.text).parameters  # type: ignore
                if self.status.status == "Accepted":
                    return True
                else:
                    return False
            # Raise an exception if the HTML response was not 200
            req.raise_for_status()
        return False

    def validate(self) -> bool:
        """"""
        """Perform validation of arguments against schema, record those errors
        in JobStatus

        Returns
        -------
        bool
            Did validation pass with no errors? (True | False)
        """
        errors = self._get_schema.validate(self.arguments)
        [self.status.errors.append(f"{k}: {v[0]}") for k, v in errors.items()]
        if len(self.status.errors) == 0:
            return True
        return False

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
                if row == "status" and type(value) != str:
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
        if hasattr(self, "status") and self.status.status == "Rejected":
            return "<b>Rejected with the following error(s): </b>" + " ".join(
                self.status.errors
            )
        else:
            header, table = self._table
            if len(table) > 0:
                return tablefy(table, header)
            else:
                return "No data"
