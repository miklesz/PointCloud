from MIDI import MIDIFile

# name = 'audio/MIDI perka melody.mid'
name = 'audio/MIDI perka.mid'
# name = 'audio/co sekunde.mid'
# name = 'audio/2020-10-02 Dan.mid'
# name = 'audio/beat1.mid'
# name = 'audio/pirates.mid'
# c = MIDIFile('audio/probe.mid')
c = MIDIFile(name)
print(name)
# print(type(c))
c.parse()
print(c)

track = c[0]
track.parse()
# print(str(track))

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
t0 = 16624
for ev in track:
    if 'NOTE_ON' in str(ev):
        # print('time='+str((ev.time - t0)/192)+' '+str(ev.message))
        print('time='+str((ev.time - t0)/96*2)+' '+str(ev.message))



    # print('ev.header', ev.header)
    # print('ev.data', ev.data)
    # print('len(ev)', len(ev))
    # print('str(ev)', str(ev))
    # print()
