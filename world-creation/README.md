# Map creation

Please make sure that you have `blender>=2.79` installed. Note that the version of the ubuntu repository might be out of date.

## Blender
Create a map in blender. Make sure you can use the option `File > Export > Collada (.dae)`. We will export the file later.

## revolve-simulator
### Groups A & B
Open a terminal in this folder.
```bash
cp -r inferno/models/inferno $SIM_HOME/revolve/models/
cp inferno/worlds/inferno.world $SIM_HOME/revolve/worlds/
```

Open blender and replace `$SIM_HOME/revolve/models/meshes/inferno.dae`

Open `$SIM_HOME/revolve/tutorial.py` and
change the worldfile: `world_file="worlds/inferno.world"`

### Group C & D
Open a terminal in this folder.
```bash
mkdir $SIM_HOME/tol-revolve/tools/models/inferno
cp -r inferno/* $SIM_HOME/tol-revolve/tools/models/inferno
cd $SIM_HOME/tol-revolve/tools/models/inferno
mv worlds/inferno.world .
mv models/inferno/* .
rmdir models/inferno
rmdir models
rmdir worlds
```


Open blender and replace `$SIM_HOME/tol-revolve/tools/models/inferno/meshes/inferno.dae`

Open `$SIM_HOME/tol-revolve/scripts/offline-evolve/offline-evolve.world` and 
change
```xml
    <include>
      <uri>model://tol_ground</uri>
    </include>
```
to
```xml
    <include>
      <uri>model://inferno</uri>
    </include>
```


Open `$SIM_HOME/tol-revolve/scripts/offline-evolve/offline_evolve.py` and
change the code to use the argument
```python
# pose = Pose(position=Vector3(0, 0,  -bbox.min.z))
pose = Pose(position=Vector3(0, 0, args.init_z))
```


Open `$SIM_HOME/tol-revolve/tol/config/config.py` and
change the value for the argument `--init-z` accordingly.
