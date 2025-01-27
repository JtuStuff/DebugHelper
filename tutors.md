New testing instructions:
0. Disable NootedRed on your system 
1. Install
https://github.com/acidanthera/DebugEnhancer
and add -dbgenhiolog -nreddbg to your boot args
2. Replace whatever build of NootedRed you had with the build NC or Visual is going to send you, or the build you're instructed to test
3. Disable stealth mode
https://support.apple.com/lt-lt/guidhe/mac-help/mh17133/mac
4. Find your macOS's IP with instructions from
https://www.hellotech.com/guide/for/how-to-find-ip-address-on-mac
 It should look like 192.*.*.* , 10.*.*.* or something like that, and will be referred to as {IP} henceforth in the instructions 
5. Find a second device with access to a terminal. It can be a computer or an Android phone with Termux installed. You can grab Termux here:
https://f-droid.org/repo/com.termux_118.apk
Do not install the one from Google Play.
6. Ping the device with 
ping -c 5 {IP}
to ensure networking is functional
7. Enable SSH following this:
https://support.apple.com/lt-lt/guide/mac-help/mchlp1066/mac
Turn on full disk access as well
8. Edit /etc/sudoers, adding the following line:
{username} ALL = (ALL) NOPASSWD:ALL
, where {username} is replaced by your actual user name, and remember to save the file
9. Enable stealth mode
10. Restart macOS and try to ssh in from the second device
11. Once SSH works, enable NootedRed, do a OC snapshot, and reboot
12. Once the system starts booting, run the following command ({password} being your user password): 
while true; do sshpass -p {password} ssh -o StrictHostKeyChecking=no {user name}@{IP} -t "sudo dmesg" | curl -F file=@- 0x0.st; done 
13. Once the screen goes black with the backlight on for 30+ seconds, run the following two in a separate terminal session: 
1) sshpass -p {password} ssh -o StrictHostKeyChecking=no {user name}@{IP} -t "ioreg -flxw0" | curl -F file=@- 0x0.st 
2) sshpass -p {password} ssh -o StrictHostKeyChecking=no {user name}@{IP} -t "/System/Library/Extensions/AppleGraphicsControl.kext/Contents/MacOS/AGDCDiagnose" | curl -F file=@- 0x0.st 
14. Send a link from each command's output 
15. Rejoice, because you just managed to finish all steps without facing any major roadblocks, and wait for analysis of the output 