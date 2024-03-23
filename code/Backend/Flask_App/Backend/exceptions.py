# Just the normal custom exceptions for fun and games
from werkzeug.exceptions import BadRequestKeyError

class MissingJSONKey(BadRequestKeyError):

    _fmt_key=' `{}`'
    _fmt_msg="Missing Key{} in request!\n"
    def __init__(self, missing_key=None, *args, **kwargs):
        if missing_key is None:
            self._fmt_key = ''
        else:
            self._fmt_key = self._fmt_key.format(missing_key)

        super().__init__(description=self.message, *args, **kwargs)

    @property
    def message(self):
        return self._fmt_msg.format(self._fmt_key)