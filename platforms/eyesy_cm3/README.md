# EYESY CM3 OS 

Configuring software for CM3 based EYESY.

base system: 2024-11-19-raspios-bookworm-armhf-lite.img.xz

Boot up, do initial config. Make second ext4 primary partition for "/sdcard" user storage.

    sudo apt-get update
    sudo apt-get install vim git

## Fixing the audio driver on EY and OG CM3 designs.

The wm8731 uses SPI instead of I2C for config. 

Build and install new kernel and modules using instructions here: https://www.raspberrypi.com/documentation/computers/linux_kernel.html#cross-compile-the-kernel

First make these changes to kernel:

```
diff --git a/sound/soc/bcm/audioinjector-pi-soundcard.c b/sound/soc/bcm/audioinjector-pi-soundcard.c
index e675cceb3..30abfc624 100644
--- a/sound/soc/bcm/audioinjector-pi-soundcard.c
+++ b/sound/soc/bcm/audioinjector-pi-soundcard.c
@@ -86,7 +86,7 @@ static int audioinjector_pi_soundcard_dai_init(struct snd_soc_pcm_runtime *rtd)
 
 SND_SOC_DAILINK_DEFS(audioinjector_pi,
        DAILINK_COMP_ARRAY(COMP_CPU("bcm2708-i2s.0")),
-       DAILINK_COMP_ARRAY(COMP_CODEC("wm8731.1-001a", "wm8731-hifi")),
+       DAILINK_COMP_ARRAY(COMP_CODEC("spi2.0", "wm8731-hifi")),
        DAILINK_COMP_ARRAY(COMP_PLATFORM("bcm2835-i2s.0")));
 
 static struct snd_soc_dai_link audioinjector_pi_soundcard_dai[] = {
diff --git a/sound/soc/codecs/wm8731-spi.c b/sound/soc/codecs/wm8731-spi.c
index 542ed097d..73b8d83d7 100644
--- a/sound/soc/codecs/wm8731-spi.c
+++ b/sound/soc/codecs/wm8731-spi.c
@@ -17,7 +17,7 @@
 #include "wm8731.h"
 
 static const struct of_device_id wm8731_of_match[] = {
-       { .compatible = "wlf,wm8731", },
+       { .compatible = "wlf,wm8731-spi", },
        { }
 };
 MODULE_DEVICE_TABLE(of, wm8731_of_match);

```

in the kernel config, enable the wm8731-spi driver:

```
CONFIG_SND_SOC_WM8731_SPI=m
```

compile the dts:

```
sudo dtc -@ -I dts -O dtb -o /boot/overlays/wm8731-spi.dtbo audioinjector-wm8731-audio-spi-overlay.dts
```

