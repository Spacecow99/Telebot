# Telebot

This report provides an analysis of the Telegram backdoor bot used by the russian group known as Telebots (Sandword, etc). A decompiled and deobfuscated version of the Telebots' telebot backdoor. I have renamed most variable names in order to add greater context and make the code easier to read for those studying it. A copy of the obfuscated version is available at [this Gist](https://gist.github.com/Spacecow99/eb77d179d23c31e7cf3c9c8b2f0d00ee). I have been sitting on this report for some time but believe it provides some historical context in light of the continued operations attributed to this group.

I found this sample on a public repository in the format of a pyinstaller executable but for brievety we will not go over the extraction process as there are many sources available covering this topic already. We will cover the core functionality of this simple bot and see how it falls in line with the continued trend of targeted attacks that rely on simple first stage implants. Since the first occurance of this bot we have seen this group shift its code base to rust which could indicate that this python implementation was simply a test sample experimenting with the use of the Telegram C2 channel.

## Sample Details

- Format: PE32 (Pyinstaller)
- Hash: `904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c`
- Sample: [http://hybrid-analysis.com/sample/904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c](http://hybrid-analysis.com/sample/904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c)
- Reference: [www.welivesecurity.com/2016/12/13/rise-telebots-analyzing-disruptive-killdisk-attacks/](www.welivesecurity.com/2016/12/13/rise-telebots-analyzing-disruptive-killdisk-attacks/)
