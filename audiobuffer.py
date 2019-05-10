class AudioBuffer(list):
    def __init__(self, *args, **kwargs):
       super(AudioBuffer, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        return AudioBuffer(list.__getitem__(self, key))

    def methodFromAudioBuffer(self):
        print("my list is", self)

foo = AudioBuffer([15, 25, 35])
foo[1:].methodFromAudioBuffer()
