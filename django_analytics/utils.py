import re
from user_agents import parse
from .models import UserAgent


class Info:
    def __init__(self, request) -> None:
        self._request = request
        self._device_type = {}
        self._user_agent_dict = {}

    @property
    def get_ip(self) -> str:
        """
        Retrieves the remote IP address from the request data.  If the user is
        behind a proxy, they may have a comma-separated list of IP addresses, so
        we need to account for that.  In such a case, only the first IP in the
        list will be retrieved.  Also, some hosts that use a proxy will put the
        REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
        IP from the proper place.

        **NOTE** This function was taken from django-tracking (MIT LICENSE)
                http://code.google.com/p/django-tracking/
        """

        # if neither header contain a value, just use local loopback

        # this is not intended to be an all-knowing IP address regex
        IP_RE = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        ip_address = self._request.META.get(
            "HTTP_X_FORWARDED_FOR", self._request.META.get("REMOTE_ADDR", "127.0.0.1")
        )
        if ip_address:
            # make sure we have one and only one IP
            try:
                ip_address = IP_RE.match(ip_address)
                if ip_address:
                    ip_address = ip_address.group(0)
                else:
                    # no IP, probably from some dirty proxy or other device
                    # throw in some bogus IP
                    ip_address = "10.0.0.1"
            except IndexError:
                pass

        return ip_address

    def _get_device_type(self) -> UserAgent:

        # Supplements information about the device.
        device_type = parse(self._request.META.get("HTTP_USER_AGENT", ""))
        if device_type.is_mobile:
            self._device_type["device_type"] = "Mobile"
            self._device_type["device_brand"] = device_type.device.brand
            self._device_type["device_family"] = device_type.device.family
            self._device_type["device_model"] = device_type.device.model
            self._device_type["os_family"] = device_type.os.family
            self._device_type["os_version"] = device_type.os.version_string
            self._device_type["touch_screen"] = device_type.is_touch_capable
            return self._device_type
        elif device_type.is_tablet:
            self._device_type["device_type"] = "Tablet"
            self._device_type["device_brand"] = device_type.device.brand
            self._device_type["device_family"] = device_type.device.family
            self._device_type["device_model"] = device_type.device.model
            self._device_type["os_family"] = device_type.os.family
            self._device_type["os_version"] = device_type.os.version_string
            self._device_type["touch_screen"] = device_type.is_touch_capable
            return self._device_type
        elif device_type.is_pc:
            self._device_type["device_type"] = "PC"
            self._device_type["os_family"] = device_type.os.family
            self._device_type["os_version"] = device_type.os.version_string
            self._device_type["touch_screen"] = device_type.is_touch_capable
            return self._device_type

    @property
    def get_user_agent(self) -> UserAgent:
        """
        Retrieves device data from HTTP_USER_AGENT using a library "python-user-agents".
        And saves the retrieved data to a dictionary.

        **NOTE** https://github.com/selwin/python-user-agents
        """

        self._user_agent_dict.update(self._get_device_type())
        parse_user_agent = parse(self._request.META.get("HTTP_USER_AGENT", ""))
        self._user_agent_dict["browser"] = parse_user_agent.browser.family
        self._user_agent_dict[
            "browser_version"
        ] = parse_user_agent.browser.version_string

        return self._user_agent_dict
