from MIDI import MIDIFile

# c = MIDIFile('audio/2020-10-02 Dan.mid')
# c = MIDIFile('audio/beat1.mid')
c = MIDIFile('audio/pirates.mid')
# print(type(c))
c.parse()

track = c[2]
track.parse()
print(str(track))

# print(str(c))

# for idx, track in enumerate(c):


# print(type(track))
# print(type(track))
# print(f'Track {idx}:')
#print()
# print(len(track))
# print(track.containsTiming)
#print(str(track))

# track = c[1]
# track.parse()
# t0 = 14791
# for ev in track:
#     if str(ev)[-13:] != 'velocity := 0':
#         print('ev.time', (ev.time - t0) / 3264 * 5.120, str(ev))



    # print('ev.header', ev.header)
    # print('ev.data', ev.data)
    # print('len(ev)', len(ev))
    # print('str(ev)', str(ev))
    # print()
