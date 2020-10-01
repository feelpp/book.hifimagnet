from nptdms import TdmsFile

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

input_file="M9_Default_200921-123303_Courants50Hz.tdms"
with TdmsFile.open(input_file) as tdms_file:
    # Iterate over all items in the file properties and print them
    for name, value in tdms_file.properties.items():
        print("{0}: {1}".format(name, value))

    # List groups
    all_groups = tdms_file.groups()
    print("all_groups=", all_groups)

    # for a given group
    group = tdms_file['Courants et Ref. Alimentations']

    # List Groups and Channels per Group
    all_group_channels = group.channels()
    print(all_group_channels)
    
    for group in all_groups:
        print("group=", group.name)
        all_group_channels = group.channels()
        print(all_group_channels)

        for channel in all_group_channels:
            print("channel=", channel.name)

            # Get a channel property
            property_list = tdms_file[group.name][channel.name].properties
            print("property_list=", property_list, "type(property_list)=", type(property_list))

            all_channel_data = channel[:]
            # print("data=", all_channel_data)

    group = tdms_file['Courants et Ref. Alimentations']
    channel = group['Courant_A1']

    # 'wf_start_time'
    start_timestamp = channel.properties['wf_start_time']
    print("start_time=", start_timestamp)
            
    # 'wf_start_offset'
    start_offset = channel.properties['wf_start_offset']
    print("start_offset=", start_offset)
            
    # 'wf_increment'
    increment = channel.properties['wf_increment']
    print("increment=", increment)
    
    # 'wf_samples'
    samples = channel.properties['wf_samples']
    # 'unit_string'
    time_steps = np.array([i*increment for i in range(0,samples)])
            
    ax = plt.gca()
    plt.plot(time_steps, channel[:], label="A1")
    plt.plot(time_steps, group['Courant_A2'][:], label="A2")
    plt.ylabel(channel.name + " [" + channel.properties['unit_string'] + "]")
    plt.xlabel("t [s]")
    plt.grid(b=True)
    ax.legend()
    plt.show()
