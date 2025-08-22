from logging import Formatter, LogRecord


class SafeRequestIDFormatter(Formatter):

    """

    A custom formatter that ensures every log record has a request ID.

    This formatter prevents errors when the request ID is missing by 
    assigning a default value.

    
    Usage
    -----
    ```
    "access": {
        "()": SafeRequestIDFormatter,
        "format": "%(asctime)s - %(levelname)s - %(name)s - [request-id=%(request_id)s] - %(message)s",
    },
    ```
    """

    def format(self, record: LogRecord) -> str:

        """

        Ensures the log record contains a request_id attribute.

        
        Parameters
        ----------
        record : LogRecord
            The log record to be formatted.

            
        Returns
        -------
        formatted_log : str
            The formatted log message string.

        """

        if not isinstance(record, LogRecord):
            raise TypeError(f"record must be an insatnce of the logging.LogRecord. Received: {record} with type {type(record)}")


        if not hasattr(record, "request_id"):
            record.request_id = "n/a"
        return super().format(record)
