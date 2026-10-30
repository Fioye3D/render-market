# Upload RenderMarket

Unzip the archive first. The repository should contain the project files, not just a ZIP attachment.

`RenderMarket_Code_v0.4.zip` contains code and documentation. `RenderMarket_Portfolio_v0.4.zip` also includes images, fonts, the Figma import payload and actual 3D files. Use the complete package for the working visual prototype.

## Publish with Git

1. Sign in as **Fioye3D** and create an empty public repository named **rendermarket-ui-ux**. Leave the initial README and licence options unchecked, because these files are already included.
2. Open a terminal inside the extracted `rendermarket-ui-ux` folder.
3. Run:

```powershell
git init
git add .
git commit -m "Add RenderMarket UI/UX portfolio"
git branch -M main
git remote add origin https://github.com/Fioye3D/rendermarket-ui-ux.git
git push -u origin main
```

Complete Git's secure sign-in if prompted. If using the original workspace, it already has Git history and the intended `origin`; use its existing setup instead of adding the remote again.

The complete package contains Blender files larger than GitHub's 25 MiB browser-upload limit. Use Git or GitHub Desktop for that package. All prepared project files are below the 100 MiB regular Git file limit. These limits are documented in [GitHub's file-size guidance](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

## Preview locally

From the extracted project folder, run:

```powershell
python -m http.server 8765
```

Open `http://localhost:8765/prototype/`. The viewer needs HTTP; opening the HTML by double-clicking can prevent GLB loading.

The repository is a new independent UI/UX portfolio study with disclosed assistance. Sample prices and creator profiles do not imply a working payment service. A public repository alone does not deploy the website or create a Figma prototype link.
