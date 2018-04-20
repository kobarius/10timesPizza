export ALSADEV="plughw:1,0"
export AUDIODEV="/dev/dsp1"
sudo modprobe snd-pcm-oss
#~/User/*****/julius/julius-4.2.3/julius/julius -C ~/User/*****/julius/julius-kits/dictation-kit-v4.2.3/fast.jconf -charconv EUC-JP UTF-8
#~/User/*****/julius/julius-4.2.3/julius/julius -C ~/User/*****/julius/julius-kits/dictation-kit-v4.2.3/pizza.jconf -charconv EUC-JP UTF-8
~/User/*****/julius/julius-4.2.3/julius/julius -C ~/User/*****/julius/julius-kits/dictation-kit-v4.2.3/pizza.jconf -module -charconv EUC-JP UTF-8
