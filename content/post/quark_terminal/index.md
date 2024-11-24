---
title: Quark terminal mode
subtitle: ''
summary: ''
date: "2024-11-24T00:00:00Z"

authors:
  - admin
tags: []
categories: []
projects: []

reading_time: true  # Show estimated reading time?
share: false  # Show social sharing links?
profile: true  # Show author profile?
comments: false  # Show comments?

# Cover image
# To use, place an image named `featured.jpg/png` in your page's folder.
# Otherwise, specify the `filename` option to load an image from your `assets/media/` folder.
# Placement options: 1 = Full column width, 2 = Out-set, 3 = Screen-width
# Focal point options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
# Set `preview_only` to `true` to just use the image for thumbnails.
image:
#   placement: 1
#   caption: "Photo by [Geo](https://github.com/gcushen/)"
#   focal_point: "Center"
  preview_only: true
#   alt_text: An optional description of the image for screen readers.
  # filename: my-image.jpg  # Uncomment to load an image from `assets/media/` instead.


# Optional header image (relative to `assets/media/` folder).
header:
  caption: ""
  image: ""

# editable: true

---

As part of my windows setup, I run a windows terminal quark mode in the background which I can always call using a hotkey ` Win + ` `. Here is how I set it up. Credits to [this github issue](https://github.com/microsoft/terminal/issues/9996). 

1. Go to your startup folder (Click `Win + R` and run shell:startup)
2. Create a shortcut to the Powershell "C:\Program Files\PowerShell\7\pwsh.exe".  I use powershell 7 here. Open the properties tab of the shortcut and change the target to `"C:\Program Files\PowerShell\7\pwsh.exe" -Command "wt -w _quake 'C:\Program Files\PowerShell\7\pwsh.exe'  -NoExit  -Command '& {clear}' -window minimized;Start-Sleep -Seconds 1;$app=New-Object -ComObject shell.application;$app.ToggleDesktop();"` I added a 1 second wait after launch quake. If the window doesn't disappear after logging in, try to extend it for a little longer.
3. Set "Run" option also to Minimized (this prevents any flicker) and apply.
4. Go the the windows terminal settings and open the setting JSON file. Add the `"compatibility.allowHeadless": true` to let the Terminal keep running even when all windows are closed.
