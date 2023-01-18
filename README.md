# DOTS IJobEntity Upgrader

NOTE: This tool is no longer required as of the Entities pre-1.0 release

Adjusts IJobEntity object initializers to not use inlined SystemAPI calls.


For example, in your system, you initialize an IJobEntity struct like this:

    protected override void OnUpdate()
    {
      Dependency = new PowerGridMembershipJob {
        Outputs = SystemAPI.GetBufferLookup<ModuleOutputConnection>(true),
        Placeables = SystemAPI.GetComponentLookup<Placeable>(),
      }.Schedule(Dependency);
    }

This tool will update that initializer to the following:

    protected override void OnUpdate()
    {
      job = new PowerGridMembershipJob();
      job.Outputs = SystemAPI.GetBufferLookup<ModuleOutputConnection>(true);
      job.Placeables = SystemAPI.GetComponentLookup<Placeable>();
      job.Schedule(Dependency);
    }

See the [Official Upgrade Guide](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/upgrade-guide.html) for detailed information on upgrading your project from .51 to 1.0.

## Quick start

Simply run

`python runner.py --dir \<Directory to your systems folder\> --commit true

## Installation

* requires Python 3.x installation

## Script Options
  -h, --help            show this help message and exit

  --dir DIR             The top level directory containing all of the .cs files that need to be updated. (default: None)

  --commit {true,false}
                        Set to false to merely print out potential results, no files will be changed. True will update the files (default: false)

## Caveats

* UTF is a real mystery to me. There's a bug where the script will insert a U+FEFF or other nonsense characters into your files. I tried a few things to fix this but didn't get far. I ended up just using find+replace all in my IDE to get rid of them.
* This tool assumes one IJobEntity initializer per file
* This tool assumes the object properties are all initialized on single lines. For example, this line will get fucked by this tool:

        Placeables =
            SystemAPI.GetComponentLookup<Placeable>();

It must looke like:

        Placeables = SystemAPI.GetComponentLookup<Placeable>();

* This tool was made in a day and tested on 1 (albeit large) project. There's probably other caveats to using it, especially if you write your initializers in any kind of weird format. I'd still recommend going through your components by hand and checking the results.
