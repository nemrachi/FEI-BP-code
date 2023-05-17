from mocap_api import *
import socket
import time
import sys

# USB Transceiver
# PID: N3TOA09033C
# IP: 192.168.1.254 / 192.168.1.159
# Current: 9.9.9.34 (usb?)
# port: 34048

HOST = '192.168.1.159'
PORT = 51128

#######################
# MOCAP API functions #
#######################

def init_mocap_api():
    global mocap_app
    mocap_app = MCPApplication()
    # mocap_app.enable_event_cache()
    render_settings = MCPRenderSettings()
    render_settings.set_up_vector(MCPUpVector.ZAxis, 1)
    render_settings.set_coord_system(MCPCoordSystem.RightHanded)
    render_settings.set_front_vector(MCPFrontVector.ParityEven, -1)
    render_settings.set_rotating_direction(MCPRotatingDirection.CounterClockwise)
    render_settings.set_unit(MCPUnit.Meter)
    mocap_app.set_render_settings(render_settings)

def uninit_mocap_api():
    global mocap_app
    close_api()
    mocap_app = None

def create_udp_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

def axis_connect():
    create_udp_server()
    settings = MCPSettings()
    #settings.set_tcp(HOST, PORT)
    #settings.set_udp_server(HOST, PORT)
    settings.set_udp(7002)
    # settings.set_bvh_data(MCPBvhData.Binary)
    # settings.set_bvh_rotation(MCPBvhRotation.YXZ)
    mocap_app.set_settings(settings)
    close_api()
    status, msg = mocap_app.open()
    print('Connect Successful' if status else 'ERROR\nConnect failed: {0}'.format(msg))

def axis_disconnect():
    status, msg = mocap_app.close()
    print('Disconnect Successful' if status else 'ERROR\nDisconnect failed: {0}'.format(msg))

def axis_start_record():
    command = MCPCommand(MCPCommands.CommandStartRecored)
    # command.get_command_result_code()
    # command.get_command_result_message()
    
def axis_stop_record():
    command = MCPCommand(MCPCommands.CommandStopRecored)
    # command.destroy_command()

def start_capture():
    command = MCPCommand(MCPCommands.CommandStartCapture)

def stop_capture():
    command = MCPCommand(MCPCommands.CommandStopCapture)

def poll_data():
    # evts = mocap_app.poll_next_event()
    # for evt in evts:
    #     if evt.event_type == MCPEventType.AvatarUpdated:
    #         avatar = MCPAvatar(evt.event_data.avatar_handle)
    #         print('{0}\n{1} '.format(avatar.get_name(), avatar.get_index()), end='')
    #         Utils.print_joint(avatar.get_root_joint())
    #         # animate_armatures(ctx, avatar)
    #     elif evt.event_type == MCPEventType.RigidBodyUpdated:
    #         print('Rigid body updated')
    #     else:
    #         Utils.print_error(evt)
    # print('hih')
    print(server_socket.recvfrom(10000000))

#######################
#   OTHER functions   #
#######################

def close_api():
    if mocap_app.is_opened(): mocap_app.close()

def reset_stdout():
    sys.stdout.close()
    sys.stdout = sys.__stdout__

#######################
#    MAIN function    #
#######################

if __name__ == '__main__':
    try:
        init_mocap_api()
        axis_connect()
        start_capture()
        print('\nCapturing data ...\n')
        #sys.stdout = open('./captured_data.txt', 'w')
        #server_socket.settimeout(2)
        while True:
            poll_data()
            time.sleep(1)
    except Exception as e:
        #reset_stdout()
        print('\nEXCEPTION --> {0} <--\n'.format(e), file=sys.stderr)
    finally:
        #reset_stdout()
        stop_capture()
        # mocap_app.queued_server_command(startrec.handle)
        axis_disconnect()
        server_socket.close()