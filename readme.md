# Maxwell Render ASCII Scene Translator #
**Version 0.1** Released 2015-12-05  
by Andrew Hazelden  

## Overview ##

The `mxs2ascii.py` tool in a new PyMaxwell based python script that will translate a binary format Maxwell Render .mxs scene file into an plain text ASCII format document with the .mxa extension.

**Note:** This proof of concept .mxa file format is a 3rd party development effort that is being developed separately from Next Limit and the Maxwell Render team. Please don't bother their support department if you have issues with the scene translators and scripts in this repository.

There is also a corresponding set of syntax highlighters that are provided with the new toolset. The syntax highlighting modules make it easier to review and edit the new .mxa format scene using one your favorite text editors like Notepad++ (Windows), TextWrangler and BBEdit (Mac), or Gedit (Multi-platform).

Here is an example .mxa Maxwell ASCII Scene file with syntax highlighting enabled:

![This is a sample mxa file that has syntax highlighting](images/mxa_syntax_highlighting.png)

## Development ##

Right now the `mxs2ascii.py` script is able to successfully translate the input `.mxs` scene file's Render Options, and Camera nodes information into the new `.mxa` format.

Once the rest of the data types in a Maxwell Render `.mxs` scene have been enabled in the `mxs2ascii.py` script, work will start on making part two of this project which is to assemble a matching `ascii2mxs.py` translator to bring your ascii scene description format back into the binary domain

Thee will also be a `mxa2render.py` script for rendering a scene file in Maxwell Render that was loaded from an ascii `.mxa` document.

## Open Source License ##

*Maxwell Render ASCII Scene Translator is distributed under a GPL v3 license.*

## Script Installation ##

Copy the `mxs2ascii.py` python file to your Maxwell 3.2 scripts directory:

### Windows Script Path ###

    C:/Program Files/Next Limit/Maxwell 3/scripts/

### Linux Script Path ###

    /opt/maxwell/3/scripts/

### Mac Script Path ###

    /Applications/Maxwell 3/scripts/


## How do I use the script? ##

![Loading the mxs2ascii.py script in PyMaxwell](images/pymaxwell_view.png)

**Step 1.** Launch PyMaxwell and open up the `mxs2ascii.py` python script.

**Step 2.** Edit the "mxsFilePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXS scene file.

**Step 3.** Select the **Script > Run** menu item in PyMaxwell.

The script will start running. First the script will verify the mxs scene file exists. Then the scene will be opened in Maxwell and all of the scene elements and parameters will be exported to an ASCII text document with the name of `<scene>.mxa`. This new file is saved to the same folder as the original mxs scene file.



* * *

I hope this tool improves your coding workflow as you develop new Maxwell scene files using a plain text editor.

Cheers,  
Andrew Hazelden

Email: [andrew@andrewhazelden.com](mailto:andrew@andrewhazelden.com)   
Blog: [http://www.andrewhazelden.com](http://www.andrewhazelden.com)  
Twitter: [@andrewhazelden](https://twitter.com/andrewhazelden)  
Google+: [https://plus.google.com/+AndrewHazelden](https://plus.google.com/+AndrewHazelden)
