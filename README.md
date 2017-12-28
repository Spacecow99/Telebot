# Telebot

This writeup is an analysis of the Telegram backdoor bot previously used by the threat group known as Telebots. Included is a decompiled and deobfuscated version of the Telebots' telebot backdoor in the form of a python script. Most indentifiers have been renamed in order to add context and simplify the code for those studying it. A copy of the obfuscated version is [available here](https://gist.github.com/Spacecow99/eb77d179d23c31e7cf3c9c8b2f0d00ee). I have been sitting on this report for some time but believe it provides some historical context in light of the continued operations attributed to this group.

This sample was found on a public repository in the format of a pyinstaller executable but for the sake of brevity we will not go over the extraction process as there are many sources online covering this topic already. We will cover the core functionality of this simple bot and see how it falls in line with the continued trend of targeted attacks that rely on simple yet effective backdoors. Since the first occurance of this bot the authors appear to have shifted its codebase to rust which could indicate that the python implementation was simply them experimenting with the use of the Telegram C2 channel (although this is just a theory).

----

## Sample Details

- Format: PE32 (Pyinstaller)
- Hash: `904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c`
- Sample: [http://hybrid-analysis.com/sample/904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c](http://hybrid-analysis.com/sample/904df5d6b900fcdac44c002f03ab1fbc698b8d421a22639819b3b208aaa6ea2c)
- Reference: [www.welivesecurity.com/2016/12/13/rise-telebots-analyzing-disruptive-killdisk-attacks/](http://www.welivesecurity.com/2016/12/13/rise-telebots-analyzing-disruptive-killdisk-attacks/)
