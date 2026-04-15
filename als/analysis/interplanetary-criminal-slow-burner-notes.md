# Interplanetary Criminal - Slow Burner — Complete Technical Reference

**Tempo:** 136.0 BPM

## Track Hierarchy

### A: **Vocals** | bars 12.75–130.0
  **VST:** Kickstart 2 | preset=''
  Clips (1):
    bar 12.75–130.0 ''

### G: **Low End**
  #### M: **Kick** | bars 30.0–127.25
    **Simpler** sample='Kick.wav' path=''
      SampleStart: 0
      LoopMode: 0
    Clips (5):
      bar 30.0–45.25 '' → notes: ['C3']
      bar 46.0–61.25 '' → notes: ['C3']
      bar 62.0–70.0 '' → notes: ['C3']
      bar 96.0–111.25 '' → notes: ['C3']
      bar 112.0–127.25 '' → notes: ['C3']

  #### M: **Bass** | bars 30.0–128.0
    **MidiPitcher**: On=true, Pitch=-12, Range=127
    **VST:** Serum 2 | preset=''
    **EQ8** (0 active bands)
    **MultibandDynamics**: DryWet=1
    **VST:** Kickstart 2 | preset=''
    Clips (4):
      bar 30.0–45.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']
      bar 46.0–62.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']
      bar 96.0–111.0 '' → notes: ['A3', 'C4', 'D4', 'E3', 'E4', 'E5', 'G3', 'G4']
      bar 112.0–128.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']

  #### M: **Break Bass** | bars 62.0–70.0
    **VST:** Serum 2 | preset=''
    **VST:** Kickstart 2 | preset=''
    Clips (1):
      bar 62.0–70.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']


### G: **Drums**
  **AudioEffectGroupDevice**: On=true, DryWet=1, Type=5, ColorOn=true, ColorFrequency=1000.00018, ColorWidth=0.3000000119, Drive=1, Lin=0.5, Speaker=true, Volume=1
  #### M: **Crash Delayed** | bars 13.0–129.0
    **Simpler** sample='Crash Delayed.wav' path=''
      Attack: 0.1000000015
      SampleStart: 0
      LoopMode: 0
    Clips (15):
      bar 13.0–15.0 '' → notes: ['C3']
      bar 30.0–31.0 '' → notes: ['C3']
      bar 37.0–38.5 '' → notes: ['C3']
      bar 45.0–47.0 '' → notes: ['C3']
      bar 53.0–54.5 '' → notes: ['C3']
      ... +10 more clips

  #### M: **Snare** | bars 26.0–78.0
    **Simpler** sample='Snare.wav' path=''
      Attack: 0.1000000015
      SampleStart: 0
      LoopMode: 0
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    Clips (2):
      bar 26.0–30.0 '' → notes: ['C3']
      bar 74.0–78.0 '' → notes: ['C3']

  #### M: **Tambourine** | bars 46.0–127.0
    **Simpler** sample='Tambourine.wav' path=''
      Attack: 0.1000000015
      SampleStart: 0
      LoopMode: 0
    **Reverb**: PreDelay=7.99999094, RoomSize=2, DecayTime=1222.97546, FreezeOn=false
    Clips (2):
      bar 46.0–61.0 '' → notes: ['C3']
      bar 112.0–127.0 '' → notes: ['C3']

  #### A: **Shaker** | bars 30.0–127.0
    **Reverb**: PreDelay=7.99999094, RoomSize=2, DecayTime=1222.97546, FreezeOn=false
    **EQ8** (0 active bands)
    Clips (4):
      bar 30.0–45.0 ''
      bar 46.0–61.0 ''
      bar 96.0–111.0 ''
      bar 112.0–127.0 ''

  #### A: **Breaks** | bars 70.0–78.0
    **EQ8** (0 active bands)
    **AutoFilter**: Cutoff=79.296875, Drive=0, Frequency=0.1099999994, Resonance=0.5654761791, Slope=true, DryWet=1
    Clips (1):
      bar 70.0–78.0 ''

  #### G: **Main**
    **Reverb**: PreDelay=7.99999094, RoomSize=2, DecayTime=1222.97546, FreezeOn=false
    **AutoFilter**: Cutoff=78.4126968, Drive=0, Frequency=0.1099999994, Resonance=0.1379310191, Slope=true, DryWet=1
    ##### M: **Clap** | bars 10.0–127.0
      **Simpler** sample='Clap.wav' path=''
        SampleStart: 0
        LoopMode: 0
      Clips (5):
        bar 10.0–29.0 '' → notes: ['C3']
        bar 30.0–45.0 '' → notes: ['C3']
        bar 46.0–61.0 '' → notes: ['C3']
        bar 96.0–111.0 '' → notes: ['C3']
        bar 112.0–127.0 '' → notes: ['C3']

    ##### M: **Open Hat** | bars 10.0–127.0
      **Simpler** sample='Open Hat.wav' path=''
        Attack: 0.1000000015
        SampleStart: 0
        LoopMode: 0
      Clips (5):
        bar 10.0–29.0 '' → notes: ['C3']
        bar 30.0–45.0 '' → notes: ['C3']
        bar 46.0–61.0 '' → notes: ['C3']
        bar 96.0–111.0 '' → notes: ['C3']
        bar 112.0–127.0 '' → notes: ['C3']

    ##### A: **Perc Akcent** | bars 10.0–127.0
      Clips (5):
        bar 10.0–29.0 ''
        bar 30.0–45.0 ''
        bar 46.0–61.0 ''
        bar 96.0–111.0 ''
        bar 112.0–127.0 ''



