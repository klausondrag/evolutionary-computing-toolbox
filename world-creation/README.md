  # World creation

  Please make sure that you have `blender>=2.79` installed. Note that the version of the Ubuntu repository might be out of date.

  ## Using Blender
  When you first open Blender, delete all the existing objects. You may save this clean state using `File > Save Startup File` so that the next time you start Blender, you don't have these unwanted objects. If you're creating worlds using heightmaps, this is a great tutorial to look at: <https://johnflower.org/tutorial/make-mountains-blender-heightmaps>. When adding the grid, it's better to ensure that the cursor is set to the centre of the plane so that your mesh is not offset elsewhere. You can scale your grid by pressing `S` and then using your mouse. You may skip the steps under 'Improve the Quality' since we're not really concerned about the quality of the visual appearance. Also, that particular step is intensive on computer resources. Make sure that the mesh is centered correctly so that it loads in the central region of Gazebo later. When you're done editing your world, export it as a .dae file using `File > Export > Collada (.dae)`. Make sure that the option to include modifiers is selected while exporting. Otherwise, your chages wouldn't be applied in the exported file.

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

  ### Groups C & D
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
