# BL3SS x CamrinWatsin - Kisses — Complete Technical Reference

**Tempo:** 142.0 BPM

## Track Hierarchy

### A: **Vocals** | bars 0.188–82.022
  **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
  **MultibandDynamics**: DryWet=1
  **Compressor2**: Threshold=0.1728025377, Ratio=3.00000024, Attack=0.02275845967, Release=100.000008, Gain=3, Knee=6.046875, DryWet=1, Model=0
  Clips (1):
    bar 0.188–82.022 ''

### G: **Drums**
  **Overdrive**: Drive=60, DryWet=5
  **Overdrive**: Drive=50, DryWet=1.5625
  **DrumBuss**: DryWet=0.1000000015
  **GlueCompressor**: Threshold=-17.4603176, Ratio=0, Attack=4, Release=0, Gain=0, DryWet=0.5
  #### M: **Kick** | bars 16.0–79.0
    **Simpler** sample='Kick.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    Clips (8):
      bar 16.0–24.0 '' → notes: ['C3']
      bar 24.0–31.0 '' → notes: ['C3']
      bar 32.0–39.0 '' → notes: ['C3']
      bar 39.5–40.0 '' → notes: ['C3']
      bar 40.0–47.0 '' → notes: ['C3']
      ... +3 more clips

  #### M: **Clap** | bars 32.0–80.0
    **Simpler** sample='Clap.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    **EQ8** (0 active bands)
    **Reverb**: PreDelay=7.99999094, RoomSize=2, DecayTime=1279.60938, FreezeOn=false
    Clips (3):
      bar 32.0–48.0 '' → notes: ['A#2']
      bar 56.0–63.0 '' → notes: ['A#2']
      bar 64.0–80.0 '' → notes: ['A#2']

  #### M: **Hat** | bars 32.0–80.0
    **Simpler** sample='Hat.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, BassMonoFrequency=120, Gain=1
    Clips (2):
      bar 32.0–48.0 '' → notes: ['C3']
      bar 64.0–80.0 '' → notes: ['C3']

  #### M: **Open Hat 1** | bars 32.0–80.0
    **Simpler** sample='Open Hat 1.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    **DrumBuss**: DryWet=0.453125
    **Overdrive**: Drive=50, DryWet=6.25
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, BassMonoFrequency=120, Gain=1
    Clips (2):
      bar 32.0–48.0 '' → notes: ['C3']
      bar 64.0–80.0 '' → notes: ['C3']

  #### M: **Open Hat 2** | bars 16.0–63.0
    **Simpler** sample='Open Hat 2.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    Clips (2):
      bar 16.0–23.0 '' → notes: ['C3']
      bar 48.0–63.0 '' → notes: ['C3']

  #### M: **Open Hat 3** | bars 56.0–63.0
    **Simpler** sample='Open Hat 3.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    Clips (1):
      bar 56.0–63.0 '' → notes: ['C3']

  #### M: **Snare 1** | bars 39.0–80.0
    **Simpler** sample='Snare 1.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    Clips (4):
      bar 39.0–40.0 '' → notes: ['C3']
      bar 47.0–48.0 '' → notes: ['C3']
      bar 71.0–72.0 '' → notes: ['C3']
      bar 79.0–80.0 '' → notes: ['C3']

  #### M: **Snare 2** | bars 16.0–63.0
    **Simpler** sample='Snare 2.wav' path=''
      SampleStart: 0
      LoopMode: 0
    **EQ8** (0 active bands)
    **Reverb**: PreDelay=2.50000048, RoomSize=10.860774, DecayTime=1222.97546, FreezeOn=false
    Clips (2):
      bar 16.0–23.0 '' → notes: ['C3']
      bar 48.0–63.0 '' → notes: ['C3']


