# Juliusの使い方

## 音声デバイスの設定

1. USBオーディオアダプタを認識しているか確認（下記の場合だとDevice 006がUSBオーディオアダプタ。）

> lsusb
>> Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp.  
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub  
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.  
Bus 001 Device 004: ID 2019:ab2a PLANEX GW-USNano2 802.11n Wireless Adapter [Realtek RTL8188CUS]  
Bus 001 Device 005: ID 05e3:0608 Genesys Logic, Inc. USB-2.0 4-Port HUB  
Bus 001 Device 006: ID 0d8c:013a C-Media Electronics, Inc.  


2. USBオーディオアダプタの優先度を確認（下記の場合、内蔵オーディオが優先されている。）

> cat /proc/asound/modules
>> 0 snd_bcm2835  
1 snd_usb_audio

3. USBオーディオアダプタの優先度を上げる

> vi /etc/modprobe.d/alsa-base.conf  

index=-2をindex=0にします。  

>> \# options snd-usb-audio index=-2  
options snd-usb-audio index=0

4. 再起動
> sudo reboot

5. USBオーディオアダプタの優先度を確認

> cat /proc/asound/modules
>> 0 snd_usb_audio  
1 snd_bcm2835


6. 録音と再生を確認


## Juliusのインストール

1. Julius他をダウンロード
※展開するディレクトリは任意（今回は"~"とする）
> cd ~  
wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F59049%2Fjulius-4.2.3.tar.gz'  
wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F59050%2Fdictation-kit-v4.2.3.tar.gz'  
wget --trust-server-names 'http://osdn.jp/frs/redir.php?m=iij&f=%2Fjulius%2F51159%2Fgrammar-kit-v4.1.tar.gz'

2. Juliusを解凍し、configureしてmake

> tar xvzf julius-4.2.3.tar.gz  
cd julius-4.2.3  
./configure  
make

3. ディクテーションキットと文法認識キットを解凍

> mkdir ~/julius-kits  
cd ~/julius-kits  
tar xvzf ~/dictation-kit-v4.2.3.tar.gz  
tar xvzf ~/grammar-kit-v4.1.tar.gz

4. USBオーディオのカード番号を確認（下記の場合は0番。）

> arecord -l
>> \*\*\*\* ハードウェアデバイス CAPTURE のリスト \*\*\*\*  
カード 0: Device [USB PnP Sound Device], デバイス 0: USB Audio [USB Audio]  
  サブデバイス: 1/1  
  サブデバイス #0: subdevice #0

5. カード番号を環境変数に指定

> export ALSADEV=hw:0

6. snd-pcm-ossモジュールの組み込み

> sudo modprobe snd-pcm-oss

※下記コマンドで起動時にsnd-pcm-ossモジュールがロードされるようになる。
> sudo sh -c "echo snd-pcm-oss >> /etc/modules"


7. Juliusを実行
> ~/julius-4.2.3/julius/julius -C ~/julius-kits/dictation-kit-v4.2.3/fast.jconf -charconv EUC-JP UTF-8

8. Juliusをサーバーモードで実行  

"-module"オプションを付けて実行する。
> ~/julius-4.2.3/julius/julius -C ~/julius-kits/dictation-kit-v4.2.3/fast.jconf -module -charconv EUC-JP UTF-8

### Reference
[1] http://cubic9.com/Devel/%C5%C5%BB%D2%B9%A9%BA%EE/RaspberryPi/%C6%FC%CB%DC%B8%EC%B2%BB%C0%BC%C7%A7%BC%B1/  
[2] https://teratail.com/questions/35410
