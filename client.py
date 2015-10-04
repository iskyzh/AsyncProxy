import asyncio
import config
import struct

class DawnClientProtocol(asyncio.Protocol):
    def __init__(self, loop, dest_addr, dest_port):
        self.loop = loop
        self.dest_addr = dest_addr
        self.dest_port = dest_port
        self.transport = None

        self.data_size = 0

    def _get_addr_buffer(self):
        __addr_data = self.dest_addr.encode()
        __port_data = struct.pack("H", self.dest_port)
        return bytes([]).join([
            bytes([len(__port_data)]),
            __port_data,
            bytes([len(__addr_data)]),
            __addr_data
        ]).ljust(config.STAGE["HEADER"]["HEADER_LENGTH"])

    def send_command(self):
        print("[NOTICE] %d Bytes Transferred." % (self.data_size))
        self.transport.write(b"E" * 1024)
        print("[NOTICE] Command Sent")
        self.loop.call_later(1, self.send_command)

    def connection_made(self, transport):
        self.transport = transport
        print("[NOTICE] Connection Established, Sending Header")
        self.transport.write(self._get_addr_buffer())
        print("[NOTICE] Header Sent")
        self.loop.call_later(1, self.send_command)

    def data_received(self, data):
        self.data_size += len(data)
        # print(data.decode())
        pass

    def connection_lost(self, exc):
        print("[NOTICE] Connection Lost, %d Bytes Transferred." % (self.data_size))
        self.loop.stop()
