# duckyPad Profile Auto-switcher

[Get duckyPad](https://www.tindie.com/products/21984/) | [Official Discord](https://discord.gg/4sJCBx5) | [Project Main Page](https://github.com/dekuNukem/duckyPad)

This app allows your duckyPad to **switch profiles automatically** based on **current active window**.

![Alt text](resources/switch.gif)

## User Manual

### Windows

[Download the latest release here](https://github.com/dekuNukem/duckyPad-profile-autoswitcher/releases/latest)

Extract the `.zip` file and launch the app by clicking `duckypad_autoprofile.exe`:

![Alt text](resources/app.png)

Windows might complain about unsigned app.

Click `More info` and then `Run anyway`.

Feel free to [review the files](../pc_software), or run the source code directly with Python.

![Alt text](resources/defender.png)

### Mac

![Alt text](resources/underc.gif)

### Linux

![Alt text](resources/underc.gif)

### Using the App

Your duckyPad should show up in the `Connection` section.

![Alt text](resources/empty.png)

Profile-Autoswitching is based on a list of *rules*.

To create a new rule, click `New rule...` button:

![Alt text](resources/rulebox.png)

A new window should pop up:

![Alt text](resources/new.png)

Each rule contains **Application name**, **Window Title**, and the **Profile** to switch to.

**`App name`** and **`Window Title`**:

* Type in the keyword you want to match

* NOT case sensitive

**`Jump-to Profile`**:

* Can be Profile Number
	* 1-indexed
* Or Profile Name 
	* **duckyPad Pro ONLY** (for now)
	* Full Name
	* Case Sensitive

Click `Save` when done.

Current active window and a list of all windows are provided for reference.

-------

Back to the main window, duckyPad should now automatically switch profile once a rule is matched!

![Alt text](resources/active_rules.png)

* Rules are evaluated **from top to bottom**, and **stops at first match**!

* Currently matched rule will turn green. 

* Select a rule and click `Move up` and `Move down` to rearrange priority.

* Click `On/Off` button to enable/disable a rule.

That's pretty much it! Just leave the app running and duckyPad will do its thing!

## Launch Autoswitcher on Windows Startup

The easiest way is to place a shortcut in the Startup folder:

* Select the autoswitcher app and press `Ctrl+C`.

* Press `Win+R` to open the `Run...` dialog, enter `shell:startup` and click OK. This will open the Startup folder.

* Right click inside the window, and click "Paste Shortcut". 

## HID Command Protocol

Of course, now that duckyPad supports HID communication, you can write your own program to control it from PC!

[Click me for details](HID_details.md)!

## Questions or Comments?

Please feel free to [open an issue](https://github.com/dekuNukem/duckypad/issues), ask in the [official duckyPad discord](https://discord.gg/4sJCBx5), DM me on discord `dekuNukem#6998`, or email `dekuNukem`@`gmail`.`com` for inquires.

