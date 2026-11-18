import sherpa_onnx, soundfile as sf, sys
name, text, out, speed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv)>4 else 1.0
d=f'/home/claude/tts/vits-piper-hi_IN-{name}-medium'
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
    model=f'{d}/hi_IN-{name}-medium.onnx', tokens=f'{d}/tokens.txt', data_dir=f'{d}/espeak-ng-data'), num_threads=2))
tts=sherpa_onnx.OfflineTts(cfg)
a=tts.generate(text, sid=0, speed=speed)
sf.write(out, a.samples, a.sample_rate)
print(len(a.samples)/a.sample_rate)
