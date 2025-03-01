from enum import Enum


class MessageType(Enum):
    """
    Use these types to annotate pub sub messages for modules that:
      1. Publishes multiple types of data.
      2. The published data is passed to an external application (openmctvia websocket).
      3. A non plugin module is borrowing a plugin's publish function, making it not obvious that PUB/SUB messages are being emitted. (See RAF SLE interface for example).

    It's not necessary to use these types for inter plugin communication. Continue to use plugin names or strings to explicitly chain plugins together into a pipeline.

    USAGE:
        Send a message:
          self.publish(packet_metadata_list, MessageType.VCID_COUNT.name)
    """
    REAL_TIME_TELEMETRY = "realtime telemetry packets and metadata"
    STORED_TELEMETRY = "stored telemetry packets and metadata"
    VCID_COUNT = "vcid counts"
    LOG = "messages from log stream"
    CLTU_STATUS = "CLTU interface: <ACTIVE|READY|UNBOUND>,\n last status report,\n count of CLTU sent"
    RAF_DATA = "Raw telemetry from RAF Interface"
    RAF_STATUS = "RAF interface: <ACTIVE|READY|UNBOUND>,\n  last status report,\n count of data received"
    HIGH_PRIORITY_CLTU_STATUS = "High priority CLTU Interfce Status\n (Disconnect/Restarts)"
    HIGH_PRIORITY_RAF_STATUS = "High priority RAF Interfce Status\n (Disconnect/Restarts)"
    TCP_STATUS = "Number of packets transferred/received"
    KMC_STATUS = "If message is received\n, KMC Plugin is active"
    SC_STATE_OF_HEALTH_REPORT = "Spacecraft state of health report"
    FILE_DOWNLINK_RESULT = "Result of a File Downlink Reassembly Task"
    FILE_DOWNLINK_UPDATE = "Result of a File Dowlink Update Task"
    TASK_S3_UPLOAD_RESULT = "Result of an S3 File Upload Task"
    PANIC = "Something has thrown an exception"
    CL_AUTO = "Automatic internally generated command uplinks"
    CL_LIST = 'List command loader scripts,\n message is path or "" '
    CL_SHOW = 'Get contents of command loader\n script or uplink info,\n message is path to\n command loader script or uplink directory'
    CL_EXECUTE = 'Have command loader execute\n a command from the dicionary,\n message is a command\n or uplink directory'
    CL_VALIDATE = 'Have command loader verify\n a script, command, or\n uplink path'
    CL_RESULT = 'Contains result of Command Loader action\n {(action, argument): (BOOL, [Errors])}'
    CL_UPLINK_COMPLETE = 'Completed CmdMetaData'
    CL_UPLINK_STATUS = 'Status of Uplink Command'
    FM_TASK_DONE = 'Generic task done\n for File Manager'
    FM_DL_STATUS = "Status of completed\n downlinks and S3 uploads"
    SLE_CLTU_RESTART = "Force an SLE CLTU Interface Restart"
    SLE_RAF_RESTART = "Force an SLE RAF Interface Restart"
    SLE_CLTU_STOP = "Force an SLE CLTU Interface to stop"
    SLE_RAF_STOP = "Force an SLE RAF Interface to stop"
    FM_RETRANSMIT_CL = 'A file downlink retransmission suggestion CL'
    FM_MISSED_DOWNLINK_INIT = 'Missed File Initalize Downlink Reply'
    FM_PAYLOAD_UPDATE = 'Payload Updates'
    CHECK_FRAME_OUT_OF_SEQUENCE = 'Out of sequence Frames'
    CHECK_FRAME_ECF_MISMATCH = 'Mismatch of Frame ECF'
    UPLINK_TRACKER_PROBE = 'Send uplink tracker Probe'
    UPLINK_TRACKER_ZOMBIES = 'Response containing zombied uplinks'
    UPLINK_TRACKER_STATUS = 'Request status'
    UPLINK_TRACKER_STATUS_RESULT = 'Result to request'
    DEPACKETIZER_REPORT = 'Depacketizer error report'
    SUNRISE_PAYLOAD_ACTIVE_FILE_DOWNLINK_INFO = 'See fgicd'

    def to_tuple(self):
        return (self.name, self.value)
