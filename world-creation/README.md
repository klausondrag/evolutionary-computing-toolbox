# World creation

Please make sure that you have `blender>=2.79` installed. Note that the version of the ubuntu repository might be out of date.

## Blender
Create a world in blender. Make sure you can use the option `File > Export > Collada (.dae)`. We will export the file later.

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


## Manual gazebo world (not needed, just for documentation)
Replace the world `example` with a name of your choosing. 
```bash
mkdir -p ~/.gazebo/custom_worlds/example
```
Open blender and output the `.dae` file to `~/.gazebo/custom_worlds/example/example.dae`

Create a world file by executing the code below. Make sure to change the directory and the file name. Additionally, change the world name and the uri in the world file.
```bash
cat << EOM >> ~/.gazebo/custom_worlds/example/example.world
<?xml version="1.0"?>
<sdf version="1.4">
  <world name="example">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <model name="my_mesh">
      <pose>0 0 0  0 0 0</pose>
      <static>true</static>
      <link name="body">
        <visual name="visual">
          <geometry>
            <mesh><uri>file://example.dae</uri></mesh>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
EOM
```

Load the map by running `gazebo custom_worlds/example.world`
Make sure that the world loads correctly and everything is defined as expected.
