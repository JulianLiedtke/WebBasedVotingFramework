import abc
import logging
from src.util.utils import get_class_from_name, subclasses_recursive

log = logging.getLogger(__name__)


class ProtocolSuite():

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.connection = None
        self.abb = None

    def set_connections(self, connections):
        self.connection = connections

    def set_abb(self, abb):
        self.abb = abb

    def broadcast_and_receive(self, msg):
        return self.connection.broadcast_and_receive(msg)

    def init_protocol(self, prot):
        prot.connection = self.connection
        prot.abb = self.abb
        return prot

    def serialize(self):
        return self.__class__.__name__

    @classmethod
    def deserialize(cls, s):
        return get_class_from_name(s, subclasses_recursive(cls))

    @abc.abstractmethod
    def add(self, cipher1, cipher2):
        pass

    @abc.abstractmethod
    def mul(self, cipher1, cipher2):
        pass

    @abc.abstractmethod
    def eq(self, cipher1, cipher2):
        pass

    @abc.abstractmethod
    def gt(self, cipher1, cipher2):
        pass


class EmptyProtocolSuite(ProtocolSuite):

    def init_protocol(self, prot):
        prot.connection = self.connection
        prot.abb = self.abb
        return

    def add(self, cipher1, cipher2):
        return None

    def mul(self, cipher1, cipher2):
        return None

    def eq(self, cipher1, cipher2, bits):
        return None

    def gt(self, cipher1, cipher2, bits):
        return None
