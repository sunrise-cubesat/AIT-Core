from ait.core.server.plugins import Plugin
from ait.core import log
from ait.dsn.plugins.TCTF_Manager import check_data_field_size, get_max_data_field_size


class PacketPadder(Plugin):
    def __init__(self, inputs=None, outputs=None, zmq_args=None, **kwargs):
        super().__init__(inputs, outputs, zmq_args)
        self.size_pad_octets = get_max_data_field_size()
        
    def process(self, cmd_struct, topic=None):
        if not cmd_struct:
            log.error(f"received no data from {topic}.")
        if not check_data_field_size(cmd_struct.payload_bytes):
            log.error(f"initial data from {topic} is oversized.")
            cmd_struct.payload_size_valid = False
        if len(cmd_struct.payload_bytes) < self.size_pad_octets:
            fill = bytearray(self.size_pad_octets - len(cmd_struct.payload_bytes))
            cmd_struct.payload_bytes += fill
        if not check_data_field_size(cmd_struct.payload_bytes):
            log.error("Created oversized payload.")
            cmd_struct.payload_size_valid = False
        log.debug(f"publishing payload of size: {len(cmd_struct.payload_bytes)}")
        cmd_struct.processors.append(self.__class__)
        self.publish(cmd_struct)
