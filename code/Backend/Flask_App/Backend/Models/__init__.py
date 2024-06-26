# 90sNet manages a ctf 
# Copyright (C) 2024  Joshua Hale and Chad Lape

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Providing Imports
from .event import Event as Event
from .machine import Machine as Machine
from .user import User as User
#from .api_runner import API_Runner as API_Runner

from typing import Union
Models = Union[Event, Machine, User]
