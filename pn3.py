from mocap_api import *
import time

# ???
# PID: N3TOA09033C
# IP: 192.168.1.254 / 192.168.1.159
# Current?: 9.9.9.34

if __name__ == '__main__':
    mocap_app = MCPApplication()
    settings = MCPSettings()
    settings.set_udp_server('255.255.255.255', 8901)
    #settings.set_udp(7002)
    mocap_app.set_settings(settings)
    status, msg = mocap_app.open()
    if status:
        print ('Connect Successful')
    else:
        print ({'ERROR'}, 'Connect failed: {0}'.format(msg))
    startcap = MCPCommand(MCPCommands.CommandStartCapture)
    # startrec = MCPCommand(MCPCommands.CommandStartRecored)
    # startrec.get_command_result_code()
    while True:
        evts = mocap_app.poll_next_event()
        for evt in evts:
            if evt.event_type == MCPEventType.AvatarUpdated:
                avatar = MCPAvatar(evt.event_data.avatar_handle)
                print(avatar.get_index())
                print(avatar.get_name())
                print_joint(avatar.get_root_joint())
            elif evt.event_type == MCPEventType.RigidBodyUpdated:
                print('rigid body updated')
            else:
                print_error(evt)
        time.sleep(1)
    # stoprec = MCPCommand(MCPCommands.CommandStopRecored)
    # command.destroy_command()
    # startrec.get_command_result_message()
    # # mocap_app.queued_server_command(startrec.handle)
    # mocap_app.close()