### G: **Instruments**
  #### M: **90s Piano** | bars 10.0–127.0
    **VST:** Serum 2 | preset=''
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1.37969279, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    **EQ8** (0 active bands)
    **AutoFilter**: Cutoff=20, Drive=0, Frequency=0.1099999994, Resonance=0.1379310191, Slope=true, DryWet=1
    **VST:** Kickstart 2 | preset=''
    Clips (4):
      bar 10.0–29.0 '' → notes: ['B2', 'B3', 'C3', 'C4', 'D3', 'D4', 'E3', 'F#3', 'G3']
      bar 46.0–61.0 '' → notes: ['B2', 'B3', 'C3', 'C4', 'D3', 'D4', 'E3', 'F#3', 'G3']
      bar 78.0–93.0 '' → notes: ['B2', 'B3', 'C3', 'C4', 'D3', 'D4', 'E3', 'F#3', 'G3']
      bar 104.0–127.0 '' → notes: ['B2', 'B3', 'C3', 'C4', 'D3', 'D4', 'E3', 'F#3', 'G3']

  #### M: **Organ** | bars 10.0–78.0
    **VST:** Serum 2 | preset=''
    **EQ8** (0 active bands)
    **AutoFilter**: Cutoff=20, Drive=0, Frequency=0.1099999994, Resonance=0.1379310191, Slope=true, DryWet=1
    **VST:** Kickstart 2 | preset=''
    Clips (2):
      bar 10.0–29.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']
      bar 62.0–78.0 '' → notes: ['A3', 'C4', 'E3', 'E4', 'G3']


### G: **Fx**
  #### M: **Laser Fx** | bars 74.0–92.0
    **VST:** Serum 2 | preset=''
    Clips (2):
      bar 74.0–76.0 '' → notes: ['C3']
      bar 90.0–92.0 '' → notes: ['C3']

  #### A: **Clock Fx** | bars 78.0–93.0
    **EQ8** (0 active bands)
    Clips (1):
      bar 78.0–93.0 ''

  #### A: **Impact** | bars 22.0–103.0
    **EQ8** (0 active bands)
    Clips (6):
      bar 22.0–29.0 ''
      bar 30.0–37.0 ''
      bar 38.0–45.0 ''
      bar 70.0–76.0 ''
      bar 86.0–93.0 ''
      ... +1 more clips

