# Maxwell Render ASCII Scene Translator #
**Version 0.1** Released 2015-12-05  
by Andrew Hazelden  

## Overview ##

The `mxs2ascii.py` tool is a new PyMaxwell based python script that will translate a binary format Maxwell Render .mxs scene file into an plain text ASCII format document with the .mxa extension.

There is also a corresponding set of syntax highlighters that are provided with the new toolset. The syntax highlighting modules make it easier to review and edit the new .mxa format scene using one your favorite text editors like Notepad++ (Windows), TextWrangler and BBEdit (Mac), or Gedit (Multi-platform).

Here is an example Maxwell ASCII .mxa scene file with syntax highlighting enabled in TextWrangler:

![This is a sample mxa file that has syntax highlighting](images/mxa_syntax_highlighting.png)

**Note:** This proof of concept `.mxa` file format for use by rendering TDs is a 3rd party development effort that is being developed independently from Next Limit and the Maxwell Render team. Please don't bother their support department if you have issues with the open source mxs2ascii scene translators and scripts in this repository.

## MXA Development Roadmap ##

### Phase 1 - Binary to ASCII (The Current Stage) ###

Currently the `mxs2ascii.py` script is able to successfully translate the input `.mxs` scene file's Render Options, and Camera node information into the new `.mxa` format.

Work is continuing right now on implementing the rest of the data types in the `mxs2ascii.py` script that are present in a binary format Maxwell Render `.mxs` scene.

### Phase 2 - ASCII to Binary Converter ###

Work will start on making part two of this project which is to assemble a matching `ascii2mxs.py` translator to bring your ASCII scene description format back into the binary domain.

### Phase 3 - ASCII Direct to Render ###

Once there is a set of working file translators that can seamlessly translate a scene from the MXS to MXA file formats and back, work will start on the final stage 3 effor which is to create a `mxa2render.py` script for rendering a .mxa scene file in Maxwell Render that was loaded straight from an ascii format `.mxa` document.

## Open Source License ##

*The Maxwell Render ASCII Scene Translator is distributed under a GPL v3 license.*

## Script Installation ##

Copy the `mxs2ascii.py` python file to your Maxwell 3.2 scripts directory:

### Windows Script Path ###

    C:/Program Files/Next Limit/Maxwell 3/scripts/

### Linux Script Path ###

    /opt/maxwell-3.2/scripts/
    or
    $home/maxwell-3.2/scripts/

### Mac Script Path ###

    /Applications/Maxwell 3/scripts/

## How do I use the script? ##

![Loading the mxs2ascii.py script in PyMaxwell](images/pymaxwell_view.png)

**Step 1.** Launch PyMaxwell and open up the `mxs2ascii.py` python script.

**Step 2.** Edit the "mxsFilePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXS scene file:

![Editing the mxsFilePath variable](images/editing-the-mxs-file-path.png)

**Step 3.** Select the **Script > Run** menu item in PyMaxwell.

![PyMaxwell Run Menu](images/pymaxwell-run-menu.png)

The script will start running. First the script will verify the mxs scene file exists.

Then the scene will be opened in Maxwell and the scene elements and parameters will be exported to an ASCII text document with the name of `<scene>.mxa`. This new file is saved to the same folder as the original mxs scene file.

Here is a snapshot of the typical console output displayed by the mxs2ascii script in PyMaxwell:

![PyMaxwell Console Output](images/pymaxwell-console-output.png)


* * *

I hope this tool improves your coding workflow as you develop new Maxwell scene files using a plain text editor.

At this point I find the script is helpful for quickly reviewing all of the active render settings and camera parameters in a Maxwell scene so you can track down any unexpected settings without having to click and scroll through each of the different panels and views in Maxwell Studio.

Cheers,  
Andrew Hazelden

Email: [andrew@andrewhazelden.com](mailto:andrew@andrewhazelden.com)   
Blog: [http://www.andrewhazelden.com](http://www.andrewhazelden.com)  
Twitter: [@andrewhazelden](https://twitter.com/andrewhazelden)  
Google+: [https://plus.google.com/+AndrewHazelden](https://plus.google.com/+AndrewHazelden)