### G: **Instrument**
  **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=0.7943282127
  **Saturator**: Drive=1, DryWet=0.1000000015, Type=4
  **Compressor2**: Threshold=0.07838593423, Ratio=1.20000005, Attack=12.4519739, Release=1018.55811, Gain=4, Knee=12, DryWet=1, Model=1
  #### M: **Organ Bass** | bars 8.0–63.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    **Saturator**: Drive=1, DryWet=0.1190476194, Type=4
    **MultibandDynamics**: DryWet=1
    Clips (4):
      bar 8.0–16.0 '' → notes: ['A#2', 'C2', 'D2', 'D3', 'F2', 'G2']
      bar 16.0–23.0 '' → notes: ['D2', 'D3']
      bar 48.0–56.0 '' → notes: ['A#2', 'C2', 'D2', 'D3', 'F2', 'G2']
      bar 56.0–63.0 '' → notes: ['D2', 'D3']

  #### M: **FM Bass** | bars 24.0–80.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, BassMonoFrequency=120, Gain=1
    Clips (2):
      bar 24.0–48.0 '' → notes: ['A#2', 'C3', 'D2', 'D3', 'F2', 'G2']
      bar 64.0–80.0 '' → notes: ['A#2', 'C3', 'D2', 'D3', 'F2', 'G2']

  #### M: **Pluck 1** | bars 32.0–80.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **VST:** Kickstart 2 | preset=''
    Clips (2):
      bar 32.0–48.0 '' → notes: ['A#2', 'A3', 'C4', 'D3', 'E3', 'F2', 'F3', 'G2']
      bar 64.0–80.0 '' → notes: ['A#2', 'A3', 'C4', 'D3', 'E3', 'F2', 'F3', 'G2']

  #### M: **Saws 1** | bars 40.0–80.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **MultibandDynamics**: DryWet=1
    **VST:** Kickstart 2 | preset=''
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    **Reverb**: PreDelay=51.5807152, RoomSize=95.6207199, DecayTime=3792.36401, FreezeOn=false
    Clips (4):
      bar 40.0–48.0 '' → notes: ['A2', 'C3', 'D2', 'F2']
      bar 48.0–56.0 '' → notes: ['A2', 'C3', 'D2', 'F2']
      bar 56.0–64.0 '' → notes: ['A2']
      bar 72.0–80.0 '' → notes: ['A2', 'C3', 'D2', 'F2']

  #### M: **Saws 2** | bars 64.0–80.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **VST:** Kickstart 2 | preset=''
    Clips (1):
      bar 64.0–80.0 '' → notes: ['D2']

  #### M: **Lead** | bars 64.0–80.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    **VST:** Kickstart 2 | preset=''
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=0.8095238209, BassMonoFrequency=120, Gain=1
    Clips (1):
      bar 64.0–80.0 '' → notes: ['A#2', 'A3', 'C4', 'D3', 'E3', 'F2', 'F3', 'G2']

  #### M: **Pad 1** | bars 52.0–63.0
    **VST:** Serum | preset=''
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    **EQ8** (0 active bands)
    Clips (2):
      bar 52.0–60.0 '' → notes: ['A3', 'D3']
      bar 60.0–63.0 '' → notes: ['A3']

  #### M: **Pad 2** | bars 55.0–63.0
    **VST:** Serum | preset=''
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    **EQ8** (0 active bands)
    Clips (1):
      bar 55.0–63.0 '' → notes: ['D2']

  #### M: **Pad 3** | bars 48.0–60.0
    **VST:** Serum | preset=''
    **EQ8** (0 active bands)
    Clips (1):
      bar 48.0–60.0 '' → notes: ['D2']


### G: **FX**
  #### A: **FX 1** | bars 16.0–74.541
    **StereoGain**: On=true, ChannelMode=1, StereoWidth=1, MidSideBalance=1, BassMonoFrequency=120, Gain=1
    Clips (16):
      bar 16.0–17.875 ''
      bar 17.875–18.0 ''
      bar 18.0–20.0 ''
      bar 20.0–20.5 ''
      bar 20.5–21.0 ''
      ... +11 more clips

  #### A: **FX 2** | bars 31.0–80.561
    **Reverb**: PreDelay=12.0000038, RoomSize=3, DecayTime=1299.67688, FreezeOn=false
    Clips (26):
      bar 31.0–31.249 ''
      bar 31.25–31.499 ''
      bar 31.5–31.749 ''
      bar 31.75–31.999 ''
      bar 32.0–32.561 ''
      ... +21 more clips

  #### A: **FX 3** | bars 48.0–82.078
    **EQ8** (0 active bands)
    Clips (2):
      bar 48.0–50.078 ''
      bar 80.0–82.078 ''

  #### A: **FX 4** | bars 48.0–52.171
    **EQ8** (0 active bands)
    Clips (1):
      bar 48.0–52.171 ''

  #### A: **FX 5** | bars 56.01–62.999
    **EQ8** (0 active bands)
    Clips (1):
      bar 56.01–62.999 ''

